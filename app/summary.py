from magic import Magician


class Summary(Magician):

    SUMMARIZE_SYSTEM_MESSAGE = """
    You will be given a complete %s. It will be enclosed in triple backticks.
    Please provide a comprehensive and cohesive summary of the %s, focusing on the key points and main ideas, while maintaining clarity and conciseness.

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

        system_message = self.SUMMARIZE_SYSTEM_MESSAGE % (
            self.media_type,
            self.media_type,
        )
        user_message = f"'''{self.text}'''"
        full_summary = self.wave_wand(system_message, user_message)

        return self.extract_code(full_summary)
