# invoice-chain-ai

Conda:

1. conda env create -f environment.yml
2. conda activate invoice-chain-ai
3. pip install -r requirements.txt

DB:

1. docker compose up
2. python -m invoice_chain_ai.db.seed

Commands:
Parser + LLM (only for marker) + QR detection
python -m invoice_chain_ai.main --pdf .\training_data\sig\10300992.pdf --parser marker --use-llm
python -m invoice_chain_ai.main --pdf .\training_data\sig\10300992.pdf --parser docling

QR only:
python -m invoice_chain_ai.main --pdf .\training_data\sig\10300992.pdf --qr
