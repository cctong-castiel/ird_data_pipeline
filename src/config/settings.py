# scraping settings
IRD_PDF_METADATA_URL = "https://www.ird.gov.hk/eng/ppr/dip.htm"
IRD_CASE_URL = "https://www.ird.gov.hk/eng/ppr/advance{0}.htm"
IRD_ADVANCE_CASE_URL = "https://www.ird.gov.hk/eng/ppr/arc.htm"

# directory settings
IRD_DATA_DIR = "data"
IRD_CASE_DIR = "data/ird_case_contents"

# llamaindex settings
NUM_WORKERS = 4

CHUNK_SIZE = 512
CHUNK_OVERLAP = 128

EMBEDDING_MODEL_NAME = "BAAI/bge-base-en-v1.5"
MAX_LENGTH = 512

TEXT_FIELD = "context_text"
EMBEDDING_FIELD = "passage_embedding"
DIM = 768

TOP_K = 3