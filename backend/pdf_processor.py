import fitz

def read_pdf(file):
    """Extracts text from an uploaded PDF file efficiently."""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        text = "\n".join(page.get_text() for page in doc)
    print(f"PDF Text:- {text}")
    return text
