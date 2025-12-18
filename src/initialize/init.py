import torch
import chromadb
from llama_parse import LlamaParse
from llama_index.core.node_parser import TokenTextSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
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