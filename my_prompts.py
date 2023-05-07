map_prompt = """
You will be given a single section from a text. This will be enclosed in triple backticks.
Your goal is to give a summary of the section so that a reader will have a full and complete understanding of it says.
Your response should fully encompass what was covered in the section.

'''{text}'''

FULL SUMMARY:
"""


combine_prompt = """
You will be given a series of summaries of sections from a text. The summaries will be enclosed in triple backticks.
Your goal is to give a verbose, complete summary of the text, fully encompassing the meaning.
The reader should be able to grasp all the main ideas of the article.
Analyze all summaries and write a cohesive summary that ties them all together in a digestable manner. 
Eliminate redundancy. Format in an easy-to-read manner.  
Only use the summaries provided.

'''{text}'''

FULL VERBOSE SUMMARY:
"""

