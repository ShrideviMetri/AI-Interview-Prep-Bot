
def extract_text_from_pdf(uploaded_file):

    uploaded_file.seek(0)
    pdf_bytes = uploaded_file.getvalue()

    print("Filename:", uploaded_file.name)
    print("File size:", len(pdf_bytes))
    print("First 20 bytes:", pdf_bytes[:20])
    print("PDF header:", pdf_bytes.startswith(b"%PDF-"))

    import fitz

    pdf = fitz.open(stream=pdf_bytes, filetype="pdf")

    text = ""
    for page in pdf:
        text += page.get_text()

    pdf.close()
    return text
