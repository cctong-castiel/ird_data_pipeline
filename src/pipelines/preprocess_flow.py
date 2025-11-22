import argparse
import yaml
from prefect import flow
from prefect.blocks.system import JSON
from src.core.preprocess.preprocessor import preprocess_step


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
