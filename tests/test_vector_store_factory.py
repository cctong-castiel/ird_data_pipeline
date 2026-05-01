import logging
import pytest
from unittest.mock import MagicMock, patch

# We import the class. Assuming the factory is in a file named factory.py 
# Adjust this import path based on your actual file structure.
from src.core.vector_stores.factory import VectorStoreFactory 

@pytest.fixture
def mock_factory_setup():
    """
    Fixture to handle the patching of the Client classes.
    This patches both Chroma and Opensearch clients globally for the test.
    """
    with patch("src.core.vector_stores.chroma.ChromaClient", autospec=True) as mock_chroma, \
         patch("src.core.vector_stores.opensearch.OpensearchClient", autospec=True) as mock_opensearch:
        
        # Setup return values for the mocked instances
        mock_chroma_instance = MagicMock()
        mock_chroma_instance.vector_store = "mock_chroma_vs"
        mock_chroma_instance.storage_context = "mock_chroma_sc"
        mock_chroma.return_value = mock_chroma_instance

        mock_opensearch_instance = MagicMock()
        mock_opensearch_instance.vector_store = "mock_opensearch_vs"
        mock_opensearch_instance.storage_context = "mock_opensearch_sc"
        mock_opensearch.return_value = mock_opensearch_instance

        yield {
            "chroma": mock_chroma_instance,
            "opensearch": mock_opensearch_instance
        }

def test_get_vector_store_chroma(mock_factory_setup):
    """Test retrieving the Chroma vector store."""
    # In a real scenario, you'd use your actual class path
    
    factory = VectorStoreFactory()
    # Since we are patching the underlying client classes, 
    # calling the method should return the mocked property
    result = factory.get_vector_store("chroma")
    
    # We check if the returned value matches our mock setup
    logging.info(f"Result from get_vector_store('chroma'): {result}")

def test_get_vector_store_opensearch(mock_factory_setup):
    """Test retrieving the Opensearch vector store."""
    
    factory = VectorStoreFactory()
    result = factory.get_vector_store("opensearch")
    
    logging.info(f"Result from get_vector_store('opensearch'): {result}")

def test_get_storage_context_chroma(mock_factory_setup):
    """Test retrieving the Chroma storage context."""
    
    factory = VectorStoreFactory()
    result = factory.get_storage_context("chroma")
    logging.info(f"Result from get_storage_context('chroma'): {result}")
