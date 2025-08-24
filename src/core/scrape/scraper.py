import os
import subprocess
import scrapy
from scrapy.crawler import CrawlerProcess
import html2text
import json
from selenium.webdriver.common.by import By
from src.core.scrape.base import SeleniumScraperBase
from src.core.utils import remove_html_tags, extract_only_alphanumeric
from src.config.settings import (
    IRD_PDF_METADATA_URL, IRD_CASE_URL, IRD_ADVANCE_CASE_URL,
    IRD_DATA_DIR, IRD_CASE_DIR
)


class IrdTableScraper(SeleniumScraperBase):
    def __init__(self, url: str = IRD_ADVANCE_CASE_URL):
        super().__init__(url=url)
        self.url = url

    def fetch_page(self):
        table = self.driver.find_element(By.CSS_SELECTOR, 'table.border_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')[1:]  # skip header row

        results = []
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, 'td')

            case_no = cols[0].find_element(By.TAG_NAME, 'a').get_attribute('innerHTML') if cols[0].find_elements(By.TAG_NAME, 'a') else None
            case_link = cols[0].find_element(By.TAG_NAME, 'a').get_attribute('href') if cols[0].find_elements(By.TAG_NAME, 'a') else None
            provision = cols[1].get_attribute('innerHTML') if cols[1] else None
            index_items = [li.get_attribute('innerHTML') for li in cols[2].find_elements(By.TAG_NAME, 'li')]
            results.append({
                'case_no': case_no,
                'case_link': case_link,
                'provision': provision,
                'index': index_items,
            })

        with open(os.path.join(IRD_DATA_DIR, 'ird_results.json'), 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)


class IrdPdfMetadataScraper(SeleniumScraperBase):
    def __init__(self, url: str = IRD_PDF_METADATA_URL):
        super().__init__(url=url)
        self.url = url

    def fetch_page(self):
        table = self.driver.find_element(By.CSS_SELECTOR, 'table.border_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')[1:]  # skip header row

        results = []
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, 'td')

            pdf_no = cols[0].find_element(By.TAG_NAME, 'a').get_attribute('innerHTML') if cols[0].find_elements(By.TAG_NAME, 'a') else None
            pdf_link = cols[0].find_element(By.TAG_NAME, 'a').get_attribute('href') if cols[0].find_elements(By.TAG_NAME, 'a') else None
            pdf_notes = cols[1].find_element(By.TAG_NAME, 'a').get_attribute('innerHTML') if cols[1] else None
            pdf_notes = remove_html_tags(text=pdf_notes) if pdf_notes else None
            pdf_date = cols[2].get_attribute('innerHTML') if cols[2] else None
            results.append({
                'pdf_no': extract_only_alphanumeric(text=pdf_no),
                'pdf_link': pdf_link,
                'pdf_notes': pdf_notes,
                'index': pdf_date,
            })

        with open(os.path.join(IRD_DATA_DIR, 'ird_pdf_results.json'), 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)


class IrdCaseContentSpider(scrapy.Spider):
    name = "ird_case_content_spider"
    start_urls = [IRD_CASE_URL.format(i) for i in [13, 16, 26, 44]]

    def parse(self, response):

        html_content = response.css('div#content').get()

        if html_content:
            # convert HTML to Markdown
            h = html2text.HTML2Text()
            h.ignore_links = False  # Set to True if you want to ignore links
            markdown_content = h.handle(html_content)

            # define filename
            filename = response.url.split("/")[-1].replace(".htm", ".md")
            with open(os.path.join(IRD_CASE_DIR, filename), 'w', encoding='utf-8') as f:
                f.write(markdown_content)
                print(f'Saved file {filename}')

def run_spider(spider: scrapy.Spider):
    process = CrawlerProcess(settings={
        "LOG_LEVEL": "ERROR",
    })
    process.crawl(spider)
    process.start()


def download_pdfs(destination_directory: str, num_pdfs: int = 63):
    """
    A function to download PDF files from a specified URL pattern and save them to a given directory.

    Args:
        destination_directory (str): The directory where the downloaded PDF files will be saved.
    """
    try:
        for i in range(1, num_pdfs + 1):
            pdf_url = f"https://www.ird.gov.hk/eng/pdf/dipn{i:02d}.pdf"
            wget_command = ["wget", "-P", destination_directory, pdf_url]
            subprocess.run(wget_command, check=True, capture_output=True, text=True)
            print(f"File downloaded successfully to: {destination_directory}")
    except subprocess.CalledProcessError as e:
        print(f"Error downloading file: {e}")
        print(f"Stderr: {e.stderr}")


def download_one_pdf(destination_directory: str, pdf_number: str = "13a"):
    """
    A function to download a single PDF file from a specified URL and save it to a given directory.

    Args:
        destination_directory (str): The directory where the downloaded PDF file will be saved.
    """

    try:
        # download pdf 13A document
        pdf_url = f"https://www.ird.gov.hk/eng/pdf/dipn{pdf_number}.pdf"
        wget_command = ["wget", "-P", destination_directory, pdf_url]
        subprocess.run(wget_command, check=True, capture_output=True, text=True)
        print(f"File downloaded successfully to: {destination_directory}")
    except subprocess.CalledProcessError as e:
        print(f"Error downloading file: {e}")
        print(f"Stderr: {e.stderr}")