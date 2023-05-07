import os
import ebooklib
import textract
from ebooklib import epub
from PyPDF2 import PdfFileReader
from docx import Document


def convert_docx_to_text(file_path):
    doc = Document(file_path)
    text = '\n'.join([para.text for para in doc.paragraphs])
    return text


def convert_pdf_to_text(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PdfFileReader(file)
        text = ''
        for page_num in range(pdf_reader.getNumPages()):
            text += pdf_reader.getPage(page_num).extract_text()
    return text


def convert_epub_to_text(file_path):
    book = epub.read_epub(file_path)
    content = ''
    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        content += item.get_content().decode('utf-8')
    return content


def convert_file_to_text(file_path):
    _, extension = os.path.splitext(file_path)
    extension = extension.lower()

    if extension == '.docx':
        return convert_docx_to_text(file_path)
    elif extension == '.pdf':
        return convert_pdf_to_text(file_path)
    elif extension == '.epub':
        return convert_epub_to_text(file_path)
    else:
        raise ValueError(f'Unsupported file extension: {extension}')


def save_text_to_file(text, output_file):
    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write(text)



