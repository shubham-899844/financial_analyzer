from crewai.tools import tool
from pypdf import PdfReader
import os
from tools import read_pdf_raw
@tool("Read Financial Document")
def read_financial_document(filename: str) -> str:
    """
    Reads a financial PDF from the data directory and extracts text.
    
    Args:
        filename (str): PDF file name located in data folder.
        
    Returns:
        str: Extracted text.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "data", filename)

    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content

    return text
