import fitz

def extract_text_from_pdf(uploaded_file):

    uploaded_file.seek(0)

    pdf_bytes = uploaded_file.getvalue()

    if not pdf_bytes:
        raise ValueError("Uploaded PDF is empty.")

    pdf = fitz.open(
        stream=pdf_bytes,
        filetype="pdf"
    )

    text = ""

    for page in pdf:
        text += page.get_text()

    pdf.close()

    return text