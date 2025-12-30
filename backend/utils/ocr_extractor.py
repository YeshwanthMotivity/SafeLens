import pytesseract
from PIL import Image
import io
import logging

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

logging.basicConfig(level=logging.INFO, format="📄 [%(levelname)s] → %(message)s")

def extract_text_from_image(image_bytes: bytes) -> str:
    """
    Extracts text from an uploaded image using Tesseract OCR.
    Args:
        image_bytes: raw bytes of the uploaded image file
    Returns:
        Extracted text as string
    """
    try:
        image = Image.open(io.BytesIO(image_bytes))
        text = pytesseract.image_to_string(image)
        clean_text = text.strip()
        logging.info(f"OCR extracted text length: {len(clean_text)} chars")
        return clean_text if clean_text else "[No text detected in image]"
    except Exception as e:
        logging.error(f"OCR extraction failed: {e}")
        return "[Error extracting text]"
