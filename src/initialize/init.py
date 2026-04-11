import torch
from llama_parse import LlamaParse
from llama_index.core.node_parser import TokenTextSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from docling.document_converter import DocumentConverter
from src.core.vector_stores.factory import VectorStoreFactory
from src.config.load_env import Environment
from src.config.settings import (
    CHUNK_SIZE, 
    CHUNK_OVERLAP,
    EMBEDDING_MODEL_NAME,
    MAX_LENGTH,
    NUM_WORKERS,
    STORE_TYPE
)

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
embedding_fn = getattr(embedding_model, "embed", embedding_model)

vector_store_factory = VectorStoreFactory(embedding_fn=embedding_fn, collection_name="ird_collection", index_name="ird_index")
vector_store = vector_store_factory.get_vector_store(STORE_TYPE)
storage_context = vector_store_factory.get_storage_context(STORE_TYPE)