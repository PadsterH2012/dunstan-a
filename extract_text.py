import fitz  # PyMuPDF
import re
import requests

OLLAMA_URL = "http://10.203.20.99:11434/api/generate"
OLLAMA_MODEL = "llama3:8b-instruct-q8_0"

def extract_text_from_pdf(pdf_path):
    document = fitz.open(pdf_path)
    text = ""
    for page_num in range(document.page_count):
        page = document.load_page(page_num)
        text += page.get_text()
    return text

def process_text_with_ai(text):
    sections = split_into_sections(text)
    rules = []
    for section in sections:
        payload = {
            "model": OLLAMA_MODEL,
            "input": f"Extract rules from the following text:\n\n{section}"
        }
        response = requests.post(OLLAMA_URL, json=payload)
        if response.status_code == 200:
            result = response.json()
            rules.append(result.get('response', ''))
    return rules

def split_into_sections(text):
    headings = re.split(r'\n[A-Z ]+\n', text)
    sections = [heading.strip() for heading in headings if heading.strip()]
    return sections
