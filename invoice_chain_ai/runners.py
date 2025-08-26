from __future__ import annotations
import json
import sys
from pathlib import Path
from typing import Optional

from langchain_core.runnables import RunnableLambda
from langchain_core.tracers import ConsoleCallbackHandler
from langsmith import traceable

from .parsers import convert_pdf_to_markdown
from .qr import scan_qr_code
from .db import get_customer_by_invoice, choose_prompt
from .io_utils import write_markdown
from .structured_output import run_structured_output_modern

handler = ConsoleCallbackHandler()

@traceable(name="Scan QR Code")
def scan_qr_trace(pdf_path: Path, run_dir: Path, use_heuristic: bool = False):
    qr_result = scan_qr_code(pdf_path, run_dir, use_heuristic=use_heuristic)
    return {"qr_result": qr_result}

@traceable(name="Convert PDF to Markdown")
def convert_pdf_trace(pdf_path: Path, engine: str, use_llm: bool, output_dir: Path):
    md = convert_pdf_to_markdown(pdf_path, engine, use_llm=use_llm, output_dir=output_dir)
    return {"engine": engine, "markdown": md}

# New helper: normalize the 'invoice' payload (may be a dict or string) into a searchable string
def _normalize_invoice_field(inv) -> str:
    """
    Accepts the invoice field returned by the QR parser (could be str or dict).
    Returns a string suitable for get_customer_by_invoice (IBAN or name/city fallback).
    """
    if inv is None:
        return ""
    if isinstance(inv, str):
        return inv
    # dict-like: prefer explicit iban
    if isinstance(inv, dict):
        iban = inv.get("iban") or inv.get("IBAN") or inv.get("account")
        if iban:
            return str(iban)
        # creditor block
        creditor = inv.get("creditor") or {}
        if isinstance(creditor, dict):
            name = creditor.get("name") or creditor.get("company") or ""
            city = creditor.get("city") or creditor.get("town") or ""
            combined = " ".join([p for p in [name, city] if p])
            if combined:
                return combined
        # fallback to JSON string
        try:
            return json.dumps(inv, ensure_ascii=False)
        except Exception:
            return str(inv)
    # other types
    return str(inv)

def run_processing(copied_pdf: Optional[Path], parser_name: str | None, use_llm: bool, qr_only: bool, run_dir: Path, structured_output_flag: bool = False) -> int:
    try:
        # Structured-output-only mode (no parser requested)
        if structured_output_flag and parser_name is None:
            # Look for markdown inside run_dir (prefer docling, then marker)
            md_candidates = list(run_dir.glob("*.docling.md")) + list(run_dir.glob("*.marker.md"))
            if not md_candidates:
                print(f"Error: no markdown (.docling.md or .marker.md) found in {run_dir}", file=sys.stderr)
                return 2
            md_path = md_candidates[0]

            customer_json_path = run_dir / "customer.json"
            if not customer_json_path.exists():
                print(f"Error: customer.json not found in run directory {run_dir}", file=sys.stderr)
                return 2

            try:
                cust = json.loads(customer_json_path.read_text(encoding="utf-8"))
                customer_prompt = choose_prompt(cust)
            except Exception as e:
                print(f"Error: could not read/parse customer.json: {e}", file=sys.stderr)
                return 2

            try:
                structured_result = run_structured_output_modern(md_path, customer_prompt, run_dir)
                so_out = run_dir / "structured_output.json"
                so_out.write_text(json.dumps(structured_result, ensure_ascii=False, indent=4), encoding="utf-8")
                print(f"Wrote structured output: {so_out}")
                return 0
            except Exception as e:
                print(f"❌ Structured output step failed: {e}", file=sys.stderr)
                return 4

        # From here, require a copied_pdf for the usual flows
        if copied_pdf is None:
            print("Error: PDF path is required for parsing/QR operations.", file=sys.stderr)
            return 2

        # QR-only mode (explicit: no heuristic)
        if qr_only and parser_name is None:
            qr_runnable = RunnableLambda(lambda _: scan_qr_trace(copied_pdf, run_dir, use_heuristic=False), name="QR Scanner")
            # invoke synchronously, serial execution ensured by sequential invoke calls
            result = qr_runnable.invoke(None, config={"callbacks": [handler]})
            qr_info = result.get("qr_result") if isinstance(result, dict) else None
            if qr_info and isinstance(qr_info, dict) and qr_info.get("invoice"):
                search_val = _normalize_invoice_field(qr_info["invoice"])
                cust = get_customer_by_invoice(search_val)
                if not cust:
                    print("Error: customer not found by IBAN or address. Aborting.", file=sys.stderr)
                    return 5
                cust_out = run_dir / "customer.json"
                cust_out.write_text(json.dumps(cust, ensure_ascii=False, indent=4), encoding="utf-8")
                prompt_key = choose_prompt(cust)
                print(f"Selected prompt: {prompt_key}")
            return 0 if result and result.get("qr_result") is not None else 1

        # Single parser modes: run parser first, write markdown, then QR (with heuristic fallback)
        if parser_name in ["docling", "marker"]:
            parser_runnable = RunnableLambda(lambda _: convert_pdf_trace(copied_pdf, parser_name, use_llm, run_dir), name=f"{parser_name.capitalize()} Parser")
            # run parser synchronously
            parser_result = parser_runnable.invoke(None, config={"callbacks": [handler]})

            # Write markdown output (required for heuristic fallback)
            try:
                markdown = parser_result["markdown"]
                written = write_markdown(run_dir, copied_pdf.stem, parser_name, markdown)
                print(f"Wrote: {written}")
                print(f"✅ {parser_name} conversion completed")
            except Exception as e:
                print(f"❌ {parser_name} conversion failed: {e}", file=sys.stderr)
                return 4

            # Now run QR scan (no heuristic first)
            qr_runnable = RunnableLambda(lambda _: scan_qr_trace(copied_pdf, run_dir, use_heuristic=False), name="QR Scanner")
            qr_result = qr_runnable.invoke(None, config={"callbacks": [handler]})

            # If no QR found, retry with heuristic (uses written markdown)
            if qr_result.get("qr_result") is None:
                print("No Swiss QR code found. Retrying with heuristic from markdown...")
                qr_runnable_h = RunnableLambda(lambda _: scan_qr_trace(copied_pdf, run_dir, use_heuristic=True), name="QR Scanner (heuristic)")
                qr_result = qr_runnable_h.invoke(None, config={"callbacks": [handler]})

            # Handle QR result
            if qr_result.get("qr_result") is None:
                print("No Swiss QR code found.")
            else:
                print("✅ QR code extraction completed")
                qr_info = qr_result.get("qr_result")
                if isinstance(qr_info, dict) and qr_info.get("invoice"):
                    search_val = _normalize_invoice_field(qr_info["invoice"])
                    cust = get_customer_by_invoice(search_val)
                    if not cust:
                        print("Error: customer not found by IBAN or address. Aborting.", file=sys.stderr)
                        return 5
                    cust_out = run_dir / "customer.json"
                    cust_out.write_text(json.dumps(cust, ensure_ascii=False, indent=4), encoding="utf-8")
                    prompt_key = choose_prompt(cust)
                    print(f"Selected prompt: {prompt_key}")

            # At this point QR may have been extracted and customer.json may exist
            # If user requested structured output, run LLM-based structured extraction using customer prompt + markdown
            if structured_output_flag:
                customer_json_path = run_dir / "customer.json"
                # fetch customer prompt via db.choose_prompt if customer found; fallback to generic prompt
                customer_prompt = None
                if customer_json_path.exists():
                    try:
                        cust = json.loads(customer_json_path.read_text(encoding="utf-8"))
                        customer_prompt = choose_prompt(cust)  # choose_prompt returns prompt text (see db.py)
                    except Exception as e:
                        print(f"Warning: could not read customer.json for structured output: {e}", file=sys.stderr)
                else:
                    print("No customer.json found; structured output will use default/empty customer prompt.")

                # run structured output: use the markdown file we wrote as context
                try:
                    # written is the path returned from write_markdown (string or Path)
                    md_path = Path(written)
                    structured_result = run_structured_output_modern(md_path, customer_prompt, run_dir)
                    so_out = run_dir / "structured_output.json"
                    so_out.write_text(json.dumps(structured_result, ensure_ascii=False, indent=4), encoding="utf-8")
                    print(f"Wrote structured output: {so_out}")
                except Exception as e:
                    print(f"❌ Structured output step failed: {e}", file=sys.stderr)
                    # don't fail the whole run for structured-output failure; continue
            return 0

        # 'all' engines - run parsers first, then QR (with heuristic fallback)
        if parser_name == "all":
            print("Running all parsers sequentially to avoid model conflicts...")
            docling_runnable = RunnableLambda(lambda _: convert_pdf_trace(copied_pdf, "docling", False, run_dir), name="Docling Parser")
            marker_runnable = RunnableLambda(lambda _: convert_pdf_trace(copied_pdf, "marker", use_llm, run_dir), name="Marker Parser")

            results = {}
            errors: list[tuple[str, Exception]] = []

            # 1. Docling
            print("1/3: Running Docling conversion...")
            try:
                docling_result = docling_runnable.invoke(None, config={"callbacks": [handler]})
                results["docling"] = docling_result
                print("✅ Docling conversion completed")
            except Exception as e:
                print(f"❌ Docling conversion failed: {e}")
                errors.append(("docling", e))

            # 2. Marker
            print("2/3: Running Marker conversion...")
            try:
                marker_result = marker_runnable.invoke(None, config={"callbacks": [handler]})
                results["marker"] = marker_result
                print("✅ Marker conversion completed")
            except Exception as e:
                print(f"❌ Marker conversion failed: {e}")
                errors.append(("marker", e))

            # write any markdown outputs so heuristic can use them
            outputs = {}
            if "docling" in results:
                try:
                    docling_md = results["docling"]["markdown"]
                    written = write_markdown(run_dir, copied_pdf.stem, "docling", docling_md)
                    print(f"Wrote: {written}")
                    outputs["docling"] = docling_md
                except Exception as e:
                    errors.append(("docling_output", e))

            if "marker" in results:
                try:
                    marker_md = results["marker"]["markdown"]
                    written = write_markdown(run_dir, copied_pdf.stem, "marker", marker_md)
                    print(f"Wrote: {written}")
                    outputs["marker"] = marker_md
                except Exception as e:
                    errors.append(("marker_output", e))

            # 3. QR (try without heuristic first)
            print("3/3: Scanning QR code...")
            qr_runnable = RunnableLambda(lambda _: scan_qr_trace(copied_pdf, run_dir, use_heuristic=False), name="QR Scanner")
            try:
                qr_result = qr_runnable.invoke(None, config={"callbacks": [handler]})
            except Exception as e:
                print(f"❌ QR scanning failed: {e}")
                errors.append(("qr", e))
                qr_result = {"qr_result": None}

            # If no QR, retry with heuristic (markdown available)
            if qr_result.get("qr_result") is None:
                print("No QR found; retrying with heuristic based on generated markdown...")
                qr_runnable_h = RunnableLambda(lambda _: scan_qr_trace(copied_pdf, run_dir, use_heuristic=True), name="QR Scanner (heuristic)")
                try:
                    qr_result = qr_runnable_h.invoke(None, config={"callbacks": [handler]})
                except Exception as e:
                    print(f"❌ QR heuristic scan failed: {e}")
                    errors.append(("qr_heuristic", e))
                    qr_result = {"qr_result": None}

            if qr_result.get("qr_result") is None:
                print("No Swiss QR code found.")
            else:
                outputs["qr"] = qr_result["qr_result"]
                if isinstance(outputs["qr"], dict) and outputs["qr"].get("invoice"):
                    search_val = _normalize_invoice_field(outputs["qr"]["invoice"])
                    cust = get_customer_by_invoice(search_val)
                    if not cust:
                        print("Error: customer not found by IBAN or address. Aborting.", file=sys.stderr)
                        return 5
                    cust_out = run_dir / "customer.json"
                    cust_out.write_text(json.dumps(cust, ensure_ascii=False, indent=4), encoding="utf-8")
                    prompt_key = choose_prompt(cust)
                    print(f"Selected prompt: {prompt_key}")

            out_json = run_dir / "run_output.json"
            out_json.write_text(json.dumps(outputs, ensure_ascii=False, indent=4), encoding="utf-8")
            print(f"Wrote structured output: {out_json}")

            if errors:
                print(f"\n⚠️  {len(errors)} error(s) occurred:")
                for eng, err in errors:
                    print(f"  • {eng}: {err}", file=sys.stderr)
                if len(outputs) > len(errors):
                    print("✅ At least one conversion succeeded")
                    return 0
                else:
                    print("❌ All conversions failed")
                    return 4

            print("✅ All conversions completed successfully")
            return 0

        print(f"Unknown parser option: {parser_name}", file=sys.stderr)
        return 2

    except NotImplementedError as e:
        print(f"{e}\n\nPlease implement the conversion function.", file=sys.stderr)
        return 3
    except Exception as e:
        print(f"Conversion failed: {e}", file=sys.stderr)
        return 4
