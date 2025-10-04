import pickle
from prefect import flow
from prefect.blocks.system import JSON
from src.core.scrape.scraper import scrape_step
from src.core.preprocess.preprocessor import preprocess_step
from src.core.process.rag import rag_step
from src.config.settings import IRD_DATA_DIR


@flow(name="ird_scrape_data_dag", description="A DAG to scrape IRD data")
def ird_scrape_data_dag():

    """
    It is the main orchestrator function to run the entire IRD data pipeline including scraping, preprocessing, and RAG processing.
    """

    # Step 1: Scrape data
    scrape_step()


@flow(name="ird_preprocess_data_dag", description="A DAG to preprocess IRD data")
def ird_preprocess_data_dag(config: dict):
    
    """
    It is the main flow to preprocess IRD data
    """

    # variables
    object_dir = config.get('object_dir')
    ird_pdf_md_dir = config.get('ird_pdf_md_dir')
    run_pdf_to_md = config.get('run_pdf_to_md', False)
    save_pickle = config.get('save_pickle', True)

    print(f"Configuration: object_dir={object_dir}, ird_pdf_md_dir={ird_pdf_md_dir}, run_pdf_to_md={run_pdf_to_md}, save_pickle={save_pickle}")

    # Step 2: preprocess data
    docs_ird_case, docs_pdf = preprocess_step(
        pdf_md_dir=ird_pdf_md_dir, object_dir=object_dir,
        run_pdf_to_md=run_pdf_to_md, save_pickle=save_pickle
    )

    # Step 3: Store docs_ird_case and docs_pdf as JSON blocks for later use
    docs_ird_case_block = JSON(value=docs_ird_case)
    docs_pdf_block = JSON(value=docs_pdf)
    docs_ird_case_block.save(name="docs-ird-case", overwrite=True)
    docs_pdf_block.save(name="docs-pdf", overwrite=True)


@flow(name="ird_rag_dag", description="A DAG to perform RAG processing on IRD data")
def ird_rag_dag(config: dict):
    
    """
    It is the main flow to perform RAG processing on IRD data
    """

    # variables
    object_dir = config.get('object_dir')
    output_filename = config.get('output_filename')
    queries = config.get('queries', ["What is the latest update on IRD cases?", "How to file an appeal with the IRD?"])
    load_pickle = config.get('load_pickle', False)

    print(f"Configuration: object_dir={object_dir}, output_filename={output_filename}, queries={queries}, load_pickle={load_pickle}")

    if load_pickle:
        with open(f'{object_dir}/docs_ird_case.pkl', 'rb') as f:
            docs_ird_case = pickle.load(f)
        with open(f'{object_dir}/docs_pdf.pkl', 'rb') as f:
            docs_pdf = pickle.load(f)
    else:
        # Load docs_ird_case and docs_pdf from JSON blocks
        docs_ird_case_block = JSON.load("docs_ird_case")
        docs_pdf_block = JSON.load("docs_pdf")
        docs_ird_case = docs_ird_case_block.value
        docs_pdf = docs_pdf_block.value
        raise ValueError("Loading from pickle is set to False. Please set it to True to load preprocessed data.")

    # Step 4: RAG 
    responses = rag_step(queries=queries, docs_ird_case=docs_ird_case, docs_pdf=docs_pdf)