from __future__ import annotations
from pathlib import Path
from typing import Optional, Dict, Any

# Updated imports for modern LangChain
from langchain_core.messages import HumanMessage, SystemMessage
from .structure import EnergyBill
from langchain_openai import ChatOpenAI
import os

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