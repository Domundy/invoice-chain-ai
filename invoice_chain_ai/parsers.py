from __future__ import annotations

import os
from pathlib import Path
from typing import Literal
import shutil  # added

from dotenv import load_dotenv
from docling.document_converter import DocumentConverter
from docling.datamodel.pipeline_options import PdfPipelineOptions
from langsmith import traceable

from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.config.parser import ConfigParser
from marker.output import text_from_rendered
from marker.services.openai import OpenAIService

Engine = Literal["docling", "marker"]

@traceable(name="Convert PDF to Markdown")
def convert_pdf_to_markdown(
    pdf_path: Path, engine: Engine, *, use_llm: bool = False, output_dir: Path
) -> str:
    """Convert PDF to markdown using specified engine."""
    if engine == "docling":
        md = _convert_with_docling(pdf_path)
        return md
    elif engine == "marker":
        md = _convert_with_marker(pdf_path, use_llm, output_dir)
        return md
    else:
        raise ValueError(f"Unknown engine: {engine}")


@traceable(name="Docling PDF Conversion")
def _convert_with_docling(pdf_path: Path) -> str:
    """Convert PDF to markdown using docling."""
    # Prefer OCR language config if supported by your docling version
    pipeline_options = PdfPipelineOptions()
    pipeline_options.ocr_options.lang = ["de", "it", "fr"]

    try:
        # Newer API: constructor accepts pipeline_options
        converter = DocumentConverter(pipeline_options=pipeline_options)
        result = converter.convert(str(pdf_path))

    except TypeError:
        # Older API: no pipeline_options support -> fall back without options
        converter = DocumentConverter()
        result = converter.convert(str(pdf_path))

    return result.document.export_to_markdown()


@traceable(name="Marker PDF Conversion")
def _convert_with_marker(
    pdf_path: Path, use_llm: bool = False, output_dir: Path = None
) -> str:
    """Convert PDF using Marker with optional LLM. Images are stored in output_dir/images after conversion if provided."""

    config = {
        "output_format": "markdown",
        "output_dir": str(output_dir),
        "disable_image_extraction": True,
    }

    if use_llm:
        load_dotenv()
        config.update(
            {
                "use_llm": True,
                "llm_service": os.getenv(
                    "MARKER_LLM_SERVICE", "marker.services.openai.OpenAIService"
                ),
                "openai_model": os.getenv("MARKER_OPENAI_MODEL", "gpt-5-mini"),
                "openai_base_url": os.getenv(
                    "OPENAI_BASE_URL", "https://api.openai.com/v1"
                ),
                "openai_api_key": os.getenv("OPENAI_API_KEY"),
            }
        )

    config_parser = ConfigParser(config)

    converter = PdfConverter(
        config=config_parser.generate_config_dict(),
        artifact_dict=create_model_dict(),
        processor_list=config_parser.get_processors(),
        renderer=config_parser.get_renderer(),
        llm_service=config_parser.get_llm_service(),
    )

    # Run conversion without changing cwd to avoid breaking relative resource paths.
    rendered = converter(str(pdf_path))
    text, metadata, images = text_from_rendered(rendered)
    if images:
        images_dir = output_dir / "images"
        images_dir.mkdir(parents=True, exist_ok=True)
        for filename, img in images.items():
            img.save(images_dir / filename)

    return text
