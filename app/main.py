import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile

from clustered_summary import ClusteredSummary
from pdf_document import PdfDocument
from summary import Summary
from utils import count_tokens
from validator import Validator
from youtube_video import YouTubeVideo


def main():
    st.title("Document Summarizer")

    input_method = st.radio(
        "Select input method", ("Upload a document", "Enter a YouTube URL")
    )

    if input_method == "Upload a document":
        uploaded_file = st.file_uploader(
            "Upload a document",
            type=["pdf"],
        )

    if input_method == "Enter a YouTube URL":
        youtube_url = st.text_input("Enter a YouTube URL")

    st.sidebar.markdown("# [Contact me by email!](mailto:ethanujohnston@gmail.com)")
    st.sidebar.markdown(
        "# [Check out my other projects!](https://github.com/e-johnstonn)"
    )
    st.sidebar.markdown("# [Twitter / X](https://x.com/ethanjdev)")

    if st.button("Summarize"):
        if input_method == "Upload a document":
            if uploaded_file is None:
                st.warning("Please upload a file.")
                return
            summarize_file(uploaded_file)

        else:
            if not youtube_url:
                st.warning("Please enter a YouTube URL.")
                return
            summarize_youtube(youtube_url)


def summarize_file(uploaded_file: UploadedFile):
    document = PdfDocument(uploaded_file)
    validation_errors = Validator.validate_text(document.text_content)

    if validation_errors:
        st.warning(f"Invalid input: {','.join(validation_errors)}")
        return

    st.markdown(run_summary(document.text_content, f"document"), unsafe_allow_html=True)


def summarize_youtube(youtube_url: str):
    video = YouTubeVideo(youtube_url)
    transcript = video.get_transcript()
    validation_errors = Validator.validate_text(transcript)

    if validation_errors:
        st.warning(validation_errors)
        return

    st.markdown(run_summary(transcript, "youtube video"), unsafe_allow_html=True)


def run_summary(text: str, media_type: str):
    tokens = count_tokens(text)

    if tokens > 100_000:
        return ClusteredSummary(text, media_type).get_summary()
    else:
        return Summary(text, media_type).get_summary()


if __name__ == "__main__":
    main()
