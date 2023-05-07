# Document Summarizer

This project is a simple yet powerful document summarizer, utilizing OpenAI's GPT-4 and langchain to generate summaries from input text files. The application is built using Streamlit and provides an easy-to-use interface for uploading documents and obtaining concise, coherent summaries.

## Installation

To install the necessary dependencies for this project, follow these steps:

1. Clone this repository to your local machine.

2. Navigate to the cloned repository.

3. Create a virtual environment to manage your dependencies.

4. Activate the virtual environment.

5. Install the dependencies from the `requirements.txt` file.


## Usage

To run the Streamlit application, execute the following command in your terminal:

streamlit run main.py


This will start a local development server. Open the provided URL in your web browser to access the application.

## File Structure

- `main.py`: The main Streamlit application file.
- `utils.py`: Contains utility functions for document loading, summarizing, and token splitting.
- `my_prompts.py`: Contains the prompt templates used by GPT-4 for summarization.
- `requirements.txt`: Lists the required Python packages and their respective versions.

## License

This project is licensed under the terms of the MIT License.
