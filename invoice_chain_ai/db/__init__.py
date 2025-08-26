from __future__ import annotations
import json
from pathlib import Path
from typing import Optional

DATA_DIR = Path(__file__).parent
SEED_FILE = DATA_DIR / "seed_customers.json"


def _load_customers() -> list[dict]:
    """Load seed customers from the JSON file next to this module."""
    try:
        return json.loads(SEED_FILE.read_text(encoding="utf-8"))
    except Exception:
        return []


def get_customer_by_invoice(invoice: str) -> Optional[dict]:
    """
    Try to find a customer by matching the invoice string to known accounts (IBAN)
    or by substring match on addresses/name.
    """
    customers = _load_customers()
    inv_clean = (invoice or "").replace(" ", "")
    for c in customers:
        # accounts match (IBAN)
        for acc in c.get("accounts", []):
            if acc.replace(" ", "") in inv_clean or inv_clean in acc.replace(" ", ""):
                return c
        # fallback: name/address substring match
        name = c.get("name", "")
        if name and name.lower() in (invoice or "").lower():
            return c
        for addr in c.get("addresses", []):
            if any(
                (v and v.lower() in (invoice or "").lower())
                for v in addr.values()
                if isinstance(v, str)
            ):
                return c
    return None


def choose_prompt(customer: Optional[dict]) -> str:
    """
    Return the customer's prompt text if present; otherwise return a default prompt.
    Accepts either the customer dict or a wrapper like {"customer": {...}}.
    """
    if not customer:
        return "Extract invoice data into the provided schema. Use the document context."
    # Unwrap if passed a wrapper
    if "customer" in customer and isinstance(customer["customer"], dict):
        c = customer["customer"]
    else:
        c = customer
    prompt = c.get("customer_prompt") or c.get("prompt") or ""
    if prompt:
        return prompt
    return f"Extract invoice data for {c.get('name','the customer')} into the JSON schema."

__all__ = ["get_customer_by_invoice", "choose_prompt", "DATA_DIR", "SEED_FILE"]
