import os
import tempfile
import streamlit as st

from langchain.chat_models import ChatOpenAI
from utils import (
    doc_loader, auto_summary_builder, check_key_validity, summary_prompt_creator, check_gpt_4,
    token_limit, token_minimum
)
from my_prompts import map_prompt, combine_prompt
from file_conversions import pdf_to_text


def main():
    st.title("Document Summarizer")
    uploaded_file = st.file_uploader("Upload a document to summarize, 10k to 100k tokens works best!", type=['txt', 'pdf'])
    api_key = st.text_input("Free usage cap has been hit! Enter your own API key here, or contact the author if you don't have one.")
    st.markdown('[Author email](ethanujohnston@gmail.com)')
    use_gpt_4 = st.checkbox("Use GPT-4 for the final prompt (STRONGLY recommended, requires GPT-4 API access)", value=True)

    st.sidebar.markdown('# Made by: [Ethan](https://github.com/e-johnstonn)')
    st.sidebar.markdown('# Git link: [Docsummarizer](https://github.com/e-johnstonn/docsummarizer)')

    if st.button('Summarize (click once and wait)'):
        process_summarize_button(uploaded_file, api_key, use_gpt_4)


def process_summarize_button(uploaded_file, api_key, use_gpt_4):
    if not validate_input(uploaded_file, api_key, use_gpt_4):
        return

    with st.spinner("Summarizing... please wait..."):
        temp_file_path = create_temp_file(uploaded_file)
        llm = create_chat_model(api_key, use_gpt_4)
        initial_chain = summary_prompt_creator(map_prompt, 'text', llm)
        final_prompt_list = summary_prompt_creator(combine_prompt, 'text', llm)
        doc = doc_loader(temp_file_path)

        if not validate_doc_size(doc):
            os.unlink(temp_file_path)
            return

        summary = auto_summary_builder(doc, 10, initial_chain, final_prompt_list, api_key, use_gpt_4)
        st.markdown(summary, unsafe_allow_html=True)
        os.unlink(temp_file_path)


def validate_input(uploaded_file, api_key, use_gpt_4):
    if uploaded_file is None:
        st.warning("Please upload a file.")
        return False

    if not check_key_validity(api_key):
        st.warning('Key not valid or API is down.')
        return False

    if use_gpt_4 and not check_gpt_4(api_key):
        st.warning('Key not valid for GPT-4.')
        return False

    return True


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


def validate_doc_size(doc):
    if not token_limit(doc, 120000):
        st.warning('File too big!')
        return False

    if not token_minimum(doc, 200):
        st.warning('File too small!')
        return False
    return True

if __name__ == '__main__':
    main()

