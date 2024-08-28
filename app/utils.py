import tiktoken


def count_tokens(text: str) -> int:
    encoding = tiktoken.get_encoding("cl100k_base")
    token_list = encoding.encode(text, disallowed_special=())
    return len(token_list)
