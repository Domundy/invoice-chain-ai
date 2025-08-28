from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict, List, Set

from langsmith import traceable

from .bz_mapping import BZ_MAPPING
from .structured_output import run_structured_output_modern

@traceable(name="BZArt Enrichment")
def enrich_bz_art(raw_structured_path: Path, run_dir: Path) -> Dict[str, Any]:
	"""
	Load raw structured output JSON, build a language-aware prompt filtered by quantity units,
	call the LLM, and enrich each line item with a 'BZArt' value. Write enriched JSON back.
	"""
	# load raw structured JSON
	raw = json.loads(raw_structured_path.read_text(encoding="utf-8"))

	# 1) extract invoice language (try common keys)
	invoice_language = (
		raw.get("invoice_language")
		or raw.get("language")
		or (raw.get("header") or {}).get("invoice_language")
		or (raw.get("header") or {}).get("language")
		or "de"
	)
	lang = invoice_language.lower()[:2]  # 'de','fr','it' fallback

	# 2) collect quantity units from each line item (include empty string / null)
	units: Set[str] = set()
	line_items = raw.get("line_items", []) or []
	for li in line_items:
		q = li.get("quantity_unit")
		if q is None:
			q = ""
		units.add(str(q))

	# 3) filter BZ_MAPPING entries by unit_quantity matching the collected units
	filtered = []
	for entry in BZ_MAPPING:
		unit = (entry.get("unit_quantity") or "")
		if unit in units:
			# build a reduced entry keeping only the description in the invoice language
			desc = ""
			if lang == "fr":
				desc = entry.get("description_fr") or entry.get("description_de") or entry.get("description_it") or ""
			elif lang == "it":
				desc = entry.get("description_it") or entry.get("description_de") or entry.get("description_fr") or ""
			else:
				desc = entry.get("description_de") or entry.get("description_fr") or entry.get("description_it") or ""
			filtered.append({
				"bz_art": entry.get("bz_art"),
				"type": entry.get("type"),
				"unit_quantity": unit,
				"price_unit": entry.get("price_unit"),
				"description": desc,
				"description_de": entry.get("description_de"),
				"description_fr": entry.get("description_fr"),
				"description_it": entry.get("description_it"),
			})

	# 4) build prompt text (reference mapping + examples + line items). Keep it compact.
	prompt_lines: List[str] = []
	prompt_lines.append("# TASK")
	prompt_lines.append("Given an energy bill line item details, determine the correct 'BZArt' (Bezugszeilenart) from the following options.")
	prompt_lines.append("Consider description, quantity_unit and category. Return a JSON array of BZArt values in the same order as the line items.")
	prompt_lines.append("\n#Reference mapping:")
	for entry in filtered:
		prompt_lines.append(f"BZArt: {entry['bz_art']}")
		if entry["type"] and entry["type"] != "NULL":
			prompt_lines.append(f"Type: {entry['type']}")
		prompt_lines.append(f"Unit Quantity: {entry['unit_quantity']}")
		prompt_lines.append(f"Price Unit: {entry['price_unit']}")
		# only include the single-language description plus the other language descs for context
		prompt_lines.append(f"- Description ({invoice_language}): {entry['description']}")
		# also include the other language descriptions for better matching
		prompt_lines.append(f"- German: {entry.get('description_de','')}")
		prompt_lines.append(f"- French: {entry.get('description_fr','')}")
		prompt_lines.append(f"- Italian: {entry.get('description_it','')}")
		prompt_lines.append("-------------------")

	# add compact examples
	prompt_lines.append(
		"""
# Examples (line item description -> BZArt):
- "Arbeit Hochtarif" -> "HT"
- "Arbeit Niedertarif" -> "NT"
- "Wirkenergie HT" -> "DL_HT"
- "Wirkenergie NT" -> "DL_NT"
- "Grundtarif" -> "DL_Geb"
- "Leistungstarif" -> "DL_Leistung"
- "Systemdienstleistungen Swissgrid" -> "NDL_System"
- "Gesetzliche Förderabgabe" -> "KEV"
- "Abgaben und Leistungen an die Gemeinde" -> "SA_L"
- "Stromreserve" -> "ERA_M"
"""
	)

	# prepare the items to be classified
	prompt_lines.append("\nFor the following line items, return ONLY a JSON array of BZArt values (strings) in the same order. If no match is found for a line item, return \"UNKNOWN\" for that position.\n")
	prompt_lines.append("# Line item details:")
	for li in line_items:
		descr = li.get("line_items_description") or li.get("description") or ""
		q_unit = li.get("quantity_unit") or ""
		category = li.get("category") or ""
		# include meter_point/VS_Adr if present for context
		extra = []
		if li.get("meter_point"):
			extra.append(f"meter_point={li.get('meter_point')}")
		if li.get("VS_Adr"):
			extra.append(f"VS_Adr={li.get('VS_Adr')}")
		extra_s = (" | " + " ; ".join(extra)) if extra else ""
		prompt_lines.append(f"- Description: {descr} | quantity_unit: {q_unit} | category: {category}{extra_s}")

	prompt_text = "\n".join(prompt_lines)

	# write prompt to a temporary md file and call the existing LLM wrapper
	bz_prompt_md = run_dir / "bz_prompt.md"
	bz_prompt_md.write_text(prompt_text, encoding="utf-8")

	# 5) call LLM via the existing helper (re-uses the project's structured output LLM pipeline)
	try:
		llm_result = run_structured_output_modern(bz_prompt_md, None, run_dir)
	except Exception as e:
		# on failure, annotate with UNKNOWN and return raw
		for li in line_items:
			li["BZArt"] = "UNKNOWN"
		out_path = run_dir / "raw_structured_output_enriched.json"
		out_path.write_text(json.dumps(raw, ensure_ascii=False, indent=2), encoding="utf-8")
		return raw

	# llm_result might be dict or string; try to extract JSON array
	predictions: List[str] = []
	if isinstance(llm_result, dict):
		# try common keys
		for k in ("output", "result", "content", "text", "answer"):
			v = llm_result.get(k)
			if v:
				try:
					predictions = json.loads(v) if isinstance(v, str) else v
					break
				except Exception:
					# not JSON, try as string of array
					try:
						predictions = json.loads(str(v))
						break
					except Exception:
						continue
		# fallback: use the dict itself if it's a list-like under 'predictions'
		if not predictions:
			if isinstance(llm_result, list):
				predictions = llm_result  # type: ignore
	elif isinstance(llm_result, str):
		# try to parse a JSON array from string
		try:
			predictions = json.loads(llm_result)
		except Exception:
			# fallback: split lines and take tokens that look like codes
			lines = [l.strip().strip('"') for l in llm_result.splitlines() if l.strip()]
			# attempt to pick tokens that look like bz_art codes
			predictions = lines

	# ensure predictions is a list of strings
	predictions = [str(p) for p in (predictions or [])]

	# 6) enrich raw line items
	for idx, li in enumerate(line_items):
		if idx < len(predictions) and predictions[idx]:
			li["BZArt"] = predictions[idx]
		else:
			li["BZArt"] = "UNKNOWN"

	# write enriched file
	out_path = run_dir / "raw_structured_output_enriched.json"
	out_path.write_text(json.dumps(raw, ensure_ascii=False, indent=2), encoding="utf-8")

	return raw