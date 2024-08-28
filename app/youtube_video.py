import urllib
from typing import List, Optional
from urllib.parse import urlparse, parse_qs

from youtube_transcript_api import YouTubeTranscriptApi


class YouTubeVideo:

    def __init__(self, video_url: str):
        self.video_url = video_url
        self.video_id = self.get_youtube_video_id()

    def get_transcript(self) -> Optional[str]:
        transcript = YouTubeTranscriptApi.get_transcript(self.video_id)
        if not transcript:
            return None
        return self.transcript_to_plain_text(transcript)

    def get_youtube_video_id(self) -> str:
        query = urlparse(self.video_url)
        if query.hostname == "youtu.be":
            return query.path[1:]
        if query.hostname in ("www.youtube.com", "youtube.com"):
            if query.path == "/watch":
                return parse_qs(query.query)["v"][0]
            if query.path[:7] == "/embed/":
                return query.path.split("/")[2]
            if query.path[:3] == "/v/":
                return query.path.split("/")[2]
        raise ValueError("Invalid YouTube URL")

    @staticmethod
    def transcript_to_plain_text(transcript: List[dict]) -> str:
        return " ".join([entry["text"] for entry in transcript])
