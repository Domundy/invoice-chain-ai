import sys
import subprocess
from pathlib import Path
import argparse

ROOT = Path(__file__).resolve().parent.parent  # repo root (one level above eval/)
EVAL_FILE = Path(__file__).resolve().parent / "evaluation-paths.txt"


def read_paths(file_path: Path):
    lines = []
    for raw in file_path.read_text(encoding="utf-8").splitlines():
        s = raw.strip()
        if not s or s.startswith("#"):
            continue
        lines.append(s)
    return lines


def resolve_path(line: str):
    p = Path(line)
    if p.is_absolute():
        return p
    # try relative to repo root first, then eval folder
    cand = (ROOT / line).resolve()
    if cand.exists():
        return cand
    cand2 = (Path(__file__).resolve().parent / line).resolve()
    if cand2.exists():
        return cand2
    # fallback: normalize the path (convert ./ to correct separators)
    return (ROOT / line.lstrip("./\\")).resolve()


def run_command(cmd, cwd=None):
    print("RUN:", " ".join(map(str, cmd)))
    proc = subprocess.run(cmd, cwd=cwd)
    if proc.returncode != 0:
        print(f"-> exited with code {proc.returncode}")
    return proc.returncode


def make_run_dir_from_pdf(pdf_path: Path):
    # invoice_chain_ai/output/<parent_folder>_<basename>
    parent = pdf_path.parent.name
    basename = pdf_path.stem
    return ROOT / "invoice_chain_ai" / "output" / f"{parent}_{basename}"


def run_parser_pass(paths, parser_choice="docling"):
    # parser_choice: "docling", "marker"
    if parser_choice == "docling":
        print("=== PASS: parser=docling ===")
        for line in paths:
            pdf = resolve_path(line)
            cmd = [sys.executable, "-m", "invoice_chain_ai.main", "--pdf", str(pdf), "--parser", "docling"]
            run_command(cmd, cwd=ROOT)

    if parser_choice == "marker":
        print("\n=== PASS: parser=marker ===")
        for line in paths:
            pdf = resolve_path(line)
            cmd = [sys.executable, "-m", "invoice_chain_ai.main", "--pdf", str(pdf), "--parser", "marker" , "--use-llm"]
            run_command(cmd, cwd=ROOT)


def run_structured_output_pass(paths):
    print("=== PASS: structured-output ===")
    for line in paths:
        pdf = resolve_path(line)
        run_dir = make_run_dir_from_pdf(pdf)
        cmd = [sys.executable, "-m", "invoice_chain_ai.main", "--run-dir", str(run_dir), "--structured-output"]
        run_command(cmd, cwd=ROOT)


def parse_args():
    p = argparse.ArgumentParser(description="Run evaluation passes for invoice_chain_ai")
    p.add_argument("--parser", choices=["docling", "marker"], default=None,
                   help="Which parser pass to run (if omitted, no parser pass is run)")
    p.add_argument("--structured-output", dest="structured", action="store_true",
                   help="Run structured-output pass using --run-dir <output> --structured-output")
    p.add_argument("--pdf", type=str, default=None,
                   help="Run only this single PDF path (absolute or relative). If omitted, uses evaluation-paths.txt")
    return p.parse_args()


def main():
    args = parse_args()

    if args.pdf:
        paths = [args.pdf]
    else:
        paths = read_paths(EVAL_FILE)

    if not paths:
        print("No files found in", EVAL_FILE)
        return 1

    # Decide which passes to run
    run_parser = args.parser in ("docling", "marker")
    run_structured = args.structured

    if run_parser:
        run_parser_pass(paths, parser_choice=args.parser)

    if run_structured:
        run_structured_output_pass(paths)

    return 0


if __name__ == "__main__":
    main()