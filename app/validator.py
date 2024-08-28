from typing import List

from utils import count_tokens


class Validator:

    MAX_TOKENS = 1_000_000

    @staticmethod
    def validate_text(text: str) -> List[str]:
        errors = []

        if not text:
            errors.append("No text found.")
            return errors

        elif count_tokens(text) > Validator.MAX_TOKENS:
            errors.append(
                "The text is too large. Please provide a text with fewer than 1,000,000 tokens."
            )

        return errors
