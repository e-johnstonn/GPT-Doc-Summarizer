from langchain.document_loaders import TextLoader
from langchain.text_splitter import TokenTextSplitter
from langchain.schema import Document
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain

from sklearn.cluster import KMeans

import tiktoken

import numpy as np


def doc_loader(document): # takes pdf or txt
    loader = TextLoader(document, encoding='utf-8')
    return loader.load()


def token_counter(text: str):  # counts tokens in a given string
    encoding = tiktoken.get_encoding('cl100k_base')
    token_list = encoding.encode(text)
    tokens = len(token_list)
    print(f'Tokens in initial document: {tokens}')
    return tokens


def doc_to_text(document):
    text = ''
    for i in document:
        text += i.page_content
    return text


def embed_docs(docs,api_key):
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    vectors = embeddings.embed_documents([x.page_content for x in docs])
    return vectors


def kmeans_clustering(vectors, num_clusters):
    kmeans = KMeans(n_clusters=num_clusters, random_state=42).fit(vectors)
    return kmeans


def get_closest_vectors(vectors, kmeans, num_clusters):
    closest_indices = []
    for i in range(num_clusters):
        distances = np.linalg.norm(vectors - kmeans.cluster_centers_[i], axis=1)
        closest_index = np.argmin(distances)
        closest_indices.append(closest_index)
    selected_indices = sorted(closest_indices)
    return selected_indices


def vector_to_doc(indices, docs): #should be the same docs that were passed to embed_docs earlier!
    selected_docs = [docs[i] for i in indices]
    return selected_docs


def summarize_chain_creator(prompt_list):
    template = PromptTemplate(template=prompt_list[0], input_variables=([prompt_list[1]]))
    chain = load_summarize_chain(llm=prompt_list[2], chain_type='stuff', prompt=template)
    return chain


def summary_from_summary_docs(summary_docs, initial_chain, final_sum_list, api_key, use_gpt_4):
    # this is really fucking ugly but oh well it works
    doc_summaries = []
    for doc in summary_docs:
        summary = initial_chain.run([doc])
        doc_summaries.append(summary)
    summaries = '\n'.join(doc_summaries)
    count = token_counter(summaries)
    if use_gpt_4:
        max_tokens = 7500 - int(count)
        model = 'gpt-4'
    else:
        max_tokens = 3800 - int(count)
        model = 'gpt-3.5-turbo'
    final_llm = ChatOpenAI(openai_api_key=api_key, temperature=0, max_tokens=max_tokens, model_name=model)
    final_sum_list[2] = final_llm
    final_sum_chain = summarize_chain_creator(final_sum_list)
    summaries = Document(page_content=summaries)
    final_summary = final_sum_chain.run([summaries])
    return final_summary


def token_splitter(doc, num_clusters, ratio=5, minimum_tokens=200, maximum_tokens=2000):
    # splits doc by tokens according to num_clusters times the embeddings:cluster ratio desired, takes from doc_loader func
    text_doc = doc_to_text(doc)
    tokens = token_counter(text_doc)
    chunks = num_clusters * ratio
    max_tokens = int(tokens / chunks)
    max_tokens = max(minimum_tokens, min(max_tokens, maximum_tokens))
    overlap = int(max_tokens/10)
    print(f'Total tokens in document: {tokens}, Max tokens: {max_tokens}, Overlap: {overlap}')
    splitter = TokenTextSplitter(chunk_size=max_tokens, chunk_overlap=overlap)
    split_doc = splitter.create_documents([text_doc])
    print(f'Number of docs: {len(split_doc)}')
    return split_doc


def auto_summary_docs_from_doc(text_document, num_clusters, api_key):
    split_document = token_splitter(text_document, num_clusters)
    vectors = embed_docs(split_document, api_key)
    kmeans = kmeans_clustering(vectors, num_clusters)
    indices = get_closest_vectors(vectors, kmeans, num_clusters)
    summary_docs = vector_to_doc(indices, split_document)
    return summary_docs


def auto_summary_from_doc(doc, num_clusters, initial_chain, final_prompt_list, api_key, use_gpt_4):
    summary_docs = auto_summary_docs_from_doc(doc, num_clusters, api_key)
    output = summary_from_summary_docs(summary_docs, initial_chain, final_prompt_list, api_key, use_gpt_4)
    return output


def auto_summary_builder(doc, num_clusters, initial_prompt_list, final_prompt_list, api_key, use_gpt_4):
    initial_chain = summarize_chain_creator(initial_prompt_list)
    summary = auto_summary_from_doc(doc, num_clusters, initial_chain, final_prompt_list, api_key, use_gpt_4)
    return summary


def summary_prompt_creator(prompt, input_var, llm):
    prompt_list = [prompt, input_var, llm]
    return prompt_list


def check_key_validity(api_key):
    try:
        ChatOpenAI(openai_api_key=api_key).call_as_llm('Hi')
        print('API Key is valid')
        return True
    except Exception as e:
        print('API key is invalid or OpenAI is having issues.')
        print(e)
        return "API key is invalid or OpenAI is having issues."

