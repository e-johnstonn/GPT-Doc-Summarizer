file_map = """
You will be given a single section from a text. This will be enclosed in triple backticks.
Please provide a cohesive summary of the following section excerpt, focusing on the key points and main ideas, while maintaining clarity and conciseness.

'''{text}'''

FULL SUMMARY:
"""


file_combine = """
Read all the provided summaries from a larger document. They will be enclosed in triple backticks. 
Determine what the overall document is about and summarize it with this information in mind.
Synthesize the info into a well-formatted easy-to-read synopsis, structured like an essay that summarizes them cohesively. 
Do not simply reword the provided text. Do not copy the structure from the provided text.
Avoid repetition. Connect all the ideas together.
Preceding the synopsis, write a short, bullet form list of key takeaways.
Format in HTML. Text should be divided into paragraphs. Paragraphs should be indented. 

'''{text}'''


"""

youtube_map = """
You will be given a single section from a transcript of a youtube video. This will be enclosed in triple backticks.
Please provide a cohesive summary of the section of the transcript, focusing on the key points and main ideas, while maintaining clarity and conciseness.

'''{text}'''

FULL SUMMARY:
"""


youtube_combine = """
Read all the provided summaries from a youtube transcript. They will be enclosed in triple backticks.
Determine what the overall video is about and summarize it with this information in mind. 
Synthesize the info into a well-formatted easy-to-read synopsis, structured like an essay that summarizes them cohesively. 
Do not simply reword the provided text. Do not copy the structure from the provided text.
Avoid repetition. Connect all the ideas together.
Preceding the synopsis, write a short, bullet form list of key takeaways.
Format in HTML. Text should be divided into paragraphs. Paragraphs should be indented. 

'''{text}'''


"""

pn_map = """
You will be given a single section from a text. This will be enclosed in triple backticks.
Please provide a progress note for the patient for this therapy session of the following section excerpt, create something that make sense to enter into an EMR while maintaining clarity and conciseness.

'''{text}'''

FULL SUMMARY:
"""


pn_combine = """
Read all the provided summarized progress notes from a larger document. They will be enclosed in triple backticks. 
Determine what the overall progress note is about and create a shorter progress note from it.
Synthesize the info into a well-formatted, easy-to-read, structured it like a typical progress note for a therapy patient.
Do not simply reword the provided text. Do not copy the structure from the provided text.
Avoid repetition. Connect all the ideas together.
Preceding the progress note, write a short, bullet form list of key takeaways.
Format in HTML. Text should be divided into paragraphs. Paragraphs should be indented. 

'''{text}'''


"""

ppve_combine = """
Read all the provided summarized progress notes from a larger document. They will be enclosed in triple backticks. 
Determine what the overall progress note is about and create a post visit email for the patient. Include action items for the patient if it make sense.
Target less than 100 words. Use friendly language. Target 5th grade reading level. 
Do not simply reword the provided text. Do not copy the structure from the provided text.
Avoid repetition. Connect all the ideas together.
Format in HTML. 

'''{text}'''


"""

superbill_combine = """
Read all the provided summarized progress notes from a larger document. They will be enclosed in triple backticks. 
Determine what the overall progress note is about and create a superbill for the patient so the patient can submit for insurance claim purposes.
Synthesize the info into a well-formatted, easy-to-read, structured it like a typical superbill for a therapy patient.
Make it professional.
Do not simply reword the provided text. Do not copy the structure from the provided text.
Avoid repetition. Connect all the ideas together.

'''{text}'''


"""

claims_combine = """
Read all the provided summarized progress notes from a larger document. They will be enclosed in triple backticks. 
Determine what the overall progress note is about and create a claims email from the psychiatrist to the patient's insurance company for reimbursement.
Synthesize the info into a well-formatted, easy-to-read, structured it like a typical claims email for a therapy session.
Make it professional.
Do not simply reword the provided text. Do not copy the structure from the provided text.
Avoid repetition. Connect all the ideas together.

'''{text}'''


"""