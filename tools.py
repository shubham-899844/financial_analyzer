from PyPDF2 import PdfReader


def extract_text_from_pdf(file):
    file.seek(0)
    reader = PdfReader(file)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    if not text.strip():
        raise ValueError("Could not extract readable text from PDF.")

    return text[:15000]  # prevent token overflow