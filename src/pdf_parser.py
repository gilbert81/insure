import pdfplumber
import pytesseract
from PIL import Image
import os
import json # For creating JSON strings if needed, though returning a dict is fine

# Path to tesseract executable, if not in PATH (uncomment and set if needed)
# pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

MIN_TEXT_LENGTH_FOR_OCR_FALLBACK = 20 # Example threshold

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file, using OCR as a fallback for image-based pages."""
    full_text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text()

                perform_ocr = False
                if page_text is None or len(page_text.strip()) < MIN_TEXT_LENGTH_FOR_OCR_FALLBACK:
                    perform_ocr = True

                if perform_ocr:
                    try:
                        img = page.to_image(resolution=300)
                        ocr_text = img.ocr(lang='eng')
                        page_text = ocr_text if ocr_text else ""
                        print(f"Page {i+1}: Used OCR. Extracted text length: {len(page_text)}")
                    except Exception as e:
                        print(f"Error during OCR on page {i+1}: {e}")
                        page_text = page.extract_text() if page.extract_text() else ""
                else:
                    print(f"Page {i+1}: Used standard text extraction. Extracted text length: {len(page_text) if page_text else 0}")

                if page_text:
                    full_text += page_text + "\n"
    except Exception as e:
        print(f"Error opening or processing PDF {pdf_path}: {e}")
        return ""

    return full_text.strip()

# Expected fields from PRD:
# - Insurance type (car, home, travel, etc.)
# - Provider name
# - Renewal date
# - Premium amount
# - Coverage type & excess

def parse_text_to_json_mock(raw_text):
    """
    Parses raw text extracted from a PDF into a structured JSON format.
    This version uses a mock implementation for LLM processing.
    """
    data = {
        "insurance_type": None,
        "provider_name": None,
        "renewal_date": None,
        "premium_amount": None,
        "coverage_type": None,
        "excess_amount": None # Assuming 'excess' might be a monetary value
    }

    # Example mock logic (very rudimentary)
    # A real LLM would handle variations, context, and complex extraction.
    # Convert raw_text to lowercase for case-insensitive matching
    raw_text_lower = raw_text.lower()

    if "car insurance" in raw_text_lower:
        data["insurance_type"] = "Car"
    elif "home insurance" in raw_text_lower:
        data["insurance_type"] = "Home"

    if "provider: exampleinsurer" in raw_text_lower: # Match "Provider: ExampleInsurer"
        data["provider_name"] = "ExampleInsurer"
    elif "admiral" in raw_text_lower: # From example UI in PRD
        data["provider_name"] = "Admiral"

    if "renewal date: 2025-07-15" in raw_text_lower: # Match "Renewal date: 2025-07-15"
        data["renewal_date"] = "2025-07-15"

    if "premium: £723" in raw_text_lower or "£723" in raw_text_lower: # From example UI
        data["premium_amount"] = "£723"

    if "fully comprehensive" in raw_text_lower:
        data["coverage_type"] = "Fully comprehensive"

    if "excess: £250" in raw_text_lower or "£250 excess" in raw_text_lower: # From example UI
        data["excess_amount"] = "£250"

    return data

def process_pdf_to_structured_data(pdf_path):
    """Extracts text from PDF and then parses it into structured JSON."""
    raw_text = extract_text_from_pdf(pdf_path)
    if raw_text:
        structured_data = parse_text_to_json_mock(raw_text)
        return structured_data
    return None

if __name__ == '__main__':
    pdf_file = 'data/example_document_for_parsing.pdf'
    if not os.path.exists(pdf_file):
        print(f"Error: PDF file not found at {pdf_file}")
    else:
        print(f"Starting full processing for: {pdf_file}")

        structured_info = process_pdf_to_structured_data(pdf_file)
        if structured_info:
            print("\nSuccessfully parsed to structured data (mocked LLM):")
            # Use json.dumps for pretty printing the dictionary
            print(json.dumps(structured_info, indent=2))
        else:
            print("\nCould not extract text or parse data.")
