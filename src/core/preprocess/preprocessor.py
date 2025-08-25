from typing import List
import json
import os
import re
from llama_index.core import Document
from llama_index.core import SimpleDirectoryReader
from src.config.settings import IRD_DATA_DIR, IRD_CASE_DIR, IRD_PDF_DIR
from src.initialize.init import parser


def preprocess_text(text: str) -> str:
    """
    It is a function to preprocess the input text by removing HTML tags, special characters, and extra spaces.

    Args:
        text (str): The input text to be preprocessed.
    
    Returns:
        str: The preprocessed text.
    """

    # Basic text preprocessing can be done here
    # remove special characters and extra spaces
    html_pattern = re.compile(r'<.*?>')
    text = re.sub(html_pattern, '', text)  # remove HTML tags
    text = re.sub(r'\W+', '', text)
    text = text.strip()
    return text

def preprocess_step() -> List[Document]:
    """
    It is a function to preprocess IRD case contents and IRD PDF files by loading their metadata and contents, applying text preprocessing, 
    and returning lists of Document objects with associated metadata.

    Returns:
        docs_ird_case (List[Document]): A list of Document objects representing preprocessed IRD case contents with metadata.
        docs_pdf (List[Document]): A list of Document objects representing preprocessed IRD PDF
    """

    file_extractor = {".pdf": parser}
    reader = SimpleDirectoryReader(
        input_dir=os.path.join(os.getcwd(), IRD_PDF_DIR),
        file_extractor=file_extractor,
        recursive=True,
        exclude_hidden=True,
    )

    # laod ird case metadata
    with open(f'{IRD_DATA_DIR}/ird_results.json', 'r', encoding='utf-8') as f:
        ird_metadata = json.load(f)

    # load ird pdf metadata
    with open(f'{IRD_DATA_DIR}/ird_pdf_results.json', 'r', encoding='utf-8') as f:
        ird_pdf_metadata = json.load(f)

    # load and preprocess ird case contents
    ird_case_contents = []
    for f in os.listdir(IRD_CASE_DIR):
        if f.endswith('.md'):
           with open(f, 'r', encoding='utf-8') as file:
               content = file.read()
               ird_case_contents.append(
                   Document(text=preprocess_text(content))
               )
    
    # load and preprocess ird pdf files
    ird_pdfs = []
    for pdfs in reader.iter_data():
        for pdf in pdfs:
            pdf.text = preprocess_text(pdf.text)
            ird_pdfs.append(
                preprocess_text(pdf)
            )

    # add the metadata to the documents
    docs_ird_case = []
    for i, (doc, meta) in enumerate(zip(ird_case_contents, ird_metadata)):
        doc.metadata = meta
        docs_ird_case.append(doc)

    docs_pdf = []
    for i, (doc, meta) in enumerate(zip(ird_pdfs, ird_pdf_metadata)):
        doc.metadata = meta
        docs_pdf.append(doc)

    return docs_ird_case, docs_pdf