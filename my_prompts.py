map_prompt = """
You will be given a single section from a text. This will be enclosed in triple backticks.
Please provide a cohesive summary of the following section excerpt, focusing on the key points and main ideas, while maintaining clarity and conciseness.

'''{text}'''

FULL SUMMARY:
"""


combine_prompt = """
Read all the provided summaries from a larger document. They will be enclosed in triple backticks. 
Synthesize their info into a well-formatted easy-to-read synopsis, structured like an essay that summarizes their info. 
Do not simply reword the provided text. Do not copy the structure from the provided text.
Avoid repetition. 
Preceding the synopsis, write a short, bullet form list of key takeaways.
Format in HTML. Text should be divided into paragraphs. Paragraphs should be indented. 

'''{text}'''


"""

