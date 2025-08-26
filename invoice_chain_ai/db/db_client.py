import os
import json
from pathlib import Path
from typing import Optional, Dict, Any, List

# Try to import psycopg (psycopg-binary). If not available, functions will be no-ops.
try:
    import psycopg
    from psycopg.rows import dict_row
except Exception:
    psycopg = None  # type: ignore

# NEW: traceable import
from langsmith import traceable

DATABASE_URL_ENV = "DATABASE_URL"
DB_INIT_SQL = str(Path(__file__).parent / "init.sql")


def _get_conn():
    dsn = os.getenv(DATABASE_URL_ENV)
    if not dsn or psycopg is None:
        return None
    return psycopg.connect(dsn, row_factory=dict_row)


@traceable(name="Init DB")
def init_db():
    """
    Create schema by executing db/init.sql if present.
    No automatic data insertion here.
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
                    # fallback minimal schema (added customer_prompt column)
                    cur.execute(
                        """
                        CREATE TABLE IF NOT EXISTS customers (
                            id SERIAL PRIMARY KEY,
                            name TEXT NOT NULL,
                            customer_prompt TEXT,
                            created_at TIMESTAMPTZ DEFAULT now()
                        );
                        CREATE TABLE IF NOT EXISTS accounts (
                            id SERIAL PRIMARY KEY,
                            customer_id INTEGER REFERENCES customers(id) ON DELETE CASCADE,
                            iban TEXT UNIQUE
                        );
                        CREATE TABLE IF NOT EXISTS addresses (
                            id SERIAL PRIMARY KEY,
                            customer_id INTEGER REFERENCES customers(id) ON DELETE CASCADE,
                            address_type TEXT,
                            name TEXT,
                            line1 TEXT,
                            line2 TEXT,
                            postal_code TEXT,
                            city TEXT,
                            country TEXT
                        );
                        """
                    )
        return {"status": "ok"}
    finally:
        conn.close()


# Internal helpers (used by lookups and seeder)
def _find_customer_by_iban(conn, iban: str) -> Optional[Dict[str, Any]]:
    if not iban:
        return None
    with conn.cursor() as cur:
        cur.execute(
            "SELECT customers.id, customers.name FROM customers JOIN accounts ON accounts.customer_id = customers.id WHERE accounts.iban = %s LIMIT 1;",
            (iban,),
        )
        return cur.fetchone()

def _find_customer_by_name_city(conn, name: str, city: str) -> Optional[Dict[str, Any]]:
    if not name:
        return None
    with conn.cursor() as cur:
        if city:
            cur.execute(
                "SELECT customers.id, customers.name FROM customers JOIN addresses ON addresses.customer_id = customers.id WHERE lower(customers.name) = lower(%s) AND lower(addresses.city) = lower(%s) LIMIT 1;",
                (name, city),
            )
            r = cur.fetchone()
            if r:
                return r
        cur.execute("SELECT id, name FROM customers WHERE lower(name) = lower(%s) LIMIT 1;", (name,))
        return cur.fetchone()


def _insert_customer(conn, name: str, customer_prompt: str | None = None) -> Optional[int]:
    """
    Insert a customer and optional customer_prompt. Returns inserted customer id.
    """
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO customers (name, customer_prompt) VALUES (%s, %s) RETURNING id;",
            (name, customer_prompt),
        )
        row = cur.fetchone()
        if not row:
            return None
        # support dict_row (dict) or tuple result
        if isinstance(row, dict):
            return row.get("id")
        try:
            return row[0]
        except Exception:
            return None


def _ensure_account(conn, customer_id: int, iban: Optional[str]):
    if not iban:
        return
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO accounts (customer_id, iban) VALUES (%s, %s) ON CONFLICT (iban) DO NOTHING RETURNING id;",
            (customer_id, iban),
        )
        return cur.fetchone()


def _ensure_address(conn, customer_id: int, addr: Dict[str, Any]):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT id FROM addresses
            WHERE customer_id = %s AND coalesce(lower(line1),'') = coalesce(lower(%s),'') AND coalesce(lower(postal_code),'') = coalesce(lower(%s),'') AND coalesce(lower(city),'') = coalesce(lower(%s),'')
            LIMIT 1;
            """,
            (customer_id, addr.get("address_line_1"), addr.get("postal_code"), addr.get("city")),
        )
        exists = cur.fetchone()
        if exists:
            return exists["id"]
        cur.execute(
            """
            INSERT INTO addresses (customer_id, address_type, name, line1, line2, postal_code, city, country)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id;
            """,
            (
                customer_id,
                addr.get("address_type"),
                addr.get("name"),
                addr.get("address_line_1"),
                addr.get("address_line_2"),
                addr.get("postal_code"),
                addr.get("city"),
                addr.get("country"),
            ),
        )
        return cur.fetchone()["id"]


# PUBLIC lookup functions (no auto-create)
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
            customer_id = cust["id"]
            with conn.cursor() as cur:
                cur.execute("SELECT iban FROM accounts WHERE customer_id = %s;", (customer_id,))
                accounts = [r["iban"] for r in cur.fetchall()]
                cur.execute(
                    "SELECT address_type, name, line1, line2, postal_code, city, country FROM addresses WHERE customer_id = %s;",
                    (customer_id,),
                )
                addresses = [dict(r) for r in cur.fetchall()]
            result = {"customer": dict(cust), "accounts": accounts, "addresses": addresses}
            return result
    finally:
        conn.close()


@traceable(name="Get Customer by QR Name/City")
def get_customer_by_name_city(name: str, city: str | None = None) -> Optional[Dict[str, Any]]:
    conn = _get_conn()
    if conn is None:
        return None
    try:
        with conn:
            cust = _find_customer_by_name_city(conn, name, city or "")
            if not cust:
                return None
            customer_id = cust["id"]
            with conn.cursor() as cur:
                cur.execute("SELECT iban FROM accounts WHERE customer_id = %s;", (customer_id,))
                accounts = [r["iban"] for r in cur.fetchall()]
                cur.execute(
                    "SELECT address_type, name, line1, line2, postal_code, city, country FROM addresses WHERE customer_id = %s;",
                    (customer_id,),
                )
                addresses = [dict(r) for r in cur.fetchall()]
            result = {"customer": dict(cust), "accounts": accounts, "addresses": addresses}
            return result
    finally:
        conn.close()


@traceable(name="Get Customer by QR iban")
def get_customer_by_invoice(parsed_invoice: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Try to find a customer for the parsed_invoice without creating new rows.
    Returns None if no match.
    """
    iban = parsed_invoice.get("iban")
    creditor = parsed_invoice.get("creditor") or {}
    # trace will capture the parsed_invoice input and the returned value
    if iban:
        found = get_customer_by_iban(iban)
        if found:
            return found
    name = creditor.get("name")
    city = creditor.get("city")
    if name:
        found = get_customer_by_name_city(name, city)
        return found
    return None


# Explicit seeding function (call only when you want to import data)
def seed_customers_from_json(json_path: str) -> Dict[str, Any]:
    """
    Load customers from a JSON file and insert into DB.
    Expected format: [{ "name": "...", "accounts": ["IBAN..."], "addresses": [{...}, ...], "customer_prompt": "..." }, ...]
    This function now clears existing tables and seeds fresh data from the JSON.
    """
    # Ensure DB schema exists / is migrated before seeding
    try:
        init_res = init_db()
    except Exception as e:
        # If init_db raises, surface an error to caller
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
            # Wipe existing data so seeding results in a fresh DB
            with conn.cursor() as cur:
                # truncate in one statement and restart serials
                cur.execute("TRUNCATE TABLE accounts, addresses, customers RESTART IDENTITY CASCADE;")

            for item in data:
                name = item.get("name") or "unknown"
                cust_prompt = item.get("customer_prompt")
                # create customer with prompt
                cust_id = _insert_customer(conn, name, cust_prompt)
                # accounts
                for iban in item.get("accounts", []):
                    _ensure_account(conn, cust_id, iban)
                # addresses
                for addr in item.get("addresses", []):
                    _ensure_address(conn, cust_id, addr)
                inserted += 1
        return {"inserted": inserted}
    finally:
        conn.close()


def choose_prompt(customer_info: Dict[str, Any]) -> str:
    """
    Basic prompt selection based on customer metadata.
    """
    if not customer_info:
        return "default"
    addresses = customer_info.get("addresses") or []
    for a in addresses:
        if a.get("country") and a.get("country").upper() != "CH":
            return "intl_prompt"
    if len(customer_info.get("accounts", [])) > 1:
        return "multi_account_prompt"
    return "default"
