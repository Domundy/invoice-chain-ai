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

## Swiss QR Code Extraction Workflow

### Overview

This project supports automatic extraction and parsing of Swiss QR payment codes (QR-Rechnung) from PDF invoices. The workflow is as follows:

1. **PDF Input**: You provide a PDF file via the CLI.
2. **QR Extraction**: The system scans the PDF for embedded images and rendered pages.
   - For each image or rendered page, the code tries to detect a Swiss QR code using:
     - **WeChat QRCode Detector** (preferred, if model files are available)
     - **OpenCV QRCodeDetector** (fallback)
   - The first QR code starting with `SPC` is considered a Swiss payment QR code.
3. **Parsing**: If a Swiss QR code is found, its payload is parsed into a structured object (`SwissQRInvoice`) according to the Swiss Payment Standards.
4. **Output**: The raw QR code text and the parsed invoice (if parsing succeeds) are saved as a JSON file in the output directory.

### CLI Usage

```powershell
# QR-only mode (no markdown extraction)
python -m invoice_chain_ai.main --pdf path/to/file.pdf --qr

# With Markdown extraction (docling or marker)
python -m invoice_chain_ai.main --pdf path/to/file.pdf --parser docling
python -m invoice_chain_ai.main --pdf path/to/file.pdf --parser marker --use-llm
```

- Output JSON will be saved in the output directory, containing both the raw QR code and the parsed invoice data.

### Improvements & Troubleshooting

- **If QR codes can't be found:**  
  Sometimes, QR codes are not detected directly from the PDF (due to image quality, encoding, or PDF structure).

  - **Improvement:** The workflow can be extended to also scan images extracted by `marker-pdf` for QR codes. This increases the chance of detection, especially for PDFs where the QR is not embedded as a standard image.
  - If you encounter missing QR codes, consider extracting all images from the PDF (e.g., with `marker-pdf` or another tool) and running the QR scanner on those images as well.

- **Model Files for WeChat Detection:**  
  For best results, ensure the WeChat QRCode model files are present in the `WeChatQR` directory as expected by the code.

- **Output Structure:**  
  The JSON output contains:
  - `"raw_qr_text"`: The full text payload of the detected QR code.
  - `"parsed_invoice"`: The structured invoice data (if parsing was successful).

---

## CLI: PDF -> Markdown (docling oder marker-pdf)

Erster Schritt: Konvertiere ein PDF via CLI in Markdown. Engine per Flag wählen, Ausgabe landet in ./output/<pdfname>.<engine>.md.

```powershell
# docling
python .\main.py --engine docling --pdf .\pfad\zu\rechnung.pdf

# marker-pdf
python .\main.py --engine marker --pdf .\pfad\zu\rechnung.pdf --outdir .\output
```

Hinweise:

- Die Konvertierungsfunktionen in main.py sind als TODO markiert.
- Implementiere sie entweder über die jeweilige Python API oder über die CLI-Tools (falls verfügbar).
- Der Output-Filename folgt dem Schema: <basename>.<engine>.md

## Database: Viewing & Initialization

Kurz:

- Du kannst die lokale Postgres-DB in VS Code mit einer Postgres-Extension (z. B. "PostgreSQL" oder "SQLTools" + Postgres-Driver) ansehen.
- Schema-Erzeugung und Seeding erfolgen per Skript im Projekt: die Initialisierung (Schema) und das Einspielen der Beispieldaten sind per Kommando ausführbar.

Empfohlene VS Code Optionen

- Extension: Suche im VS Code Marketplace nach `PostgreSQL` oder `SQLTools` (SQLTools benötigt zusätzlichen Postgres-Driver).
- Verbindung anlegen: In der Extension eine neue Connection anlegen — du kannst die vollständige CONNECTION STRING (DATABASE_URL) benutzen oder Host/Port/DB/User/Password einzeln eintragen.
- Nach Verbindung: Rechtsklick auf die DB → New Query / Explorer öffnen → SQL ausführen.

Beispiele (Terminal)

1. Starte Postgres (Docker, Postgres 17):

- Bash / macOS / Linux:
  docker run --rm -e POSTGRES_USER=invoice_user -e POSTGRES_PASSWORD=secret -e POSTGRES_DB=invoice_db -p 5432:5432 --name invoice-db -d postgres:17
- PowerShell:
  docker run --rm -e POSTGRES_USER=invoice_user -e POSTGRES_PASSWORD=secret -e POSTGRES_DB=invoice_db -p 5432:5432 --name invoice-db -d postgres:17

2. Setze DATABASE_URL (Beispiel)

- Bash:
  export DATABASE_URL="postgresql://invoice_user:secret@localhost:5432/invoice_db"
- PowerShell:
  $env:DATABASE_URL="postgresql://invoice_user:secret@localhost:5432/invoice_db"

3. Abhängigkeiten installieren (falls noch nicht):

- pip install -r requirements.txt
  (wichtig: `psycopg[binary]` muss installiert sein für DB-Zugriff)

4. DB-Schema initialisieren (nur Schema) — optional:

- Python-Einzeiler:
  python -c "from invoice_chain_ai.db.db_client import init_db; print(init_db())"

5. Schema + Seed (fügt Beispielkunden aus db/seed_customers.json ein):

- Verwende das Projekt-seed-Skript:
  python -m invoice_chain_ai.db.seed
  (Dieses Skript ruft init_db() und anschließend `seed_customers.json` ein; nur ausführen, wenn du wirklich Einträge anlegen willst.)

Wichtig

- Die Anwendung selbst führt nur Lookups durch (keine Inserts) — Inserts passieren nur, wenn du bewusst `db.seed` ausführst.
- Nutze in VS Code die Connection String aus deiner `.env` bzw. die gleichen Credentials, die du beim Docker-Start gesetzt hast.
- Für schnelle CLI-Checks kannst du auch `psql` verwenden:
  psql "postgresql://invoice_user:secret@localhost:5432/invoice_db"
