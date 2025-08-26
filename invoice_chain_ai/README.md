# Invoice Chain AI — README

## Setup

1. Create conda env (Python 3.11):

```powershell
conda env create -f environment.yml
conda activate invoice-chain-ai
```

2. Install/update Python deps:

```powershell
pip install -r requirements.txt
```

Prerequisites

- For DB operations: set DATABASE_URL in your environment (Postgres).
- For structured output (LLM): set OPENAI_API_KEY and install langchain + an OpenAI-compatible model/client.

## CLI — common commands

Note: entrypoint is invoice_chain_ai.main (module). All commands require the `--pdf` path argument.

1. Convert PDF to Markdown (docling)

```powershell
python -m invoice_chain_ai.main --pdf path/to/file.pdf --parser docling
```

2. Convert PDF to Markdown (marker) with optional LLM-assisted parsing

```powershell
python -m invoice_chain_ai.main --pdf path/to/file.pdf --parser marker --use-llm
```

3. QR-only mode (scan and write customer.json)

```powershell
python -m invoice_chain_ai.main --pdf path/to/file.pdf --qr
```

4. Parser run + structured LLM output in one step

```powershell
python -m invoice_chain_ai.main --pdf path/to/file.pdf --parser marker --use-llm --structured-output
```

5. Structured-output only (use an existing run directory)

- If you already have a run output folder (contains markdown and customer.json), run structured-output only. `--pdf` is still required (used to resolve the basename).

```powershell
python -m invoice_chain_ai.main --pdf path/to/original.pdf --structured-output --run-dir path/to/existing/run_dir
```

- The CLI will look for `<basename>.docling.md` or `<basename>.marker.md` and `customer.json` inside `--run-dir`.

## Database — init & seed

1. Initialize DB schema (runs db/init.sql or fallback DDL):

```powershell
python -c "from invoice_chain_ai.db.db_client import init_db; print(init_db())"
```

2. Seed example customers (calls init_db() then loads db/seed_customers.json)

```powershell
python -m invoice_chain_ai.db.seed
```

3. Seed from a specific JSON file:

```powershell
python -c "from invoice_chain_ai.db.db_client import seed_customers_from_json; print(seed_customers_from_json(r'c:\\path\\to\\seed_customers.json'))"
```

Important: seeding truncates customers/accounts/addresses. Back up data if needed.

## Output locations

- Default outputs are written under `invoice_chain_ai/output/<pdf_stem>_<timestamp>/` (or the `--outdir` you provide).
- Structured output is saved as `structured_output.json` inside the run directory.
- Customer lookup results are saved as `customer.json`.

## Troubleshooting

- If structured output fails: ensure OPENAI_API_KEY is set, langchain and chat model libs are installed, and network access to the model is available.
- If DB init doesn't add columns to an existing DB, run the init command (it contains ALTER TABLE IF NOT EXISTS for the customer_prompt column).
- If QR scanning misses a QR: try running parser first to generate markdown and then retry QR with heuristic (the toolchain can do this automatically when using a parser).

## Quick examples

```powershell
# Full flow: marker parsing + QR scanning + structured output
python -m invoice_chain_ai.main --pdf invoices/bkw_10300359.pdf --parser marker --use-llm --structured-output

# Only QR:
python -m invoice_chain_ai.main --pdf invoices/bkw_10300359.pdf --qr

# Structured output only using an existing run directory:
python -m invoice_chain_ai.main --pdf invoices/bkw_10300359.pdf --structured-output --run-dir ./output/bkw_10300359
```

-- End of README --
