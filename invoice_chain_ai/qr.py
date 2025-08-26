from __future__ import annotations
from pathlib import Path
from typing import Optional, List, Tuple, Dict, Any
import io
import json
import os
from dataclasses import dataclass, asdict
from decimal import Decimal

import fitz  # PyMuPDF
from PIL import Image, ImageEnhance, ImageOps
from langsmith import traceable

try:
    import numpy as np
except Exception:
    np = None

try:
    import cv2

    try:
        from cv2 import wechat_qrcode

        WECHAT_AVAILABLE = True
    except Exception:
        wechat_qrcode = None
        WECHAT_AVAILABLE = False
except Exception:
    cv2 = None
    wechat_qrcode = None
    WECHAT_AVAILABLE = False


WECHAT_DETECTOR_PATH = str(Path(__file__).parent / "WeChatQR" / "detect.prototxt")
WECHAT_DETECTOR_MODEL = str(Path(__file__).parent / "WeChatQR" / "detect.caffemodel")
WECHAT_SR_PATH = str(Path(__file__).parent / "WeChatQR" / "sr.prototxt")
WECHAT_SR_MODEL = str(Path(__file__).parent / "WeChatQR" / "sr.caffemodel")


@dataclass
class SwissQRAddress:
    """Swiss QR Code Address structure"""

    address_type: str  # 'S' for structured, 'K' for combined
    name: str
    address_line_1: str = ""
    address_line_2: str = ""
    postal_code: str = ""
    city: str = ""
    country: str = ""

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SwissQRInvoice:
    """Swiss QR Invoice data structure according to Swiss Payment Standards"""

    # Header
    qr_type: str  # Should be "SPC"
    version: str  # Version (e.g., "0200")
    coding_type: str  # Character set (1 = UTF-8)

    # Creditor Account Information
    iban: str

    # Creditor
    creditor: SwissQRAddress

    # Ultimate Creditor (optional)
    ultimate_creditor: Optional[SwissQRAddress] = None

    # Payment Amount Information
    amount: Optional[str] = None  # Amount as string to preserve precision
    currency: str = "CHF"

    # Ultimate Debtor
    ultimate_debtor: Optional[SwissQRAddress] = None

    # Payment Reference
    reference_type: str = ""  # QRR, SCOR, NON
    reference: str = ""

    # Additional Information
    unstructured_message: str = ""
    trailer: str = "EPD"  # End Payment Data

    # Alternative Schemes (optional)
    alternative_scheme_1: str = ""
    alternative_scheme_2: str = ""

    def as_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        # Convert nested dataclasses
        if self.creditor:
            result["creditor"] = self.creditor.as_dict()
        if self.ultimate_creditor:
            result["ultimate_creditor"] = self.ultimate_creditor.as_dict()
        if self.ultimate_debtor:
            result["ultimate_debtor"] = self.ultimate_debtor.as_dict()
        return result


@traceable(name="Parse Swiss QR Address")
def parse_address(
    fields: List[str], start_idx: int
) -> Tuple[Optional[SwissQRAddress], int]:
    """Parse address fields from QR data"""
    if start_idx >= len(fields):
        return None, start_idx

    address_type = fields[start_idx] if start_idx < len(fields) else ""

    if not address_type:
        return None, start_idx + 7  # Skip 7 empty fields

    name = fields[start_idx + 1] if start_idx + 1 < len(fields) else ""

    if address_type == "S":  # Structured address
        address_line_1 = fields[start_idx + 2] if start_idx + 2 < len(fields) else ""
        address_line_2 = fields[start_idx + 3] if start_idx + 3 < len(fields) else ""
        postal_code = fields[start_idx + 4] if start_idx + 4 < len(fields) else ""
        city = fields[start_idx + 5] if start_idx + 5 < len(fields) else ""
        country = fields[start_idx + 6] if start_idx + 6 < len(fields) else ""

        return (
            SwissQRAddress(
                address_type=address_type,
                name=name,
                address_line_1=address_line_1,
                address_line_2=address_line_2,
                postal_code=postal_code,
                city=city,
                country=country,
            ),
            start_idx + 7,
        )

    elif address_type == "K":  # Combined address
        address_line_1 = fields[start_idx + 2] if start_idx + 2 < len(fields) else ""
        address_line_2 = fields[start_idx + 3] if start_idx + 3 < len(fields) else ""
        # For combined addresses, fields 4-6 are empty
        country = fields[start_idx + 6] if start_idx + 6 < len(fields) else ""

        return (
            SwissQRAddress(
                address_type=address_type,
                name=name,
                address_line_1=address_line_1,
                address_line_2=address_line_2,
                country=country,
            ),
            start_idx + 7,
        )

    # Empty address - skip 7 fields
    return None, start_idx + 7


@traceable(name="Parse Swiss QR Invoice")
def parse_swiss_qr(qr_text: str) -> SwissQRInvoice:
    """Parse Swiss QR Code text into structured SwissQRInvoice object"""
    if not qr_text or not qr_text.startswith("SPC"):
        raise ValueError("Invalid Swiss QR Code format")

    # Split by line breaks and filter out empty lines at the end
    lines = qr_text.strip().split("\n")
    fields = [line.strip() for line in lines]

    # Ensure we have minimum required fields (at least 31 fields for basic structure)
    while len(fields) < 35:  # Pad with empty strings if needed
        fields.append("")

    try:
        # Parse header (fields 0-2)
        qr_type = fields[0]  # SPC
        version = fields[1]  # 0200
        coding_type = fields[2]  # 1 (UTF-8)

        # Parse creditor account (field 3)
        iban = fields[3]

        # Parse creditor address (fields 4-10)
        creditor, next_idx = parse_address(fields, 4)

        # Parse ultimate creditor (fields 11-17)
        ultimate_creditor, next_idx = parse_address(fields, 11)

        # Parse payment amount information (fields 18-19)
        amount = fields[18] if fields[18] else None
        currency = fields[19] if fields[19] else "CHF"

        # Parse ultimate debtor (fields 20-26)
        ultimate_debtor, next_idx = parse_address(fields, 20)

        # Parse payment reference (fields 27-28)
        reference_type = fields[27] if len(fields) > 27 else ""
        reference = fields[28] if len(fields) > 28 else ""

        # Parse additional information (field 29)
        unstructured_message = fields[29] if len(fields) > 29 else ""

        # Parse trailer (field 30)
        trailer = fields[30] if len(fields) > 30 else "EPD"

        # Parse alternative schemes (fields 31-32, optional)
        alternative_scheme_1 = fields[31] if len(fields) > 31 else ""
        alternative_scheme_2 = fields[32] if len(fields) > 32 else ""

        return SwissQRInvoice(
            qr_type=qr_type,
            version=version,
            coding_type=coding_type,
            iban=iban,
            creditor=creditor,
            ultimate_creditor=ultimate_creditor,
            amount=amount,
            currency=currency,
            ultimate_debtor=ultimate_debtor,
            reference_type=reference_type,
            reference=reference,
            unstructured_message=unstructured_message,
            trailer=trailer,
            alternative_scheme_1=alternative_scheme_1,
            alternative_scheme_2=alternative_scheme_2,
        )

    except (IndexError, ValueError) as e:
        raise ValueError(f"Failed to parse Swiss QR Code: {e}")

def preprocess_image(image: Image.Image) -> Image.Image:
    image = ImageOps.grayscale(image)
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)
    image = image.resize((image.width * 2, image.height * 2), Image.LANCZOS)
    return image


def _pil_from_pixmap(pix):
    """Convert PyMuPDF Pixmap to PIL Image"""
    if pix.n - pix.alpha < 4:  # GRAY or RGB
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    else:  # CMYK
        img = Image.frombytes("CMYK", [pix.width, pix.height], pix.samples)
    return img

def _wechat_decode(img: Image.Image) -> Optional[str]:
    if not WECHAT_AVAILABLE or cv2 is None or wechat_qrcode is None:
        return None
    import os

    if not (
        os.path.exists(WECHAT_DETECTOR_PATH)
        and os.path.exists(WECHAT_DETECTOR_MODEL)
        and os.path.exists(WECHAT_SR_PATH)
        and os.path.exists(WECHAT_SR_MODEL)
    ):
        return None
    try:
        arr = np.array(img.convert("RGB")) if np is not None else None
        if arr is None:
            return None
        detector = wechat_qrcode.WeChatQRCode(
            WECHAT_DETECTOR_PATH,
            WECHAT_DETECTOR_MODEL,
            WECHAT_SR_PATH,
            WECHAT_SR_MODEL,
        )
        res, _ = detector.detectAndDecode(arr)
        if res:
            # Only return the first valid QR and do not print here
            for txt in res:
                if isinstance(txt, str) and txt.strip() and txt.startswith("SPC"):
                    return txt
    except Exception:
        return None
    return None

def _opencv_decode(img: Image.Image) -> Optional[str]:
    if cv2 is None:
        return None
    try:
        arr = np.array(img.convert("RGB"))[:, :, ::-1] if np is not None else None
        if arr is None:
            return None
        detector = cv2.QRCodeDetector()
        try:
            ok, texts, points, _ = detector.detectAndDecodeMulti(arr)
            if ok and texts is not None:
                for t in texts:
                    if isinstance(t, str) and t.strip() and t.startswith("SPC"):
                        return t
        except Exception:
            pass
        try:
            text, points, _ = detector.detectAndDecode(arr)
            if text and text.strip() and text.startswith("SPC"):
                return text
        except Exception:
            pass
    except Exception:
        return None
    return None


@traceable(name="Scan QR Code from PDF")
def scan_qr_code(pdf_path: Path, output_dir: Path, use_heuristic: bool = False) -> dict:
	doc = None
	found_method = None
	try:
		doc = fitz.open(pdf_path)
		page_count = doc.page_count if hasattr(doc, "page_count") else len(doc)

		# Phase 1: scan the lower half of every page (last -> first)
		for page_num in range(page_count - 1, -1, -1):
			page = doc.load_page(page_num)
			for zoom in (4.0, 6.0, 8.0):
				try:
					pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
					page_img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
					# Crop to lower half
					w, h = page_img.size
					lower_half = page_img.crop((0, h // 2, w, h))
					pre_img = preprocess_image(lower_half)
					qr_text = _wechat_decode(pre_img)
					if qr_text:
						found_method = "WeChat"
					else:
						qr_text = _opencv_decode(pre_img)
						if qr_text:
							found_method = "OpenCV"
					if qr_text and qr_text.startswith("SPC"):
						if found_method:
							print(f"Extracted with: {found_method}")
						os.makedirs(output_dir, exist_ok=True)
						out_path = Path(output_dir) / (pdf_path.stem + "_qr.json")
						json_data = {"raw_qr_text": qr_text}
						try:
							invoice = parse_swiss_qr(qr_text)
							json_data["parsed_invoice"] = invoice.as_dict()
						except Exception as e:
							print("Failed to parse Swiss QR invoice:", e)
						with open(out_path, "w", encoding="utf-8") as f:
							json.dump(json_data, f, ensure_ascii=False, indent=2)
							print("Amount to pay:", invoice.amount if 'invoice' in locals() else None)
						return {
							"qr_text": qr_text,
							"method": found_method,
							"invoice": json_data.get("parsed_invoice"),
							"output_file": str(out_path),
						}
				except Exception:
					continue

		# Phase 2: fallback to original behavior (embedded images first, then full-page renders)
		for page_num in range(page_count - 1, -1, -1):
			page = doc.load_page(page_num)
			for info in page.get_images(full=True):
				xref = info[0]
				try:
					base_image = doc.extract_image(xref)
					img_bytes = base_image.get("image")
					if not img_bytes:
						continue
					try:
						pil_img = Image.open(io.BytesIO(img_bytes))
					except Exception:
						pix = fitz.Pixmap(doc, xref)
						pil_img = _pil_from_pixmap(pix)
					pre_img = preprocess_image(pil_img)
					qr_text = _wechat_decode(pre_img)
					if qr_text:
						found_method = "WeChat"
					else:
						qr_text = _opencv_decode(pre_img)
						if qr_text:
							found_method = "OpenCV"
					if qr_text and qr_text.startswith("SPC"):
						if found_method:
							print(f"Extracted with: {found_method}")
						os.makedirs(output_dir, exist_ok=True)
						out_path = Path(output_dir) / (pdf_path.stem + "_qr.json")
						json_data = {"raw_qr_text": qr_text}
						try:
							invoice = parse_swiss_qr(qr_text)
							json_data["parsed_invoice"] = invoice.as_dict()
						except Exception as e:
							print("Failed to parse Swiss QR invoice:", e)
						with open(out_path, "w", encoding="utf-8") as f:
							json.dump(json_data, f, ensure_ascii=False, indent=2)
							print("Amount to pay:", invoice.amount if 'invoice' in locals() else None)
						return {
							"qr_text": qr_text,
							"method": found_method,
							"invoice": json_data.get("parsed_invoice"),
							"output_file": str(out_path),
						}
				except Exception:
					continue
			for zoom in (4.0, 6.0, 8.0):
				try:
					pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
					page_img = Image.frombytes(
						"RGB", [pix.width, pix.height], pix.samples
					)
					pre_img = preprocess_image(page_img)
					qr_text = _wechat_decode(pre_img)
					if qr_text:
						found_method = "WeChat"
					else:
						qr_text = _opencv_decode(pre_img)
						if qr_text:
							found_method = "OpenCV"
					if qr_text and qr_text.startswith("SPC"):
						if found_method:
							print(f"Extracted with: {found_method}")
						os.makedirs(output_dir, exist_ok=True)
						out_path = Path(output_dir) / (pdf_path.stem + "_qr.json")
						json_data = {"raw_qr_text": qr_text}
						try:
							invoice = parse_swiss_qr(qr_text)
							json_data["parsed_invoice"] = invoice.as_dict()
						except Exception as e:
							print("Failed to parse Swiss QR invoice:", e)
						with open(out_path, "w", encoding="utf-8") as f:
							json.dump(json_data, f, ensure_ascii=False, indent=2)
							print("Amount to pay:", invoice.amount if 'invoice' in locals() else None)
						return {
							"qr_text": qr_text,
							"method": found_method,
							"invoice": json_data.get("parsed_invoice"),
							"output_file": str(out_path),
						}
				except Exception:
					continue

		# If no QR code found, save error JSON
		os.makedirs(output_dir, exist_ok=True)
		out_path = Path(output_dir) / (pdf_path.stem + "_qr_error.json")
		with open(out_path, "w", encoding="utf-8") as f:
			json.dump({"error": "No QR code found"}, f, ensure_ascii=False, indent=2)

		# Heuristic fallback: only if explicitly allowed
		if use_heuristic:
			try:
				from .io_utils import find_iban_in_markdown  # lazy import to avoid circular issues
				iban = find_iban_in_markdown(output_dir)
			except Exception:
				iban = None

			if iban:
				# Create a minimal fallback parsed invoice structure
				fallback = {
					"raw_qr_text": None,
					"heuristic_iban": iban,
					"parsed_invoice": {
						"qr_type": None,
						"version": None,
						"coding_type": None,
						"iban": iban,
						"creditor": None,
						"amount": None,
						"currency": None,
					},
				}
				fallback_path = Path(output_dir) / (pdf_path.stem + "_qr_fallback.json")
				with open(fallback_path, "w", encoding="utf-8") as f:
					json.dump(fallback, f, ensure_ascii=False, indent=2)
				# Return a consistent structure similar to successful detections:
				# include qr_text (None here), method, invoice (parsed structure), and output_file.
				return {
					"qr_text": None,
					"method": "heuristic",
					"invoice": fallback["parsed_invoice"],
					"output_file": str(fallback_path),
				}

		return {"error": "No QR code found", "output_file": str(out_path)}
	finally:
		if doc is not None:
			doc.close()