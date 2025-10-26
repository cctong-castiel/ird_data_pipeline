from typing import List, Any, MutableMapping
import json
from prefect import task
from llama_index.core import VectorStoreIndex, Document
from llama_index.core.base.base_retriever import BaseRetriever
from src.initialize.init import (
    splitter, embedding_model, storage_context
)
from src.config.settings import TOP_K, VECTOR_QUERY_MODE


def _sanitize_metadata(md: MutableMapping) -> dict:
    sanitized = {}
    for k, v in (md or {}).items():
        key = str(k)
        if v is None:
            sanitized[key] = None
        elif isinstance(v, (str, int, float)):
            sanitized[key] = v
        elif isinstance(v, (list, dict, tuple, set)):
            try:
                sanitized[key] = json.dumps(v)
            except Exception:
                sanitized[key] = str(v)
        else:
            sanitized[key] = str(v)
    return sanitized


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

    # sanitize documents' metadata and create new Document objects
    sanitized_docs: List[Document] = []
    for d in all_docs:
        # different llama-index versions may store text in .text or .get_text()
        text = getattr(d, "text", None) or getattr(d, "get_text", lambda: None)()
        # fall back to str(d) if no text
        if not text:
            text = str(d)

        # try to extract metadata from common attributes
        md = {}
        if hasattr(d, "metadata"):
            md = d.metadata or {}
        elif hasattr(d, "extra_info"):
            md = d.extra_info or {}

        sanitized = _sanitize_metadata(md)
        sanitized_docs.append(Document(text=text, metadata=sanitized))

    # token text splitter
    token_nodes = splitter.get_nodes_from_documents(documents=sanitized_docs, show_progress=True)

    # create index
    index = VectorStoreIndex(
        token_nodes, storage_context=storage_context, embed_model=embedding_model
    )

    # create retriever
    retriever = index.as_retriever(
        similarity_top_k=TOP_K,
        # vector_store_query_mode=VECTOR_QUERY_MODE
    )

    return retriever


def retrieve_documents(query: str, retriever: BaseRetriever) -> Any:
    """
    It is a function to retrieve documents from the vector store index based on user queries.

    Args:
        retriever (BaseRetriever): A retriever object that can be used to query the vector store index.

    Return:
        response (Any): It is the retrieval response from the retriever.
    """

    response = retriever.retrieve(query)

    return response


@task(name="rag_step", task_run_name="rag_ird_data_task")
def rag_step(queries: List[str], docs_ird_case: List[Document], docs_pdf: List[Document]) -> List[Any]:
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
    responses = []
    for index, query in enumerate(queries):
        response = retrieve_documents(query=query, retriever=retriever)
        responses.append(response)

    return responses