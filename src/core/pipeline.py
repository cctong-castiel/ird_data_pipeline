from src.core.scrape.scraper import scrape_step
from src.core.preprocess.preprocessor import preprocess_step
from src.core.process.rag import rag_step


def run_pipeline():
    """
    It is a function to run the entire data pipeline including scraping, preprocessing, and RAG processing.
    """

    # Step 1: Scrape data
    # scrape_step()

    # Step 2: preprocess data
    docs_ird_case, docs_pdf = preprocess_step()

    # Step 3: RAG process
    rag_step(docs_ird_case, docs_pdf)