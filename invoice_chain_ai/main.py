from __future__ import annotations

# Suppress pydantic "conflict with protected namespace 'model_'" UserWarnings emitted
# by third-party libraries during import. This is safe to do if you cannot change
# the third-party models. It only hides the warnings; it does not change behavior.
import warnings
warnings.filterwarnings(
    "ignore",
    category=UserWarning,
    message=r'.*has conflict with protected namespace "model_".*',
)

from dotenv import load_dotenv

load_dotenv()

try:
    from .db.db_client import (
        init_db,
        get_customer_by_invoice,
        get_customer_by_iban,
        get_customer_by_name_city,
        seed_customers_from_json,
        choose_prompt,
    )
except Exception:
    # Fallbacks when db package or psycopg isn't available
    def init_db():
        return {"status": "noop", "reason": "db package not available"}

    def get_customer_by_invoice(_):
        return None

    def get_customer_by_iban(_):
        return None

    def get_customer_by_name_city(_, __=None):
        return None

    def seed_customers_from_json(_):
        return {"error": "db package not available"}

    def choose_prompt(_):
        return "default"

from .cli import run_cli

# New imports
import os
from pathlib import Path

# Try to import helpers; keep fallbacks if unavailable
try:
	from .io_utils import unique_outdir, copy_pdf_to_run
	from .qr import scan_qr_code
except Exception:
	unique_outdir = None
	copy_pdf_to_run = None
	scan_qr_code = None

def _get_parser_option(argv: list[str]) -> str | None:
	"""Extract --parser value support '--parser value' and '--parser=value'"""
	if not argv:
		return None
	i = 0
	while i < len(argv):
		t = argv[i]
		if t.startswith("--parser="):
			return t.split("=", 1)[1].lower()
		if t == "--parser" and i + 1 < len(argv):
			return str(argv[i + 1]).lower()
		i += 1
	return None

def main(argv: list[str] | None = None) -> int:
	# First: run the CLI (this should perform PDF -> markdown extraction if CLI is used that way)
	exit_code = run_cli(argv)

	# Decide if heuristic fallback is allowed based on argv
	allowed_parsers = {"marker", "docling", "all"}
	parser_opt = _get_parser_option(argv or [])
	use_heuristic = False
	if parser_opt and parser_opt in allowed_parsers:
		use_heuristic = True
	if argv and "--qr" in argv:
		# explicit --qr also enables heuristic fallback per request
		use_heuristic = True

	# Then: if a PDF path was supplied as the first positional arg, run the QR scanner
	try:
		if argv and len(argv) > 0:
			first = argv[0]
			pdf_path = Path(first)
			if pdf_path.exists() and pdf_path.suffix.lower() == ".pdf" and unique_outdir and copy_pdf_to_run and scan_qr_code:
				# Determine base output dir from env or default
				base_out = Path(os.environ.get("OUTPUT_DIR", "./runs"))
				run_dir = unique_outdir(base_out, pdf_path)
				run_dir.mkdir(parents=True, exist_ok=True)
				copied = copy_pdf_to_run(pdf_path, run_dir)
				# Call QR scanner (pass whether heuristic fallback should be used)
				try:
					result = scan_qr_code(copied, run_dir, use_heuristic=use_heuristic)
					print("QR scan result:", result)
				except Exception as e:
					print("QR scanning failed:", e)
	except Exception:
		# Do not fail the whole process if post-processing is not possible
		pass

	return exit_code

if __name__ == "__main__":
	raise SystemExit(main())