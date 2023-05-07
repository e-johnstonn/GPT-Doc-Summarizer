map_prompt = """
You will be given a single section from a text. This will be enclosed in triple backticks.
Please provide a cohesive summary of the following section excerpt, focusing on the key points and main ideas, while maintaining clarity and conciseness.

'''{text}'''

FULL SUMMARY:
"""


combine_prompt = """
Combine the provided section summaries into a cohesive, well-formatted, and easy-to-read final summary. 
The section summaries will be enclosed in triple backticks. 
Ensure all important details from each section are included and presented in a clear and comprehensive manner.

'''{text}'''

FULL VERBOSE SUMMARY:
"""

