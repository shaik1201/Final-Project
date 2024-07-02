import fitz

def extract_text(file):
    try:
        doc = fitz.open(stream=file.read(), filetype="pdf")
        text = ""
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text()
        return text
    except Exception as e:
        print(f"Failed to extract text from PDF: {str(e)}")
        return None