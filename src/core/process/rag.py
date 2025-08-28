from typing import List
from llama_index.core import VectorStoreIndex, Document
from llama_index.core.base.base_retriever import BaseRetriever
from src.initialize.init import (
    splitter, embedding_model, storage_context, vector_store
)
from src.config.settings import TOP_K, VECTOR_QUERY_MODE


def process_rag(docs_ird_case: List[Document], docs_pdf: List[Document]) -> BaseRetriever:
    """
    It is a function to process RAG (Retrieval-Augmented Generation) by creating a vector store index from the provided documents and returning a retriever for querying.

    Args:
        docs_ird_case (List[Document]): A list of Document objects representing IRD case contents.
        docs_pdf (List[Document]): A list of Document objects representing IRD PDF contents
    
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


def retrieve_documents(retriever: BaseRetriever):
    """
    It is a function to retrieve documents from the vector store index based on user queries.

    Args:
        retriever: A retriever object that can be used to query the vector store index.
    """

    query = input("Enter your query related to IRD cases or PDFs: ")
    response = retriever.retrieve(query)
    
    for r in response:
        print("\n--- Document ---")
        print(f"Content: {r}")
        print("Metadata:", r.metadata)
    

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