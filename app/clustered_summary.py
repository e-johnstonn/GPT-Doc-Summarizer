from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List

import numpy as np
from sklearn.cluster import KMeans

from magic import Magician
from utils import count_tokens


class ClusteredSummary(Magician):

    MIN_CHUNK_SIZE = 50_000
    NUM_CLUSTERS = 8
    MAX_THREADS = 4

    SUMMARIZE_CHUNK_SYSTEM_MESSAGE = """
    You will be given a single section from a %s. This will be enclosed in triple backticks.
    Please provide a comprehensive and cohesive summary of the excerpt, focusing on the key points and main ideas, while maintaining clarity and conciseness."""

    SUMMARIZE_ALL_CHUNKS_SYSTEM_MESSAGE = """
    You will be given a list of summaries from a %s. They will be enclosed in triple backticks.
    Please provide a cohesive summary of the %s, focusing on the key points and main ideas, while maintaining clarity and conciseness.
    
    Format your summary in HTML. It should be structured as follows:
    
    - A short, bullet form list of key takeaways.
    - A well-formatted easy-to-read synopsis, structured like an essay that summarizes the document cohesively.
    - A conclusion that ties all the ideas together.
    
    Format for maximum readability and clarity.
    """

    def __init__(self, text: str, media_type: str):
        super().__init__()
        self.text = text
        self.media_type = media_type

    def get_summary(self) -> str:
        text_chunks = self.chunk_text()
        clustered_chunks = self.cluster_chunks(text_chunks)
        summaries = [None] * len(clustered_chunks)

        with ThreadPoolExecutor(max_workers=self.MAX_THREADS) as executor:
            future_to_index = {
                executor.submit(self.get_summary_for_chunk, chunk): i
                for i, chunk in enumerate(clustered_chunks)
            }
            for future in as_completed(future_to_index):
                index = future_to_index[future]
                summaries[index] = future.result()

        system_message = self.SUMMARIZE_ALL_CHUNKS_SYSTEM_MESSAGE % (
            self.media_type,
            self.media_type,
        )
        user_message = "\n".join([f"'''{summary}'''" for summary in summaries])
        full_summary = self.wave_wand(system_message, user_message)

        return self.extract_code(full_summary)

    def get_summary_for_chunk(self, chunk):
        system_message = self.SUMMARIZE_CHUNK_SYSTEM_MESSAGE % self.media_type
        user_message = f"'''{chunk}'''"
        return self.wave_wand(system_message, user_message)

    def chunk_text(self):
        total_tokens = count_tokens(self.text)
        min_chunk_size = min(self.MIN_CHUNK_SIZE, total_tokens // 2)
        num_chunks = max(1, total_tokens // min_chunk_size)
        chunk_size = total_tokens // num_chunks
        avg_token_length = len(self.text) // total_tokens
        chunk_size_in_chars = chunk_size * avg_token_length
        text_chunks = self._split_text_by_characters(self.text, chunk_size_in_chars)

        return text_chunks

    def cluster_chunks(self, chunks: List[str]) -> List[str]:
        if len(chunks) < self.NUM_CLUSTERS:
            return chunks

        embeddings = [self.create_magic_numbers(chunk)[chunk] for chunk in chunks]
        embeddings_matrix = np.array(embeddings)

        kmeans = KMeans(n_clusters=self.NUM_CLUSTERS, random_state=42).fit(
            embeddings_matrix
        )

        closest_chunks = []
        for cluster_idx in range(self.NUM_CLUSTERS):
            cluster_center = kmeans.cluster_centers_[cluster_idx]
            distances = np.linalg.norm(embeddings_matrix - cluster_center, axis=1)
            closest_chunk_idx = np.argmin(distances)
            closest_chunks.append(chunks[closest_chunk_idx])

        return closest_chunks

    def _split_text_by_characters(
        self, text: str, chunk_size_in_chars: int
    ) -> List[str]:
        chunks = []
        start = 0

        while start < len(text):
            end = start + chunk_size_in_chars

            if end < len(text):
                end = text.rfind(" ", start, end) + 1

            if end <= start:
                end = start + chunk_size_in_chars

            chunks.append(text[start:end].strip())
            start = end

        return chunks
