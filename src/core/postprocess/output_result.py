import os
from typing import Any
from datetime import datetime
import pandas as pd
from src.config.settings import OUTPUT_DIR
from src.config.templates import retrieval_template


def display_retrieved_doc_txt(responses: Any):
    """
    It is a function to process the retrieved response and fit the content into a retrieval template

    Args:
        response (Any): It is the retrieval response from the retriever.
    """

    # start to complete the retrieval_template
    text_display_template = ""
    for r in responses:
        print(f"r: {r}")
        retrieval_template.format(
            doc_id=r.doc_id,
            document=str(r),
            doc_url=r.metadata.doc_url,
            doc_filetype=r.metadata.doc_filetype
        )
        text_display_template += retrieval_template

    # save the text_display_template result to results folders
    with open(os.path.join(OUTPUT_DIR, f"rag_retrieval_{datetime.now()}.txt"), "w", encoding='utf-8') as f:
        f.write(text_display_template)


def display_retrieved_doc_excel(responses: Any, output_filename: str):
    """
    It is a function to process the retrieved response and save the result in excel file.

    Args:
        response (Any): It is the retrieval response from the retriever.
    """

    doc_ids = []
    documents = []
    doc_urls = []
    doc_filetypes = []
    for r in responses:
        print(f"r: {r}")
        doc_ids.append(r.doc_id)
        documents.append(str(r))
        doc_urls.append(r.metadata.doc_url)
        doc_filetypes.append(r.metadata.doc_filetype)

    # save the result in an excel file
    d_result = {
        "doc_ids": doc_ids,
        "documents": documents,
        "doc_urls": doc_urls,
        "doc_filetypes": doc_filetypes
    }
    df = pd.DataFrame(data=d_result)
    df.to_excel(os.path.join(OUTPUT_DIR, f"rag_retrieval_{output_filename}_{datetime.now().timestamp()}.xlsx"))
    