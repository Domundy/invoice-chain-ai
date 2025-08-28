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


# Export commonly used helpers from db_client for package-level imports
from .db_client import (
    get_customer_by_iban,
    get_customer_by_invoice,
    choose_prompt,
    init_db,
    seed_customers_from_json,
)

# Simple CLI utility to avoid an empty `if __name__ == "__main__":` block
if __name__ == "__main__":
    import sys
    # Usage:
    #   python -m invoice_chain_ai.db init
    #   python -m invoice_chain_ai.db seed <json_path>
    if len(sys.argv) >= 2 and sys.argv[1] == "init":
        print(init_db())
    elif len(sys.argv) >= 3 and sys.argv[1] == "seed":
        print(seed_customers_from_json(sys.argv[2]))
    else:
        print("Usage: python -m invoice_chain_ai.db init | seed <json_path>")