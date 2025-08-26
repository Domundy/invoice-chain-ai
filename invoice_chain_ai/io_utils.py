from __future__ import annotations
from pathlib import Path
import shutil
import re
from typing import Optional

def unique_outdir(base_outdir: Path, pdf_path: Path) -> Path:
    # Use parent folder name and PDF stem for output folder
    parent_name = pdf_path.parent.name
    pdf_stem = pdf_path.stem
    folder_name = f"{parent_name}_{pdf_stem}"
    candidate = base_outdir / folder_name
    if not candidate.exists():
        return candidate
    i = 2
    while True:
        candidate = base_outdir / f"{folder_name}_{i}"
        if not candidate.exists():
            return candidate
        i += 1

def copy_pdf_to_run(pdf_path: Path, run_dir: Path) -> Path:
    dest = run_dir / pdf_path.name
    try:
        shutil.copy2(pdf_path, dest)
    except Exception:
        # Keep original error handling in callers if needed
        raise
    return dest

def write_markdown(run_dir: Path, pdf_stem: str, engine: str, markdown: str) -> Path:
    out_file = run_dir / f"{pdf_stem}.{engine}.md"
    out_file.write_text(markdown, encoding="utf-8")
    return out_file

# New: heuristic IBAN extraction from markdown files in an output folder
def find_iban_in_markdown(output_dir: Path) -> Optional[str]:
    """
    Scan markdown files in output_dir for a Swiss IBAN. Returns normalized IBAN (no spaces)
    if found, otherwise None. Handles IBANs with or without spaces and common markdown noise.
    """
    if not output_dir.exists() or not output_dir.is_dir():
        return None

    # Look for possible IBAN-like snippets in .md files
    md_files = list(output_dir.glob("*.md"))
    if not md_files:
        return None

    # Rough regex to find CH + 2 digits plus following characters (allow spaces)
    # We'll normalize and validate length afterwards.
    pattern = re.compile(r"\bCH[\s\dA-Za-z]{10,30}\b", flags=re.IGNORECASE)

    for md in md_files:
        try:
            text = md.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for m in pattern.findall(text):
            # Normalize: remove non-alphanumeric characters and uppercase
            clean = re.sub(r"[^A-Za-z0-9]", "", m).upper()
            # Validate Swiss IBAN length (Switzerland total IBAN length is 21 characters)
            if not clean.startswith("CH"):
                continue
            if len(clean) == 21 and clean[2:4].isdigit():
                # Found a plausible Swiss IBAN
                return clean
            # Some OCR or input errors produce grouped digits; as a fallback,
            # if result contains many digits and length close to expected, accept.
            if len(clean) >= 19 and len(clean) <= 25 and clean[2:4].isdigit():
                return clean
    # No IBAN found
    return None
