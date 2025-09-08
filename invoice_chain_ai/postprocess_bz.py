from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict, List, Set

from langsmith import traceable

from .bz_mapping import BZ_MAPPING
from .structured_output import run_bz_art_classification

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
		(raw.get("header") or {}).get("invoice_language")
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
			if lang == "fr":
				desc = entry.get("description_fr") or ""
			elif lang == "it":
				desc = entry.get("description_it") or ""
			else:
				desc = entry.get("description_de") or ""
			filtered.append({
				"bz_art": entry.get("bz_art"),
				"type": entry.get("type"),
				"unit_quantity": unit,
				"price_unit": entry.get("price_unit"),
				"description": desc,
			})

	# 4) build prompt text (reference mapping + examples + line items). Keep it compact.
	prompt_lines: List[str] = []

	# Set task instructions based on language
	if lang == "fr":
		prompt_lines.append("# TÂCHE")
		prompt_lines.append("Étant donné les détails d'une ligne de facture d'énergie, déterminez le 'BZArt' (type de ligne de consommation) correct parmi les options suivantes pour chaque ligne.")
		prompt_lines.append("Prenez en compte la description, l'unité de quantité et la catégorie. Retournez un tableau JSON des valeurs BZArt dans le même ordre que les lignes. Si aucune correspondance n'est possible, retournez 'UNKNOWN'.")
		prompt_lines.append("\n#Mapping de référence :")
	elif lang == "it":
		prompt_lines.append("# COMPITO")
		prompt_lines.append("Dato i dettagli di una voce di bolletta energetica, determina il 'BZArt' (tipo di riga di consumo) corretto tra le seguenti opzioni per ogni voce.")
		prompt_lines.append("Considera descrizione, unità di quantità e categoria. Restituisci un array JSON dei valori BZArt nello stesso ordine delle voci. Se non è possibile assegnare, restituisci 'UNKNOWN'.")
		prompt_lines.append("\n#Mappatura di riferimento:")
	elif lang == "de":
		prompt_lines.append("# AUFGABE")
		prompt_lines.append("Gegeben die Details einer Energiebillenzeile, bestimme die korrekte 'BZArt' (Bezugszeilenart) aus den folgenden Optionen pro line Item.")
		prompt_lines.append("Berücksichtige Beschreibung, Mengeneinheit und Kategorie. Gib ein JSON-Array der BZArt-Werte in derselben Reihenfolge wie die Zeilen zurück. Falls keine Zuordnung möglich, gib 'UNKNOWN' zurück.")
		prompt_lines.append("\n#Referenzmapping:")

	for entry in filtered:
		if lang == "fr":
			prompt_lines.append(f"BZArt : {entry['bz_art']}")
			if entry["type"] and entry["type"] != "NULL":
				prompt_lines.append(f"Type : {entry['type']}")
			prompt_lines.append(f"Unité de quantité : {entry['unit_quantity']}")
			prompt_lines.append(f"Unité de prix : {entry['price_unit']}")
			prompt_lines.append(f"- Description ({invoice_language}) : {entry['description']}")
			prompt_lines.append("-------------------")
		elif lang == "it":
			prompt_lines.append(f"BZArt: {entry['bz_art']}")
			if entry["type"] and entry["type"] != "NULL":
				prompt_lines.append(f"Tipo: {entry['type']}")
			prompt_lines.append(f"Unità di quantità: {entry['unit_quantity']}")
			prompt_lines.append(f"Unità di prezzo: {entry['price_unit']}")
			prompt_lines.append(f"- Descrizione ({invoice_language}): {entry['description']}")
			prompt_lines.append("-------------------")
		elif lang == "de":
			prompt_lines.append(f"BZArt: {entry['bz_art']}")
			if entry["type"] and entry["type"] != "NULL":
				prompt_lines.append(f"Typ: {entry['type']}")
			prompt_lines.append(f"Einheit Menge: {entry['unit_quantity']}")
			prompt_lines.append(f"Einheit Preis: {entry['price_unit']}")
			prompt_lines.append(f"- Beschreibung ({invoice_language}): {entry['description']}")
			prompt_lines.append("-------------------")

	# add compact examples in the correct language
	if lang == "fr":
		prompt_lines.append(
			"""
# Exemples (description de la ligne -> BZArt):
- "Travail tarif élevé" -> "HT"
- "Travail tarif bas" -> "NT"
- "Énergie active HT" -> "DL_HT"
- "Énergie active NT" -> "DL_NT"
- "Tarif de base" -> "DL_Geb"
- "Tarif de puissance" -> "DL_Leistung"
- "Services système Swissgrid" -> "NDL_System"
- "Taxe légale de promotion" -> "KEV"
- "Taxes et prestations à la commune" -> "SA_L"
- "Réserve d'électricité" -> "ERA_M"
"""
		)
	elif lang == "it":
		prompt_lines.append(
			"""
# Esempi (descrizione voce -> BZArt):
- "Lavoro tariffa alta" -> "HT"
- "Lavoro tariffa bassa" -> "NT"
- "Energia attiva HT" -> "DL_HT"
- "Energia attiva NT" -> "DL_NT"
- "Tariffa base" -> "DL_Geb"
- "Tariffa potenza" -> "DL_Leistung"
- "Servizi di sistema Swissgrid" -> "NDL_System"
- "Tassa legale di promozione" -> "KEV"
- "Tasse e prestazioni al comune" -> "SA_L"
- "Riserva elettrica" -> "ERA_M"
"""
		)
	elif lang == "de":
		prompt_lines.append(
			"""
# Beispiele (line item description -> BZArt):
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


	prompt_lines.append("# Line item:")
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

	# 5) call LLM
	# request an output shaped as {"bz_arts": ["DL_HT", "NT", ...]}
	# Build a language-aware instruction for the classifier (customer-facing)
	if lang == "fr":
		customer_instruction = "Retournez un seul objet JSON avec la propriété 'bz_arts' qui est un tableau de chaînes. Chaque élément correspond à la BZArt de la ligne correspondante. Utilisez 'UNKNOWN' si aucune correspondance."
	elif lang == "it":
		customer_instruction = "Restituisci un unico oggetto JSON con la proprietà 'bz_arts' che è un array di stringhe. Ogni elemento corrisponde al BZArt della voce corrispondente. Usa 'UNKNOWN' se non c'è corrispondenza."
	else:
		customer_instruction = "Geben Sie ein einzelnes JSON-Objekt mit der Eigenschaft 'bz_arts' zurück, das ein Array von Strings ist. Jedes Element entspricht der BZArt der jeweiligen Zeile. Verwenden Sie 'UNKNOWN', wenn keine Zuordnung möglich ist."
	
	try:
		res = run_bz_art_classification(bz_prompt_md, customer_prompt=customer_instruction, run_dir=run_dir, lang=lang)
	except Exception:
		# safe fallback if the call fails: mark all as UNKNOWN
		res = {"bz_arts": []}

	bz_arts = res.get("bz_arts") or []

	# merge results into line items (key: "BZArt"), fallback to "UNKNOWN" if missing
	for idx, li in enumerate(line_items):
		val = bz_arts[idx] if idx < len(bz_arts) else "UNKNOWN"
		li["BZArt"] = val

	# write enriched JSON back to disk
	raw["line_items"] = line_items

	# Ensure header exists
	header = raw.get("header") or {}

	# Try to find a previously extracted QR json (pattern *_qr.json) in run_dir (recursive)
	qr_files = list(run_dir.rglob("*_qr.json"))
	if qr_files:
		qr_json_path = qr_files[0]
		try:
			qr_data = json.loads(qr_json_path.read_text(encoding="utf-8"))
			parsed = qr_data.get("parsed_invoice") or qr_data.get("parsed") or {}

			# provider <- creditor block (if present)
			creditor = parsed.get("creditor") or {}
			prov_name = creditor.get("name") or creditor.get("creditor_name") or parsed.get("creditor_name")
			prov_addr1 = creditor.get("address_line_1") or creditor.get("address_line1") or None
			postal = creditor.get("postal_code") or creditor.get("postal") or ""
			city = creditor.get("city") or ""
			city_zip = (" ".join([p for p in [postal, city] if p])).strip() or None

			header["provider"] = {
				"name": prov_name,
				"address_line1": prov_addr1,
				"city_zip": city_zip
			}

			# payment_information from parsed_invoice top-level and creditor info
			header["payment_information"] = {
				"creditor_name": prov_name,
				"street": prov_addr1,
				"city_zip": city_zip,
				"iban": parsed.get("iban"),
				"reference": parsed.get("reference"),
				"amount": parsed.get("amount"),
				"currency": parsed.get("currency")
			}

			# filename: extract from qr filename (part before '_qr.json')
			filename = qr_json_path.name.split("_qr.json")[0]
			header["filename"] = filename
		except Exception:
			pass
	else:
		pass

	raw["header"] = header

	raw_structured_path.write_text(json.dumps(raw, ensure_ascii=False, indent=2), encoding="utf-8")

	return raw
