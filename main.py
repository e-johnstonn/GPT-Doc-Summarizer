import os
import streamlit as st

from utils import (
    doc_loader, summary_prompt_creator, doc_to_final_summary,
)
from my_prompts import file_map, file_combine
from streamlit_app_utils import \
    check_gpt_4, \
    check_openai_key_validity, \
    check_elevenlabs_key_validity, \
    create_temp_file, \
    create_chat_model, \
    token_limit, \
    token_minimum

from utils import transcript_loader


def main():
    """
    The main function for the Streamlit app.

    :return: None.
    """
    st.title("Custom Audiobook")

    openai_api_key = st.text_input("Enter OpenAI API key here")
    use_gpt_4 = True #st.checkbox("Use GPT-4 for the final prompt (STRONGLY recommended, requires GPT-4 API access - progress bar will appear to get stuck as GPT-4 is slow)", value=True)
    elevenlabs_api_key = st.text_input("Enter ElevenLabs API key here")
    uploaded_file = st.file_uploader("Upload a Plain Text UTF-8 file from Project Gutenberg", type=['txt'])
    
    st.sidebar.markdown('# Made by: [Yornoc](https://github.com/conroywhitney)')
    st.sidebar.markdown('# OpenSource: [GitHub Link](https://github.com/conroywhitney/yornoc-lablabai-elevenlabs)')
    st.sidebar.markdown('# For the [LabLab/ElevenLabs Hackathon](https://lablab.ai/event/eleven-labs-ai-hackathon)')
    st.sidebar.markdown("""<small>It's always good practice to verify that a website is safe before giving it your API key. 
                        This site is open source, so you can check the code yourself, or run the streamlit app locally.</small>""", unsafe_allow_html=True)

    if st.button('Generate Audiobook'):
        process_summarize_button(uploaded_file, openai_api_key, use_gpt_4, elevenlabs_api_key)

def process_summarize_button(file_or_transcript, openai_api_key, use_gpt_4, elevenlabs_api_key, file=True):
    """
    Processes the summarize button, and displays the summary if input and doc size are valid

    :param file_or_transcript: The file uploaded by the user or the transcript from the YouTube URL

    :param openai_api_key: The OpenAI API key entered by the user

    :param use_gpt_4: Whether to use GPT-4 or not

    :param elevenlabs_api_key: The ElevenLabs API key entered by the user

    :return: None
    """
    if not validate_input(file_or_transcript, openai_api_key, use_gpt_4, elevenlabs_api_key):
        return

    with st.spinner("Generating... please wait..."):
        temp_file_path = create_temp_file(file_or_transcript)
        doc = doc_loader(temp_file_path)
        map_prompt = file_map
        combine_prompt = file_combine

        llm = create_chat_model(openai_api_key, use_gpt_4)
        initial_prompt_list = summary_prompt_creator(map_prompt, 'text', llm)
        final_prompt_list = summary_prompt_creator(combine_prompt, 'text', llm)

        if not validate_doc_size(doc):
            if file:
                os.unlink(temp_file_path)
            return

        if elevenlabs_api_key:
            summary = doc_to_final_summary(doc, 10, initial_prompt_list, final_prompt_list, openai_api_key, use_gpt_4, elevenlabs_api_key)

        else:
            summary = doc_to_final_summary(doc, 10, initial_prompt_list, final_prompt_list, openai_api_key, use_gpt_4)

        st.markdown(summary, unsafe_allow_html=True)
        if file:
            os.unlink(temp_file_path)


def validate_doc_size(doc):
    """
    Validates the size of the document

    :param doc: doc to validate

    :return: True if the doc is valid, False otherwise
    """
    if not token_limit(doc, 800000):
        st.warning('File or transcript too big!')
        return False

    if not token_minimum(doc, 2000):
        st.warning('File or transcript too small!')
        return False
    return True


def validate_input(file_or_transcript, openai_api_key, use_gpt_4, elevenlabs_api_key):
    """
    Validates the user input, and displays warnings if the input is invalid

    :param file_or_transcript: The file uploaded by the user or the YouTube URL entered by the user

    :param openai_api_key: The OpenAI API key entered by the user

    :param use_gpt_4: Whether the user wants to use GPT-4

    :param elevenlabs_api_key: The ElevenLabs API key entered by the user

    :return: True if the input is valid, False otherwise
    """
    if file_or_transcript == None:
        st.warning("Please upload a TXT file from Project Gutenberg")
        return False

    if not check_openai_key_validity(openai_api_key):
        st.warning('OpenAI Key not valid or API is down.')
        return False

    if use_gpt_4 and not check_gpt_4(openai_api_key):
        st.warning('Key not valid for GPT-4.')
        return False
    
    if not check_elevenlabs_key_validitiy(elevenlabs_api_key):
        st.warning('ElevenLabs Key not valid or API is down.')
        return False

    return True


if __name__ == '__main__':
    main()

