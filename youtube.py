from langchain.document_loaders import YoutubeLoader


def transcript_loader(video_url):
    """
    Load the transcript of a YouTube video into a loaded langchain Document object.

    :param video_url: The URL of the YouTube video to load the transcript of.

    :return: A loaded langchain Document object.
    """
    transcript = YoutubeLoader.from_youtube_url(video_url)
    loaded = transcript.load()
    return loaded

