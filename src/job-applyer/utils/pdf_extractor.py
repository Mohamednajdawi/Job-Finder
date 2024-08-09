import io

import PyPDF2


def extract_text_from_pdf(pdf_file: io.BytesIO) -> str:
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    return "".join(page.extract_text() for page in pdf_reader.pages)
