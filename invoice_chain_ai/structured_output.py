from __future__ import annotations
from pathlib import Path
from typing import Optional, Dict, Any, List

# Updated imports for modern LangChain
from langchain_core.messages import HumanMessage, SystemMessage
from .structure import EnergyBill
from langchain_openai import ChatOpenAI
import os
from pydantic import BaseModel

SYSTEM_PROMPT = """
# Swiss Utility Bill Parser

You are a specialized data extraction system that converts Swiss commercial utility bills into structured JSON using the provided Pydantic schema.

## Extraction Protocol
1. **Parse systematically**: Process header information first, then extract all line items sequentially
2. **Follow field constraints**: Adhere strictly to formatting rules embedded in each field description
3. **Preserve source accuracy**: Extract values exactly as shown - never calculate or derive missing data
4. **Complete extraction**: Include every line item present on the bill, regardless of price value.

## Critical Rules
- **VAT handling**: Only extract explicitly stated VAT amounts - never calculate or infer
- **Data completeness**: Extract all line items, including those with zero values
- **Format adherence**: Follow all date, currency, and measurement constraints specified in field descriptions
- **Line item handling**: Never summarize line items; extract each one individually ignoring any subtotals
- **Schema compliance**: Ensure output strictly matches the EnergyBill structure

## Output Requirements
Return a single, valid JSON object conforming to the EnergyBill schema. Do not include explanatory text or metadata outside the JSON structure.
"""

def _default_system_message() -> str:
    """Return the embedded system prompt."""
    return SYSTEM_PROMPT

def run_structured_output_modern(markdown_path: Path, customer_prompt: Optional[str] = None, run_dir: Optional[Path] = None) -> Dict[str, Any]:
    """
    Modern approach using ChatOpenAI with structured output (recommended).
    Requires langchain-openai package.
    """
    system_msg = _default_system_message()

    model_name = os.environ.get("STRUCTURED_OUTPUT_MODEL", "gpt-5-mini")
    llm = ChatOpenAI(
        model=model_name,
        temperature=0
    )
    
    # Use with_structured_output for automatic JSON parsing
    structured_llm = llm.with_structured_output(EnergyBill)
    
    # Read markdown content
    with open(markdown_path, "r", encoding="utf-8") as f:
        context = f.read()

    # Create messages
    messages = [
        SystemMessage(content=system_msg),
        HumanMessage(content=f"""
        Instructions: {customer_prompt}

        Invoice markdown:
        {context}

        """)
    ]
    
    # Get structured output
    result = structured_llm.invoke(messages)
    
    # Convert to dict if it's a Pydantic model
    if hasattr(result, "model_dump"):
        return result.model_dump()
    elif hasattr(result, "dict"):
        return result.dict()
    else:
        return result

# New: tiny Pydantic model for BZArt list
class BZArtList(BaseModel):
    bz_arts: List[str]

def run_bz_art_classification(markdown_path: Path, customer_prompt: Optional[str] = None, run_dir: Optional[Path] = None, lang: str = "de") -> Dict[str, Any]:
    """
    Call the LLM to classify each line item into a BZArt. Returns a dict with key 'bz_arts' => list[str].
    Expects the markdown file to contain the mapping + line items (created in postprocess_bz).
    """
    # language-aware system message
    if lang == "fr":
        system_msg = (
            "Vous recevez une mappage de référence et une liste de lignes de facture. "
            "Retournez un seul objet JSON avec la propriété 'bz_arts' qui est un tableau de chaînes. "
            "Chaque élément correspond au BZArt pour la ligne correspondante dans le même ordre. "
            "Utilisez la chaîne exacte 'UNKNOWN' si aucune affectation n'est possible. "
            "N'incluez aucun commentaire supplémentaire ni champs additionnels."
        )
    elif lang == "it":
        system_msg = (
            "Ricevi una mappatura di riferimento e un elenco di voci di fattura. "
            "Restituisci un unico oggetto JSON con la proprietà 'bz_arts' che è un array di stringhe. "
            "Ogni elemento corrisponde al BZArt per la voce corrispondente nello stesso ordine. "
            "Usa la stringa esatta 'UNKNOWN' se non è possibile assegnare. "
            "Non includere commenti o campi aggiuntivi."
        )
    else:
        system_msg = (
            "Sie erhalten ein Referenzmapping und eine Liste von Rechnungszeilen. "
            "Geben Sie ein einzelnes JSON-Objekt mit der Eigenschaft 'bz_arts' zurück, das ein Array von Strings ist. "
            "Jedes Element entspricht der BZArt für die jeweilige Zeile in derselben Reihenfolge. "
            "Verwenden Sie genau den String 'UNKNOWN', wenn keine Zuordnung möglich ist. "
            "Fügen Sie keine zusätzlichen Erläuterungen oder Felder hinzu."
        )

    model_name = os.environ.get("STRUCTURED_OUTPUT_MODEL", "gpt-5-mini")
    llm = ChatOpenAI(
        model=model_name,
        temperature=0
    )

    structured_llm = llm.with_structured_output(BZArtList)

    # Read markdown content
    with open(markdown_path, "r", encoding="utf-8") as f:
        context = f.read()

    # language-aware human instruction (customer_prompt overrides)
    if customer_prompt:
        human_text = customer_prompt
    else:
        if lang == "fr":
            human_text = "Classifiez les lignes suivantes en BZArt. Retournez uniquement {\"bz_arts\":[...]}."
        elif lang == "it":
            human_text = "Classifica le seguenti righe in BZArt. Restituisci solo {\"bz_arts\":[...]}."
        else:
            human_text = "Klassifiziere die folgenden Zeilen in BZArt. Gib nur {\"bz_arts\":[...]} zurück."
            
    messages = [
        SystemMessage(content=system_msg),
        HumanMessage(content=f"{human_text}\n\nInvoice markdown:\n{context}")
    ]

    result = structured_llm.invoke(messages)

    if hasattr(result, "model_dump"):
        return result.model_dump()
    elif hasattr(result, "dict"):
        return result.dict()
    else:
        # fallback: try to return an empty structure
        return {"bz_arts": []}