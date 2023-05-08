import PyPDF2
import pdfplumber
from io import StringIO
import re



def pdf_to_text(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = StringIO()
    for i in range(len(pdf_reader.pages)):
        p = pdf_reader.pages[i]
        text.write(p.extract_text())
    return text.getvalue().encode('utf-8')


def find_toc_page(file_path):
    with pdfplumber.open(file_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if re.search(r'\bTable of Contents\b', text, re.IGNORECASE):
                return i
        return None


def extract_toc(file_path, toc_page_num):
    toc = []
    with pdfplumber.open(file_path) as pdf:
        text = pdf.pages[toc_page_num].extract_text()
        for line in text.split('\n'):
            match = re.match(r'([\w\s\d,.:;-]+)', line)
            if match:
                title = match.group().strip()
                toc.append(title)
    return toc


def extract_sections(file_path, toc):
    sections = {}
    current_section = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            for line in text.split('\n'):
                # Check if the line is one of the section titles
                if line.strip() in toc:
                    current_section = line.strip()
                    sections[current_section] = ""
                # Append the text to the current section
                elif current_section:
                    sections[current_section] += f"{line}\n"
    return sections

