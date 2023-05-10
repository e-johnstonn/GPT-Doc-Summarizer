from langchain.document_loaders import TextLoader
from langchain.text_splitter import TokenTextSplitter
from langchain.schema import Document
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain

import streamlit as st

from sklearn.cluster import KMeans

import tiktoken

import numpy as np

from elbow import calculate_inertia, determine_optimal_clusters

import time


def doc_loader(file_path: str):
    """
    Load the contents of a text document from a file path into a loaded langchain Document object.

    :param file_path: The path to the text document to load.

    :return: A langchain Document object.
    """
    loader = TextLoader(file_path, encoding='utf-8')
    return loader.load()


def token_counter(text: str):
    """
    Count the number of tokens in a string of text.

    :param text: The text to count the tokens of.

    :return: The number of tokens in the text.
    """
    encoding = tiktoken.get_encoding('cl100k_base')
    token_list = encoding.encode(text)
    tokens = len(token_list)
    return tokens


def doc_to_text(document):
    """
    Convert a langchain Document object into a string of text.

    :param document: The loaded langchain Document object to convert.

    :return: A string of text.
    """
    text = ''
    for i in document:
        text += i.page_content
    return text


def embed_docs(docs, api_key):
    """
    Embed a list of loaded langchain Document objects into a list of vectors.

    :param docs: A list of loaded langchain Document objects to embed.

    :param api_key: The OpenAI API key to use for embedding.

    :return: A list of vectors.
    """
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    vectors = embeddings.embed_documents([x.page_content for x in docs])
    return vectors


def kmeans_clustering(vectors, num_clusters=None):
    """
    Cluster a list of vectors using K-Means clustering.

    :param vectors: A list of vectors to cluster.

    :param num_clusters: The number of clusters to use. If None, the optimal number of clusters will be determined.

    :return: A K-Means clustering object.
    """
    if num_clusters is None:
        inertia_values = calculate_inertia(vectors)
        num_clusters = determine_optimal_clusters(inertia_values)
        print(f'Optimal number of clusters: {num_clusters}')

    kmeans = KMeans(n_clusters=num_clusters, random_state=42).fit(vectors)
    return kmeans


def get_closest_vectors(vectors, kmeans):
    """
    Get the closest vectors to the cluster centers of a K-Means clustering object.

    :param vectors: A list of vectors to cluster.

    :param kmeans: A K-Means clustering object.

    :return: A list of indices of the closest vectors to the cluster centers.
    """
    closest_indices = []
    print(len(kmeans.cluster_centers_))
    for i in range(len(kmeans.cluster_centers_)):
        distances = np.linalg.norm(vectors - kmeans.cluster_centers_[i], axis=1)
        closest_index = np.argmin(distances)
        closest_indices.append(closest_index)

    selected_indices = sorted(closest_indices)
    return selected_indices


def map_vectors_to_docs(indices, docs):
    """
    Map a list of indices to a list of loaded langchain Document objects.

    :param indices: A list of indices to map.

    :param docs: A list of langchain Document objects to map to.

    :return: A list of loaded langchain Document objects.
    """
    selected_docs = [docs[i] for i in indices]
    return selected_docs


def create_summarize_chain(prompt_list):
    """
    Create a langchain summarize chain from a list of prompts.

    :param prompt_list: A list containing the template, input variables, and llm to use for the chain.

    :return: A langchain summarize chain.
    """
    template = PromptTemplate(template=prompt_list[0], input_variables=([prompt_list[1]]))
    chain = load_summarize_chain(llm=prompt_list[2], chain_type='stuff', prompt=template)
    return chain


def create_summary_from_docs(summary_docs, initial_chain, final_sum_list, api_key, use_gpt_4):
    """
    Summarize a list of loaded langchain Document objects using multiple langchain summarize chains.

    :param summary_docs: A list of loaded langchain Document objects to summarize.

    :param initial_chain: The initial langchain summarize chain to use.

    :param final_sum_list: A list containing the template, input variables, and llm to use for the final chain.

    :param api_key: The OpenAI API key to use for summarization.

    :param use_gpt_4: Whether to use GPT-4 or GPT-3.5-turbo for summarization.

    :return: A string containing the summary.
    """
    doc_summaries = []

    progress = st.progress(0)  # Create a progress bar to show the progress of summarization.
    # Remove this line and all references to it if you are not using Streamlit.
    total = len(summary_docs) + 1 # Remove this line and all references to it if you are not using Streamlit.

    for doc in summary_docs:
        summary = initial_chain.run([doc])
        doc_summaries.append(summary)

        progress.progress(len(doc_summaries) / total)  # Remove this line and all references to it if you are not using Streamlit.

    summaries = '\n'.join(doc_summaries)
    count = token_counter(summaries)

    if use_gpt_4:
        max_tokens = 7500 - int(count)
        model = 'gpt-4'

    else:
        max_tokens = 3800 - int(count)
        model = 'gpt-3.5-turbo'

    final_sum_list[2] = ChatOpenAI(openai_api_key=api_key, temperature=0, max_tokens=max_tokens, model_name=model)
    final_sum_chain = create_summarize_chain(final_sum_list)
    summaries = Document(page_content=summaries)
    final_summary = final_sum_chain.run([summaries])

    progress.progress(1.0)  # Remove this line and all references to it if you are not using Streamlit.
    time.sleep(0.4)  # Remove this line and all references to it if you are not using Streamlit.
    progress.empty()  # Remove this line and all references to it if you are not using Streamlit.

    return final_summary


def split_by_tokens(doc, num_clusters, ratio=5, minimum_tokens=200, maximum_tokens=2000):
    """
    Split a  langchain Document object into a list of smaller langchain Document objects.

    :param doc: The langchain Document object to split.

    :param num_clusters: The number of clusters to use.

    :param ratio: The ratio of documents to clusters to use for splitting.

    :param minimum_tokens: The minimum number of tokens to use for splitting.

    :param maximum_tokens: The maximum number of tokens to use for splitting.

    :return: A list of langchain Document objects.
    """
    text_doc = doc_to_text(doc)
    tokens = token_counter(text_doc)
    chunks = num_clusters * ratio
    max_tokens = int(tokens / chunks)
    max_tokens = max(minimum_tokens, min(max_tokens, maximum_tokens))
    overlap = int(max_tokens/10)

    splitter = TokenTextSplitter(chunk_size=max_tokens, chunk_overlap=overlap)
    split_doc = splitter.create_documents([text_doc])
    return split_doc


def extract_summary_docs(langchain_document, num_clusters, api_key, find_clusters):
    """
    Automatically convert a single langchain Document object into a list of smaller langchain Document objects that represent each cluster.

    :param langchain_document: The langchain Document object to summarize.

    :param num_clusters: The number of clusters to use.

    :param api_key: The OpenAI API key to use for summarization.

    :param find_clusters: Whether to find the optimal number of clusters to use.

    :return: A list of langchain Document objects.
    """
    split_document = split_by_tokens(langchain_document, num_clusters)
    vectors = embed_docs(split_document, api_key)

    if find_clusters:
        kmeans = kmeans_clustering(vectors, None)

    else:
        kmeans = kmeans_clustering(vectors, num_clusters)

    indices = get_closest_vectors(vectors, kmeans)
    summary_docs = map_vectors_to_docs(indices, split_document)
    return summary_docs


def doc_to_final_summary(langchain_document, num_clusters, initial_prompt_list, final_prompt_list, api_key, use_gpt_4, find_clusters=False):
    """
    Automatically summarize a single langchain Document object using multiple langchain summarize chains.

    :param langchain_document: The langchain Document object to summarize.

    :param num_clusters: The number of clusters to use.

    :param initial_prompt_list: The initial langchain summarize chain to use.

    :param final_prompt_list: A list containing the template, input variables, and llm to use for the final chain.

    :param api_key: The OpenAI API key to use for summarization.

    :param use_gpt_4: Whether to use GPT-4 or GPT-3.5-turbo for summarization.

    :param find_clusters: Whether to automatically find the optimal number of clusters to use.

    :return: A string containing the summary.
    """
    initial_prompt_list = create_summarize_chain(initial_prompt_list)
    summary_docs = extract_summary_docs(langchain_document, num_clusters, api_key, find_clusters)
    output = create_summary_from_docs(summary_docs, initial_prompt_list, final_prompt_list, api_key, use_gpt_4)
    return output


def summary_prompt_creator(prompt, input_var, llm):
    """
    Create a list containing the template, input variables, and llm to use for a langchain summarize chain.

    :param prompt: The template to use for the chain.

    :param input_var: The input variables to use for the chain.

    :param llm: The llm to use for the chain.

    :return: A list containing the template, input variables, and llm to use for the chain.
    """
    prompt_list = [prompt, input_var, llm]
    return prompt_list






