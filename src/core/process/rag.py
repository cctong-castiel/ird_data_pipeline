import os
from typing import List, Any
from datetime import datetime
import pandas as pd
from llama_index.core import VectorStoreIndex, Document
from llama_index.core.base.base_retriever import BaseRetriever
from src.initialize.init import (
    splitter, embedding_model, storage_context
)
from src.config.settings import TOP_K, VECTOR_QUERY_MODE, OUTPUT_DIR
from src.config.templates import retrieval_template


def process_rag(docs_ird_case: List[Document], docs_pdf: List[Document]) -> BaseRetriever:
    """
    It is a function to process RAG (Retrieval-Augmented Generation) by creating a vector store index from the provided documents and returning a retriever for querying.

    Args:
        docs_ird_case (List[Document]): A list of Document objects representing IRD case contents.
        docs_pdf (List[Document]): A list of Document objects representing IRD PDF contents.
    
    Returns:
        retriever: A retriever object that can be used to query the vector store index.
    """

    # combine all documents
    all_docs = docs_ird_case + docs_pdf

    # token text splitter
    token_nodes = splitter.get_nodes_from_documents(documents=all_docs, show_progress=True)

    # create index
    index = VectorStoreIndex(
        token_nodes, storage_context=storage_context, embed_model=embedding_model
    )

    # create retriever
    retriever = index.as_retriever(
        similarity_top_k=TOP_K,
        vector_store_query_mode=VECTOR_QUERY_MODE
    )

    return retriever


def retrieve_documents(retriever: BaseRetriever) -> Any:
    """
    It is a function to retrieve documents from the vector store index based on user queries.

    Args:
        retriever (BaseRetriever): A retriever object that can be used to query the vector store index.

    Return:
        response (Any): It is the retrieval response from the retriever.
    """

    query = input("Enter your query related to IRD cases or PDFs: ")
    response = retriever.retrieve(query)

    return response
    
    # for r in response:
    #     print("\n--- Document ---")
    #     print(f"Content: {r}")
    #     print("Metadata:", r.metadata)

def display_retrieved_doc_txt(response: Any):
    """
    It is a function to process the retrieved response and fit the content into a retrieval template

    Args:
        response (Any): It is the retrieval response from the retriever.
    """

    # start to complete the retrieval_template
    text_display_template = ""
    for r in response:
        retrieval_template.format(
            doc_id=r.doc_id,
            document=str(r),
            doc_url=r.metadata.doc_url,
            doc_filetype=r.metadata.doc_filetype
        )
        text_display_template += retrieval_template

    # save the text_display_template result to results folders
    with open(os.path.join(OUTPUT_DIR, f"rag_retrieval_{datetime.now()}.txt"), "w", encoding='utf-8') as f:
        f.write(text_display_template)


def display_retrieved_doc_excel(response: Any):
    """
    It is a function to process the retrieved response and save the result in excel file.

    Args:
        response (Any): It is the retrieval response from the retriever.
    """

    doc_ids = []
    documents = []
    doc_urls = []
    doc_filetypes = []
    for r in response:
        doc_ids.append(r.doc_id)
        documents.append(str(r))
        doc_urls.append(r.metadata.doc_url)
        doc_filetypes.append(r.metadata.doc_filetype)

    # save the result in an excel file
    d_result = {
        "doc_ids": doc_ids,
        "documents": documents,
        "doc_urls": doc_urls,
        "doc_filetypes": doc_filetypes
    }
    df = pd.DataFrame(data=d_result)
    pd.to_excel(os.path.join(OUTPUT_DIR, f"rag_retrieval_{datetime.now()}.xlsx"))
    

def rag_step(docs_ird_case: List[Document], docs_pdf: List[Document]):
    """
    It is a function to perform the RAG (Retrieval-Augmented Generation) step by creating a retriever from the provided documents 
    and retrieving documents based on user queries.

    Args:
        docs_ird_case (List[Document]): A list of Document objects representing IRD case contents.
        docs_pdf (List[Document]): A list of Document objects representing IRD PDF contents
    """

    # create retriever
    retriever = process_rag(docs_ird_case, docs_pdf)

    # retrieve documents based on user query
    retrieve_documents(retriever)