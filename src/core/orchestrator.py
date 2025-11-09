import pickle
from prefect import flow
from prefect.blocks.system import JSON
from src.core.preprocess.preprocessor import preprocess_step
from src.core.process.rag import rag_step



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