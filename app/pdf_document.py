import io
import PyPDF2


class PdfDocument:
    def __init__(self, pdf_bytes: io.BytesIO):
        self.pdf_bytes = pdf_bytes
        self._text_content = None

    @property
    def text_content(self) -> str:
        if self._text_content:
            return self._text_content
        pdf_reader = PyPDF2.PdfReader(self.pdf_bytes)
        text = ""
        for i in range(len(pdf_reader.pages)):
            p = pdf_reader.pages[i]
            text += p.extract_text()
        self._text_content = text
        return self.sanitize_text(text)

    @staticmethod
    def sanitize_text(text: str) -> str:
        special_tokens = [
            ">|endoftext|",
            "<|fim_prefix|",
            "<|fim_middle|",
            "<|fim_suffix|",
            "<|endofprompt|>",
        ]
        for special in special_tokens:
            text = text.replace(special, "")
        return text
