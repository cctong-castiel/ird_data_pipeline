from typing import List
import json
import os
import re
from llama_index.core import Document
from llama_index.core import SimpleDirectoryReader
from src.config.settings import IRD_DATA_DIR, IRD_CASE_DIR, IRD_PDF_DIR, NUM_WORKERS
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
    # text = re.sub(r'\W+', ' ', text)
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
        ird_metadata = sorted(ird_metadata, key=lambda x: x['case_no'])  # sort by case_no

    # load ird pdf metadata
    with open(f'{IRD_DATA_DIR}/ird_pdf_results.json', 'r', encoding='utf-8') as f:
        ird_pdf_metadata = json.load(f)
        ird_pdf_metadata = sorted(ird_pdf_metadata, key=lambda x: x['pdf_link'])

    # load and preprocess ird case contents
    docs_ird_case = []
    ird_cases_list = sorted([i for i in os.listdir(IRD_CASE_DIR) if i.endswith('.md')])
    for f, metadata in zip(ird_cases_list, ird_metadata):
        with open(os.path.join(IRD_CASE_DIR, f), 'r', encoding='utf-8') as file:
            content = file.read()
            document = Document(text=preprocess_text(content), metadata=metadata)
            print(f"document: {document}")
            docs_ird_case.append(document)

    # load and preprocess ird pdf files
    docs_pdf = []
    pdfs = list(reader.load_data(num_workers=4))
    for doc, metadata in zip(pdfs[:5], ird_pdf_metadata[:5]):
        document = Document(text=preprocess_text(doc.text), metadata=metadata)
        docs_pdf.append(document)

    return docs_ird_case, docs_pdf