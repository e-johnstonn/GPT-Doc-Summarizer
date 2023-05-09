import tempfile

import PyPDF2
import pdfplumber
from io import StringIO
import re

from langchain.chat_models import ChatOpenAI

from utils import doc_to_text, token_counter


def pdf_to_text(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = StringIO()
    for i in range(len(pdf_reader.pages)):
        p = pdf_reader.pages[i]
        text.write(p.extract_text())
    return text.getvalue().encode('utf-8')


# attempt at auto - extracting table of contents
# def find_toc_page(file_path):
#     with pdfplumber.open(file_path) as pdf:
#         for i, page in enumerate(pdf.pages):
#             text = page.extract_text()
#             if re.search(r'\bTable of Contents\b', text, re.IGNORECASE):
#                 return i
#         return None
#
#
# def extract_toc(file_path, toc_page_num):
#     toc = []
#     with pdfplumber.open(file_path) as pdf:
#         text = pdf.pages[toc_page_num].extract_text()
#         for line in text.split('\n'):
#             match = re.match(r'([\w\s\d,.:;-]+)', line)
#             if match:
#                 title = match.group().strip()
#                 toc.append(title)
#     return toc
#
#
# def extract_sections(file_path, toc):
#     sections = {}
#     current_section = ""
#     with pdfplumber.open(file_path) as pdf:
#         for page in pdf.pages:
#             text = page.extract_text()
#             for line in text.split('\n'):
#                 # Check if the line is one of the section titles
#                 if line.strip() in toc:
#                     current_section = line.strip()
#                     sections[current_section] = ""
#                 # Append the text to the current section
#                 elif current_section:
#                     sections[current_section] += f"{line}\n"
#     return sections


def check_gpt_4(api_key):
    try:
        ChatOpenAI(openai_api_key=api_key, model_name='gpt-4').call_as_llm('Hi')
        print('User has GPT-4 access')
        return True
    except Exception as e:
        print('No GPT-4 access')
        return False


def token_limit(doc, maximum: 200000): #checks how many tokens are in a doc, returns false if it exceeds the limit set
    text = doc_to_text(doc)
    count = token_counter(text)
    if count > maximum:
        return False
    return True


def token_minimum(doc, minimum:2000):
    text = doc_to_text(doc)
    count = token_counter(text)
    if count < minimum:
        return False
    return True


def check_key_validity(api_key):
    try:
        ChatOpenAI(openai_api_key=api_key).call_as_llm('Hi')
        print('API Key is valid')
        return True
    except Exception as e:
        print('API key is invalid or OpenAI is having issues.')
        print(e)
        return False


def create_temp_file(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as temp_file:
        if uploaded_file.type == 'application/pdf':
            temp_file.write(pdf_to_text(uploaded_file))
        else:
            temp_file.write(uploaded_file.getvalue())
    return temp_file.name


def create_chat_model(api_key, use_gpt_4):
    if use_gpt_4:
        return ChatOpenAI(openai_api_key=api_key, temperature=0, max_tokens=500, model_name='gpt-3.5-turbo')
    else:
        return ChatOpenAI(openai_api_key=api_key, temperature=0, max_tokens=250, model_name='gpt-3.5-turbo')



