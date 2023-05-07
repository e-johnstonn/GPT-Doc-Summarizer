# Document Summarizer

This project is a simple yet powerful document summarizer, utilizing OpenAI's GPT-4 and langchain to generate summaries from input text files. The application is built using Streamlit and provides an easy-to-use interface for uploading documents and obtaining concise, coherent summaries.

The methods in utils.py provide a way to automatically summarize long documents using vector embeddings and clustering techniques. It breaks down the document into smaller chunks, clusters the chunks, and selects representative chunks to create a summary. This is done with the help of OpenAI's GPT models, which are fine-tuned for summarization tasks.

# How it works
The program uses the following steps to summarize long documents:

Split the document: The input document is split into smaller chunks based on a token limit using the token_splitter function. This ensures that each chunk is small enough for further processing.

Calculate embeddings: The embed_docs function calculates the vector embeddings of each document chunk using OpenAI's GPT models. These embeddings capture the semantic meaning of the chunks.

Cluster the chunks: The KMeans clustering algorithm is applied to the embeddings using the kmeans_clustering function. The number of clusters is specified by the user.

Select representative chunks: The get_closest_vectors function selects the chunk with the closest vector to the centroid of each cluster. This results in a set of representative chunks for the document.

Summarize the chunks: The summary_from_summary_docs function summarizes the representative chunks using GPT 3.5. These chunks are then given to GPT-4 for a final cohesive summary of the overall document. The summarization is performed by creating a summary chain with the summarize_chain_creator function.




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
