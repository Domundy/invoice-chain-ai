import os
import json
from pathlib import Path
from typing import Optional, Dict, Any, List, Callable
from dotenv import load_dotenv

load_dotenv()

# Try to import psycopg (psycopg-binary). If not available, functions will be no-ops.
try:
    import psycopg
    from psycopg.rows import dict_row
except Exception:
    psycopg = None  # type: ignore

# Make langsmith optional: provide a no-op traceable decorator if missing
try:
    from langsmith import traceable  # type: ignore
except Exception:
    def traceable(*t_args, **t_kwargs) -> Callable:
        def _decorator(fn):
            return fn
        return _decorator

DB_INIT_SQL = str(Path(__file__).parent / "init.sql")


def _get_conn():
    dsn = os.getenv("DATABASE_URL")
    if not dsn or psycopg is None:
        return None
    return psycopg.connect(dsn, row_factory=dict_row)


@traceable(name="Init DB")
def init_db():
    """
    Create schema by executing db/init.sql if present.
    """
    conn = _get_conn()
    if conn is None:
        return {"status": "noop", "reason": "no DATABASE_URL or psycopg not installed"}
    try:
        sql = None
        if os.path.exists(DB_INIT_SQL):
            with open(DB_INIT_SQL, "r", encoding="utf-8") as f:
                sql = f.read()
        with conn:
            with conn.cursor() as cur:
                if sql:
                    cur.execute(sql)
                else:
                    # fallback minimal single-table schema
                    cur.execute(
                        """
                        CREATE TABLE IF NOT EXISTS customers (
                            id SERIAL PRIMARY KEY,
                            name TEXT NOT NULL,
                            customer_prompt TEXT,
                            ibans TEXT[] DEFAULT ''::text[],
                            created_at TIMESTAMPTZ DEFAULT now()
                        );
                        """
                    )
        return {"status": "ok"}
    finally:
        conn.close()


# Internal helpers
def _find_customer_by_iban(conn, iban: str) -> Optional[Dict[str, Any]]:
    if not iban:
        return None
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id, name, customer_prompt, ibans FROM customers WHERE %s = ANY(ibans) LIMIT 1;",
            (iban,),
        )
        return cur.fetchone()


def _insert_customer(conn, name: str, customer_prompt: Optional[str], ibans: Optional[List[str]] = None) -> Optional[int]:
    """
    Insert a customer and return inserted customer id.
    ibans should be a list of strings or None.
    """
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO customers (name, customer_prompt, ibans) VALUES (%s, %s, %s) RETURNING id;",
            (name, customer_prompt, ibans),
        )
        row = cur.fetchone()
        if not row:
            return None
        if isinstance(row, dict):
            return row.get("id")
        try:
            return row[0]
        except Exception:
            return None


# PUBLIC lookup functions
@traceable(name="Get Customer by IBAN")
def get_customer_by_iban(iban: str) -> Optional[Dict[str, Any]]:
    conn = _get_conn()
    if conn is None:
        return None
    try:
        with conn:
            cust = _find_customer_by_iban(conn, iban)
            if not cust:
                return None
            return {"customer": dict(cust)}
    finally:
        conn.close()


@traceable(name="Get Customer by Invoice (IBAN)")
def get_customer_by_invoice(parsed_invoice: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Try to find a customer for the parsed_invoice based on the iban.
    Returns None if no match.
    """
    iban = parsed_invoice.get("iban")
    if not iban:
        return None
    return get_customer_by_iban(iban)


def seed_customers_from_json(json_path: str) -> Dict[str, Any]:
    """
    Load customers from a JSON file and insert into DB.
    Expected format: [{ "name": "...", "customer_prompt": "...", "ibans": ["IBAN...","..."] }, ...]
    This function clears existing customers and seeds fresh data from the JSON.
    """
    # Ensure DB schema exists / is migrated before seeding
    try:
        init_res = init_db()
    except Exception as e:
        return {"error": f"init_db failed: {e}"}

    conn = _get_conn()
    if conn is None:
        return {"error": "No DATABASE_URL configured or psycopg not installed"}
    if not os.path.exists(json_path):
        return {"error": "seed file not found"}
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    inserted = 0
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("TRUNCATE TABLE customers RESTART IDENTITY CASCADE;")
            for item in data:
                name = item.get("name") or "unknown"
                cust_prompt = item.get("customer_prompt")
                ibans = item.get("ibans") or []
                # ensure list type for psycopg to map to text[]
                if not isinstance(ibans, list):
                    ibans = [ibans] if ibans else []
                _insert_customer(conn, name, cust_prompt, ibans)
                inserted += 1
        return {"inserted": inserted}
    finally:
        conn.close()


def choose_prompt(customer_info: Dict[str, Any]) -> str:
    """
    Return the stored customer_prompt if present; otherwise 'default'.
    """
    if not customer_info:
        return "default"
    cust = customer_info.get("customer") or {}
    prompt = cust.get("customer_prompt")
    return prompt if prompt else "default"