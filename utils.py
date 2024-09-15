import io
import os
from typing import Any, Dict

import PyPDF2
from fastapi import HTTPException
from pydantic import BaseModel, Field

from config import logger


class Message(BaseModel):
    role: str = Field(default="user", description="The role of the user.")
    parts: str = Field(default="model", description="The parts of the system to access.")


# Function to save a file to a temporary location
def save_temp_file(file_bytes: bytes, file_name: str) -> str:
    temp_file_path = f"/tmp/{file_name}"
    try:
        with open(temp_file_path, "wb") as f:
            f.write(file_bytes)
        logger.info(f"File saved: {temp_file_path}")
    except Exception as e:
        logger.error(f"Error saving file {file_name}: {e}")
        raise HTTPException(status_code=500, detail="Error saving file")
    return temp_file_path


# Function to clean up a temporary file
def clean_up_temp_file(file_path: str) -> None:
    try:
        os.remove(file_path)
        logger.info(f"File removed: {file_path}")
    except Exception as e:
        logger.error(f"Error removing file {file_path}: {e}")
        raise HTTPException(status_code=500, detail="Error removing file")


# Function to extract text from a PDF
def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    if not pdf_bytes:
        logger.error("No PDF data provided")
        raise HTTPException(status_code=400, detail="No PDF data provided")

    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
        if not pdf_reader.pages:
            logger.error("No pages found in PDF")
            raise HTTPException(status_code=400, detail="No pages found in PDF")

        extracted_text = ""
        for page_num, page in enumerate(pdf_reader.pages):
            try:
                text = page.extract_text()
                if text:
                    extracted_text += text
                else:
                    logger.warning(f"No text found on page {page_num}")
            except Exception as page_error:
                logger.error(f"Error extracting text from page {page_num}: {page_error}")
                continue  # Skip the problematic page and continue with the next one

        if not extracted_text:
            logger.error("No text extracted from PDF")
            raise HTTPException(status_code=400, detail="No text extracted from PDF")

        return extracted_text
    except Exception as e:
        logger.error(f"PDF read error: {e}")
        raise HTTPException(status_code=500, detail="Error reading PDF")


class GenerateStructuredOutputRequest(BaseModel):
    prompt: str = Field(default="Provide a summary of the latest news.", description="The prompt to generate content.")
    json_schema: Dict[str, Any] = Field(
        default={
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "summary": {"type": "string"}
            },
            "required": ["title", "summary"]
        },
        description="The JSON schema to structure the output."
    )