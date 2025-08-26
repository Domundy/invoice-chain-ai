from __future__ import annotations
import argparse
import textwrap
import sys
from pathlib import Path
from dotenv import load_dotenv

from .io_utils import unique_outdir, copy_pdf_to_run
from . import runners

def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="invoice-chain-ai",
        description="Convert a PDF to Markdown (docling or marker) and extract Swiss QR.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """
            Examples:
              python -m invoice_chain_ai.main --pdf path/to/file.pdf --parser docling
              python -m invoice_chain_ai.main --pdf path/to/file.pdf --parser marker --use-llm
                            
            """
        ),
    )
    parser.add_argument("--pdf", required=False, type=Path, default=None, help="Path to the input PDF. Optional when using --structured-output with --run-dir.")
    parser.add_argument(
        "--parser",
        choices=["docling", "marker"],  # removed "all"
        required=False,
        default=None,
        help="Parser to use. Required unless --qr is provided. (docling or marker)",
    )
    parser.add_argument(
        "--outdir",
        default=Path(__file__).parent / "output",
        type=Path,
        help="Directory to write outputs. A subfolder per run is created inside.",
    )
    parser.add_argument(
        "--use-llm",
        action="store_true",
        help="Only relevant for marker: enable LLM-assisted parsing (requires OPENAI_API_KEY).",
    )
    parser.add_argument(
        "--qr",
        action="store_true",
        help="QR-only mode: scan Swiss QR and write JSON; can be used with --parser or alone.",
    )
    parser.add_argument(
        "--structured-output",
        action="store_true",
        help="Invoke LLM to produce structured output (uses customer prompt + generated markdown).",
    )
    parser.add_argument(
        "--run-dir",
        default=None,
        type=Path,
        help="Optional existing run directory to use for --structured-output only runs.",
    )
    return parser

def run_cli(argv: list[str] | None = None) -> int:
    # load dotenv here as well (safe no-op if already loaded)
    load_dotenv()

    parser = _build_parser()
    args = parser.parse_args(argv)

    pdf_path: Path | None = args.pdf
    parser_name: str | None = args.parser
    outdir: Path = args.outdir
    use_llm: bool = bool(args.use_llm)
    qr_only: bool = bool(args.qr)
    structured_output: bool = bool(args.structured_output)
    provided_run_dir: Path | None = args.run_dir

    if parser_name == "docling" and use_llm:
        print("Note: --use-llm is ignored for 'docling'.", file=sys.stderr)

    # If no run-dir provided, require --pdf
    if provided_run_dir is None:
        if pdf_path is None:
            print("Error: --pdf is required unless running --structured-output with --run-dir.", file=sys.stderr)
            return 2
        if not pdf_path.exists():
            print(f"Error: PDF not found: {pdf_path}", file=sys.stderr)
            return 2
        if pdf_path.suffix.lower() != ".pdf":
            print(f"Error: Not a PDF file: {pdf_path}", file=sys.stderr)
            return 2
    else:
        # run-dir provided: allow missing pdf only if structured-output requested
        if pdf_path is None and not structured_output:
            print("Error: --pdf is required for non-structured-output runs even when --run-dir is provided.", file=sys.stderr)
            return 2

    # require parser unless qr-only or structured-output is requested
    if not qr_only and parser_name is None and not structured_output:
        print("Error: please choose --parser {docling,marker} or use --qr for QR-only. Use --structured-output to run only the structured output step.", file=sys.stderr)
        return 2

    outdir.mkdir(parents=True, exist_ok=True)

    # If user provided an existing run directory (for structured-output-only), use it.
    if provided_run_dir:
        run_dir = provided_run_dir
        if not run_dir.exists() or not run_dir.is_dir():
            print(f"Error: provided run directory does not exist: {run_dir}", file=sys.stderr)
            return 2
    else:
        run_dir = unique_outdir(outdir, pdf_path)  # pdf_path is not None here
        run_dir.mkdir(parents=True, exist_ok=False)

    # Only copy PDF when we have one and we're creating a new run dir
    if pdf_path is not None and provided_run_dir is None:
        try:
            copied_pdf = copy_pdf_to_run(pdf_path, run_dir)
        except Exception as e:
            print(f"Warning: could not copy original PDF: {e}", file=sys.stderr)
            copied_pdf = pdf_path  # fallback, still proceed
    else:
        # structured-output-only with --run-dir: no copied_pdf available
        copied_pdf = None

    # Delegate processing to runners module
    return runners.run_processing(copied_pdf, parser_name, use_llm, qr_only, run_dir, structured_output)
