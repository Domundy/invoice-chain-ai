import sys
from pathlib import Path
from dotenv import load_dotenv

# Load .env so DATABASE_URL (etc.) is available to db_client
load_dotenv()

from .db_client import seed_customers_from_json, init_db

def main(seed_path=None):
    init_db()  # ensure schema exists
    seed_file = seed_path or (Path(__file__).parent / "seed_customers.json")
    res = seed_customers_from_json(str(seed_file))
    print(res)

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
