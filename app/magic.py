import re
from typing import Dict, List

import openai


class Magician:
    MAGIC_WAND = "gpt-4o-mini"
    OTHER_MAGIC_WAND = "text-embedding-3-small"

    def __init__(self):
        self.client = openai.OpenAI()

    def wave_wand(self, system_message: str, user_message: str) -> str:
        return (
            self.client.chat.completions.create(
                model=self.MAGIC_WAND,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message},
                ],
            )
            .choices[0]
            .message.content
        )

    def create_magic_numbers(self, text: str) -> Dict[str, List[float]]:
        response = self.client.embeddings.create(
            input=text,
            model=self.OTHER_MAGIC_WAND,
        )
        return {text: response.data[0].embedding}

    @staticmethod
    def extract_code(markdown_text: str) -> str:
        cleaned_text = re.sub(
            r"```[\w]*\n(.*?)```", r"\1", markdown_text, flags=re.DOTALL
        ).replace("\n", "")

        return cleaned_text
