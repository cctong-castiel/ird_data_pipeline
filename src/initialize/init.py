import os
import torch
from llama_parse import LlamaParse
from llama_index.core.node_parser import TokenTextSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.opensearch import OpensearchVectorStore, OpensearchVectorClient
from llama_index.core import StorageContext
from docling.document_converter import DocumentConverter
from src.config.load_env import Environment
from src.config.settings import *

# set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# load environment variables
ENV = Environment()


# RAG initialization
converter = DocumentConverter()

parser = LlamaParse(
    api_key=ENV.LLAMAINDEX_KEY,
    result_type="markdown",
    num_workers=NUM_WORKERS,
    language='en',
    verbose=False
)

splitter = TokenTextSplitter(
    chunk_size=CHUNK_SIZE, 
    chunk_overlap=CHUNK_OVERLAP,
)

embedding_model = HuggingFaceEmbedding(
    model_name=EMBEDDING_MODEL_NAME, 
    max_length=MAX_LENGTH, 
    device=device
)

try:
    if ENV.AWS_OPENSEARCH_ENDPOINT != '' or ENV.AWS_OPENSEARCH_USERNAME != '' or ENV.AWS_OPENSEARCH_PASSWORD != '':
        opensearch_client = OpensearchVectorClient(
            endpoint=ENV.OPENSEARCH_ENDPOINT,
            index=ENV.OPENSEARCH_INDEX_NAME,
            dim=DIM,
            embedding_field=EMBEDDING_FIELD,
            text_field=TEXT_FIELD,
            search_pipeline=ENV.OPENSEARCH_SEARCH_PIPELINE,
            method={"name": "hnsw", "space_type": "l2", "engine": "faiss", "parameters": {"ef_construction": 256, "m": 48}},
        )

    else:
        opensearch_client = OpensearchVectorClient(
            endpoint=ENV.AWS_OPENSEARCH_ENDPOINT,
            index=ENV.OPENSEARCH_INDEX_NAME,
            dim=DIM,
            embedding_field=EMBEDDING_FIELD,
            text_field=TEXT_FIELD,
            search_pipeline=ENV.OPENSEARCH_SEARCH_PIPELINE,
            method={"name": "hnsw", "space_type": "l2", "engine": "faiss", "parameters": {"ef_construction": 256, "m": 48}},
            kwargs={"http_auth": (ENV.AWS_OPENSEARCH_USERNAME, ENV.AWS_OPENSEARCH_PASSWORD), "use_ssl": True, "verify_certs": True, "timeout": 30}
        )

    vector_store = OpensearchVectorStore(opensearch_client)

    storage_context = StorageContext.from_defaults(vector_store=vector_store)
except Exception as e:
    print(f"Error initializing OpensearchVectorStore: {e}")
    opensearch_client = None
    vector_store = None
    storage_context = None