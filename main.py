import os
import streamlit as st
from streamlit_option_menu import option_menu
from st_on_hover_tabs import on_hover_tabs

from utils import (
    doc_loader, summary_prompt_creator, doc_to_final_summary,
)
from my_prompts import file_map, file_combine, youtube_map, youtube_combine, pn_map, pn_combine, ppve_combine, superbill_combine
from streamlit_app_utils import check_gpt_4, check_key_validity, create_temp_file, create_chat_model, \
    token_limit, token_minimum

from utils import transcript_loader



def main():
    """
    The main function for the Streamlit app.

    :return: None.
    """

    st.set_page_config(layout="wide")
    st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)

    with st.sidebar:
        tabs = on_hover_tabs(tabName=['Dashboard', 'Patient Portal', 'Revenue Report'], 
                            iconName=['dashboard', 'economy', 'money'], default_choice=0)

    if tabs =='Dashboard':
        st.title("IrisMed's Private Practice Assistant")
        # st.write('Name of option is {}'.format(tabs))

    elif tabs == 'Patient Portal':
        st.title("Patient Portal")
        st.write('Name of option is {}'.format(tabs))

    elif tabs == 'Revenue Report':
        st.title("Revenue Report")
        st.write('Name of option is {}'.format(tabs))
        

    input_method = st.radio("Select input method", ('Upload a document', 'Enter a Video URL'))

    if input_method == 'Upload a document':
        # uploaded_file = st.file_uploader("Upload a document to summarize, 10k to 100k tokens works best!", type=['txt', 'pdf'])
        uploaded_file = st.file_uploader("Upload a session transcript to process.", type=['txt', 'pdf'])

    if input_method == 'Enter a Video URL':
        youtube_url = st.text_input("Enter a Video URL to process")

    with st.expander("Credential Options"):
        api_key = st.text_input("Enter API key here.")
    st.markdown('[Contact Support](mailto:han@irismed.co)')
    with st.expander("Advanced Options"):
        use_gpt_4 = st.checkbox("Use GPT-4 for the final prompt (STRONGLY recommended, requires GPT-4 API access - progress bar will appear to get stuck as GPT-4 is slow)", value=True)
        find_clusters = st.checkbox('Find optimal clusters (experimental, could save on token usage)', value=False)
    # st.sidebar.markdown('### Made by: [IrisMed](https://irismed.co)')
    # st.sidebar.markdown("""Private Practice's Back Office Digital Assitant. We are here to reduce documentation burden for your awesome practice.""", unsafe_allow_html=True)


    if st.button('Process (click once and wait)'):
        if input_method == 'Upload a document':
            process_summarize_button(uploaded_file, api_key, use_gpt_4, find_clusters)

        else:
            doc = transcript_loader(youtube_url)
            process_summarize_button(doc, api_key, use_gpt_4, find_clusters, file=False)
    # if tabs =='Dashboard':
    #     st.write('Name of option is {}'.format(tabs))


def process_summarize_button(file_or_transcript, api_key, use_gpt_4, find_clusters, file=True):
    """
    Processes the summarize button, and displays the summary if input and doc size are valid

    :param file_or_transcript: The file uploaded by the user or the transcript from the YouTube URL

    :param api_key: The API key entered by the user

    :param use_gpt_4: Whether to use GPT-4 or not

    :param find_clusters: Whether to find optimal clusters or not, experimental

    :return: None
    """
    if not validate_input(file_or_transcript, api_key, use_gpt_4):
        return

    with st.spinner("Summarizing... please wait..."):
        if file:
            temp_file_path = create_temp_file(file_or_transcript)
            doc = doc_loader(temp_file_path)
            map_prompt = file_map
            combine_prompt = file_combine
            
            map_pn_prompt = pn_map
            combine_pn_prompt = pn_combine
            combine_ppve_prompt = ppve_combine
            combine_superbill_prompt = superbill_combine

        else:
            doc = file_or_transcript
            map_prompt = youtube_map
            combine_prompt = youtube_combine
            
            map_pn_prompt = pn_map
            combine_pn_prompt = pn_combine
            combine_ppve_prompt = ppve_combine
            combine_superbill_prompt = superbill_combine

        llm = create_chat_model(api_key, use_gpt_4)
        initial_prompt_list = summary_prompt_creator(map_prompt, 'text', llm)
        final_prompt_list = summary_prompt_creator(combine_prompt, 'text', llm)

        initial_pn_prompt_list = summary_prompt_creator(map_pn_prompt, 'text', llm)
        final_pn_prompt_list = summary_prompt_creator(combine_pn_prompt, 'text', llm)

        final_ppve_prompt_list = summary_prompt_creator(combine_ppve_prompt, 'text', llm)
        final_superbill_prompt_list = summary_prompt_creator(combine_superbill_prompt, 'text', llm)

        if not validate_doc_size(doc):
            if file:
                os.unlink(temp_file_path)
            return

        if find_clusters:
            summaries = doc_to_final_summary(doc, 10, initial_prompt_list, final_prompt_list, api_key, use_gpt_4, find_clusters)
            summary = summaries['summary']
        else:
            # summaries = doc_to_final_summary(doc, 10, initial_prompt_list, final_prompt_list, api_key, use_gpt_4) # don't need this for now
            # summary = summaries['summary']
            summaries = doc_to_final_summary(doc, 10, initial_pn_prompt_list, final_pn_prompt_list, final_ppve_prompt_list, final_superbill_prompt_list, api_key, use_gpt_4)
            pn_summary = summaries['pn_summary']
            ppve_summary = summaries['ppve_summary']
            superbill_summary = summaries['superbill_summary']

        if pn_summary:
            st.markdown("#### Progress Note", unsafe_allow_html=True)
            st.markdown(pn_summary, unsafe_allow_html=True)
        if ppve_summary:
            st.markdown("#### Post Visit Note")
            st.markdown(ppve_summary, unsafe_allow_html=True)
        if superbill_summary:    
            st.markdown("#### Superbill & Claim Email Example")
            st.markdown(superbill_summary, unsafe_allow_html=True)

        with st.sidebar:
            tabs = on_hover_tabs(tabName=['Progress Note', 'Post Vist Note', 'Superbill'], 
                                iconName=['money', 'money', 'money'], default_choice=0)
            
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


def validate_input(file_or_transcript, api_key, use_gpt_4):
    """
    Validates the user input, and displays warnings if the input is invalid

    :param file_or_transcript: The file uploaded by the user or the YouTube URL entered by the user

    :param api_key: The API key entered by the user

    :param use_gpt_4: Whether the user wants to use GPT-4

    :return: True if the input is valid, False otherwise
    """
    if file_or_transcript == None:
        st.warning("Please upload a file or enter a Video URL.")
        return False

    if not check_key_validity(api_key):
        st.warning('Key not valid or API is down.')
        return False

    if use_gpt_4 and not check_gpt_4(api_key):
        st.warning('Key not valid for GPT-4.')
        return False

    return True


if __name__ == '__main__':
    main()

