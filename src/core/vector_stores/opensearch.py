from llama_index.core import StorageContext
from llama_index.vector_stores.opensearch import OpensearchVectorStore, OpensearchVectorClient
from requests_aws4auth import AWS4Auth
import boto3

from src.config.load_env import ENV
from src.config.settings import DIM, EMBEDDING_FIELD, TEXT_FIELD


class OpensearchClient:
    def __init__(self, index_name="ird_index"):
        self.index_name = index_name
        self.client = None
        self.vector_store = None
        self.storage_context = None

    def initialize(self):
        try:
            self.client = self.__build_client()
            self.vector_store = self.__build_vector_store()
            self.storage_context = self.__build_storage_context()
        except Exception as e:
            print(f"Error initializing Opensearch: {e}")
            self.client = None
            self.vector_store = None
            self.storage_context = None

    @staticmethod
    def __build_client():
        opensearch_client = OpensearchVectorClient(
            endpoint=ENV.OPENSEARCH_ENDPOINT,
            index=ENV.OPENSEARCH_INDEX_NAME,
            dim=DIM,
            embedding_field=EMBEDDING_FIELD,
            text_field=TEXT_FIELD,
            search_pipeline=ENV.OPENSEARCH_SEARCH_PIPELINE,
            method={
                "name": "hnsw", 
                "space_type": "l2", 
                "engine": "faiss", 
                "parameters": {
                    "ef_construction": 256, 
                    "m": 48
                }
            },
        )
        return opensearch_client

    def __build_vector_store(self):
        vector_store = OpensearchVectorStore(client=self.client)
        return vector_store

    def __build_storage_context(self):
        storage_context = StorageContext.from_defaults(vector_store=self.vector_store)
        return storage_context


class AWSOpensearchClient(OpensearchClient):
    def __init__(self, index_name="ird_index"):
        self.index_name = index_name
        self.client = None
        self.vector_store = None
        self.storage_context = None

    def initialize(self):
        try:
            self.client = self.__build_client()
            self.vector_store = self.__build_vector_store()
            self.storage_context = self.__build_storage_context()
        except Exception as e:
            print(f"Error initializing AWS Opensearch: {e}")
            self.client = None
            self.vector_store = None
            self.storage_context = None

    @staticmethod
    def __build_client():
        session = boto3.Session()
        credentials = session.get_credentials()
        awsauth = AWS4Auth(
            credentials.access_key,
            credentials.secret_key,
            "us-east-1",  # your region
            "es",
            session_token=getattr(credentials, "token", None)
        )
        print(f'awsauth: {awsauth}')
        opensearch_client = OpensearchVectorClient(
            endpoint=ENV.AWS_OPENSEARCH_ENDPOINT,
            index=ENV.OPENSEARCH_INDEX_NAME,
            dim=DIM,
            embedding_field=EMBEDDING_FIELD,
            text_field=TEXT_FIELD,
            search_pipeline=ENV.OPENSEARCH_SEARCH_PIPELINE,
            method={"name": "hnsw", "space_type": "l2", "engine": "faiss", "parameters": {"ef_construction": 256, "m": 48}},
            kwargs={"http_auth": awsauth, "use_ssl": True, "verify_certs": True, "timeout": 60}
        )
        return opensearch_client
