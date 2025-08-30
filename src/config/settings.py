from llama_index.core.vector_stores.types import VectorStoreQueryMode

# scraping settings
IRD_PDF_METADATA_URL = "https://www.ird.gov.hk/eng/ppr/dip.htm"
IRD_CASE_URL = "https://www.ird.gov.hk/eng/ppr/advance{0}.htm"
IRD_ADVANCE_CASE_URL = "https://www.ird.gov.hk/eng/ppr/arc.htm"

# directory settings
IRD_DATA_DIR = "data"
IRD_CASE_DIR = "data/ird_case_contents"
IRD_PDF_DIR = "data/ird_pdfs"
IRD_PDF_MD_DIR = "data/ird_pdfs_md"
OUTPUT_DIR = "results"

# llamaindex settings
NUM_WORKERS = 8

CHUNK_SIZE = 512
CHUNK_OVERLAP = 50

EMBEDDING_MODEL_NAME = "BAAI/bge-base-en-v1.5"
MAX_LENGTH = 512

TEXT_FIELD = "context_text"
EMBEDDING_FIELD = "passage_embedding"
DIM = 768

TOP_K = 3
VECTOR_QUERY_MODE = VectorStoreQueryMode.HYBRID