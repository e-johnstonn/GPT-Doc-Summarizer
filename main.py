import streamlit as st
import os
import tempfile

import openai

from langchain.chat_models import ChatOpenAI

from file_conversions import convert_file_to_text
from utils import doc_loader, auto_summary_builder, check_key_validity, summary_prompt_creator
from my_prompts import map_prompt, combine_prompt


st.title("Document Summarizer")
uploaded_file = st.file_uploader("Upload a document to summarize, 10k to 100k tokens works best!", type=['txt', 'pdf', 'epub', 'docx'])
api_key = st.text_input("Enter your API key here")
use_gpt_4 = st.checkbox("Use GPT-4 for the final prompt (recommended, requires GPT-4 API access)")

st.sidebar.markdown('# Made by: [Ethan](https://github.com/e-johnstonn)')
st.sidebar.markdown('# Git link: [Docsummarizer](https://github.com/e-johnstonn/docsummarizer)')

if st.button("Summarize"):
    valid = check_key_validity(api_key)
    if uploaded_file is not None and valid is True:
        with st.spinner("Summarizing... please wait..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix='.txt',) as temp_file:
                file_name, file_extension = os.path.splitext(uploaded_file.name)
                if file_extension != '.txt':
                    text = convert_file_to_text(uploaded_file)
                    temp_file.write(text)
                    temp_file_path = temp_file.name
                else:
                    temp_file.write(uploaded_file.getvalue())
                    temp_file_path = temp_file.name
            if use_gpt_4:
                llm = ChatOpenAI(openai_api_key=api_key, temperature=0, max_tokens=500, model_name='gpt-3.5-turbo')
            else:
                llm = ChatOpenAI(openai_api_key=api_key, temperature=0, max_tokens=250, model_name='gpt-3.5-turbo')
            initial_chain = summary_prompt_creator(map_prompt, 'text', llm)
            final_prompt_list = summary_prompt_creator(combine_prompt, 'text', llm)
            doc = doc_loader(temp_file_path)
            summary = auto_summary_builder(doc, 10, initial_chain, final_prompt_list, api_key, use_gpt_4)
            st.write(summary)
            os.unlink(temp_file_path)
    elif uploaded_file is None:
        st.warning("Please upload a .txt file.")
    else:
        st.warning(check_key_validity(api_key))

