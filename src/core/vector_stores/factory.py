from typing import Any, Callable, Dict
from src.core.vector_stores.chroma import ChromaClient
from src.core.vector_stores.opensearch import OpensearchClient, AWSOpensearchClient


class VectorStoreFactory:
    def __init__(self, embedding_fn=None, collection_name="ird_collection", index_name="ird_index"):
        # Register the store types and their corresponding initialization
        # Call the Clients initialize() only once and reuse the same instance for all requests
        self._chroma_instance = ChromaClient(embedding_fn=embedding_fn, collection_name=collection_name).initialize()
        self._opensearch_instance = OpensearchClient(index_name=index_name).initialize()
        # self._aws_opensearch_instance = AWSOpensearchClient(index_name=index_name).initialize()

        self._builders: Dict[str, Callable[..., Any]] = {
            "chroma": self._chroma_instance,
            "opensearch": self._opensearch_instance,
            # "aws_opensearch": self._aws_opensearch_instance
        }

    def get_vector_store(self, store_type: str) -> Any:
        return self._builders.get(store_type).vector_store if store_type in self._builders else None
    
    def get_storage_context(self, store_type: str) -> Any:
        return self._builders.get(store_type).storage_context if store_type in self._builders else None