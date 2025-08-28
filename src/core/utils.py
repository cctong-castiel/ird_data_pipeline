import re


# utils functions
def extract_only_alphanumeric(text: str) -> str:
    '''
    Extract only the first continuous sequence of digits and alphabets from the input text.

    Args:
        text (str): The input text from which to extract numbers.
    Returns:
        str: The extracted number as a string, or an empty string if no digits and alphabets are found.
    '''

    match = re.search(r'[A-Za-z0-9]+', text)
    return match.group(0) if match else ''
    

def remove_html_tags(text: str) -> str:
    '''
    Remove HTML tags from the input text.

    Args:
        text (str): The input text containing HTML tags.
    Returns:
        str: The text with HTML tags removed.
    '''
    
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


STOPWORDS = [
    "Our website : www.ird.gov.hk",
    "**Evaluation Only. Created with Aspose.Words. Copyright 2003-2025 Aspose Pty Ltd.**"
    '`  `',
    "&amp;",
    "&amp"
]

STOPWORDS_PATTERN = "|".join(STOPWORDS)