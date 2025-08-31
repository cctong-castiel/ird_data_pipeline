import pickle
from src.core.scrape.scraper import scrape_step
from src.core.preprocess.preprocessor import preprocess_step
from src.core.process.rag import rag_step
from src.core.postprocess.output_result import display_retrieved_doc_excel


def run_pipeline(config: dict):
    """
    It is a function to run the entire data pipeline including scraping, preprocessing, and RAG processing.
    """

    # variables
    scrape_data = config.get('scrape_data', False)
    load_pickle = config.get('load_pickle', False)
    save_pickle = config.get('save_pickle', True)
    object_dir = config.get('object_dir')
    output_filename = config.get('output_filename')
    ird_pdf_md_dir = config.get('ird_pdf_md_dir')
    run_pdf_to_md = config.get('run_pdf_to_md', False)
    queries = config.get('queries', ["What is the latest update on IRD cases?", "How to file an appeal with the IRD?"])

    print(f"Configuration: load_pickle={load_pickle}, save_pickle={save_pickle}, object_dir={object_dir}, output_filename={output_filename}, ird_pdf_md_dir={ird_pdf_md_dir}, run_pdf_to_md={run_pdf_to_md}, queries={queries}")

    if not load_pickle:

        if scrape_data:
            # Step 1: Scrape data
            scrape_step()

        # Step 2: preprocess data
        docs_ird_case, docs_pdf = preprocess_step(
            pdf_md_dir=ird_pdf_md_dir, object_dir=object_dir,
            run_pdf_to_md=run_pdf_to_md, save_pickle=save_pickle
        )

    # Step 3: RAG 
    if load_pickle:
        with open(f'{object_dir}/docs_ird_case.pkl', 'rb') as f:
            docs_ird_case = pickle.load(f)
        with open(f'{object_dir}/docs_pdf.pkl', 'rb') as f:
            docs_pdf = pickle.load(f)

    responses = rag_step(queries=queries, docs_ird_case=docs_ird_case, docs_pdf=docs_pdf)

    # Step 4: Output result
    # display_retrieved_doc_excel(responses=responses, output_filename=output_filename)