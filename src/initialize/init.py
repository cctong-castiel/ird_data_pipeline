import os
import torch
import chromadb
from llama_parse import LlamaParse
from llama_index.core.node_parser import TokenTextSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.opensearch import OpensearchVectorStore, OpensearchVectorClient
from llama_index.core import StorageContext
from docling.document_converter import DocumentConverter
from llama_index.vector_stores.chroma import ChromaVectorStore
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
    # if ENV.AWS_OPENSEARCH_ENDPOINT == '' or ENV.AWS_OPENSEARCH_USERNAME == '' or ENV.AWS_OPENSEARCH_PASSWORD == '':
    #     print("Using self-managed OpenSearch")
    #     opensearch_client = OpensearchVectorClient(
    #         endpoint=ENV.OPENSEARCH_ENDPOINT,
    #         index=ENV.OPENSEARCH_INDEX_NAME,
    #         dim=DIM,
    #         embedding_field=EMBEDDING_FIELD,
    #         text_field=TEXT_FIELD,
    #         search_pipeline=ENV.OPENSEARCH_SEARCH_PIPELINE,
    #         method={"name": "hnsw", "space_type": "l2", "engine": "faiss", "parameters": {"ef_construction": 256, "m": 48}},
    #     )

    # else:
    #     print("Using AWS OpenSearch")
    #     from requests_aws4auth import AWS4Auth
    #     import boto3
    #     session = boto3.Session()
    #     credentials = session.get_credentials()
    #     print(f'credentials access_key: {credentials.access_key}')
    #     print(getattr(credentials, "token", None))
    #     awsauth = AWS4Auth(
    #         credentials.access_key,
    #         credentials.secret_key,
    #         "us-east-1",  # your region
    #         "es",
    #         session_token=getattr(credentials, "token", None)
    #     )
    #     print(f'awsauth: {awsauth}')
    #     opensearch_client = OpensearchVectorClient(
    #         endpoint=ENV.AWS_OPENSEARCH_ENDPOINT,
    #         index=ENV.OPENSEARCH_INDEX_NAME,
    #         dim=DIM,
    #         embedding_field=EMBEDDING_FIELD,
    #         text_field=TEXT_FIELD,
    #         search_pipeline=ENV.OPENSEARCH_SEARCH_PIPELINE,
    #         method={"name": "hnsw", "space_type": "l2", "engine": "faiss", "parameters": {"ef_construction": 256, "m": 48}},
    #         kwargs={"http_auth": awsauth, "use_ssl": True, "verify_certs": True, "timeout": 60}
    #     )
    #     print(f'opensearch_client: {opensearch_client}')

    # vector_store = OpensearchVectorStore(opensearch_client)
    # storage_context = StorageContext.from_defaults(vector_store=vector_store)

    embedding_fn = getattr(embedding_model, "embed", embedding_model)
    chroma_client = chromadb.EphemeralClient()
    chroma_collection = chroma_client.create_collection(name="ird_collection")
    vector_store = ChromaVectorStore(persist_directory='chroma_db', chroma_collection=chroma_collection, embedding_function=embedding_fn)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
except Exception as e:
    print(f"Error initializing OpensearchVectorStore: {e}")
    opensearch_client = None
    vector_store = None
    storage_context = None