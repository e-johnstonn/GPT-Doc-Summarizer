map_prompt = """
You will be given a single section from a scholarly article. This will be enclosed in triple backticks.
Your goal is to give a summary of the section so that a reader will have a full understanding of the article says, and the core concepts it describes.
Your response should fully encompass what was covered in the section.

'''{text}'''

FULL SUMMARY:
"""


combine_prompt = """
You will be given a series of summaries of sections from a scholarly article. The summaries will be enclosed in triple backticks.
Your goal is to give a verbose, complete summary of the article, and all key concepts.
The reader should be able to grasp all the main ideas of the article.
Do not simply resummarize each summary provided to you. Analyze them all, and write a cohesive summary that ties them all together in a digestable manner. 
Eliminate redundancy. Format in an easy-to-read manner. Clarify the key concepts. 
Only use the summaries provided.

'''{text}'''

FULL VERBOSE SUMMARY:
"""

