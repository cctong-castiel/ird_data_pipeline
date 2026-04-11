import chromadb
from llama_index.core import StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore


class ChromaClient:
    def __init__(self, embedding_fn, collection_name="ird_collection"):
        self.embedding_fn = embedding_fn
        self.collection_name = collection_name
        self.client = None
        self.vector_store = None
        self.storage_context = None

    def initialize(self):
        try:
            self.client = self.__build_client(self.embedding_fn)
            self.vector_store = self.__build_vector_store(self.client, self.collection_name, self.embedding_fn)
            self.storage_context = self.__build_storage_context(self.vector_store)
        except Exception as e:
            print(f"Error initializing Chroma: {e}")
            self.client = None
            self.vector_store = None
            self.storage_context = None

    def __build_client(embedding_fn):
        chroma_client = chromadb.EphemeralClient()
        return chroma_client

    def __build_vector_store(client, collection_name, embedding_fn):
        chroma_collection = client.create_collection(name=collection_name)
        vector_store = ChromaVectorStore(persist_directory='chroma_db', chroma_collection=chroma_collection, embedding_function=embedding_fn)
        return vector_store

    def __build_storage_context(vector_store):
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        return storage_context