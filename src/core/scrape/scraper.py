import os
import subprocess
import scrapy
from scrapy.crawler import CrawlerProcess
import html2text
import json
from selenium.webdriver.common.by import By
from prefect import task
from src.core.scrape.base import SeleniumScraperBase
from src.core.utils import remove_html_tags, extract_only_alphanumeric
from src.config.settings import (
    IRD_PDF_METADATA_URL, IRD_CASE_URL, IRD_ADVANCE_CASE_URL,
    IRD_DATA_DIR, IRD_CASE_DIR, IRD_PDF_DIR
)


class IrdTableScraper(SeleniumScraperBase):
    """
    A class to scrape the IRD case table from the specified URL and save the results to a JSON file.
    """

    def __init__(self, url: str = IRD_ADVANCE_CASE_URL):
        super().__init__(url=url)
        self.url = url

    def fetch_page(self):
        """
        A method to fetch and parse the IRD case table from the webpage.
        """

        # First part - extract the headers part
        gov_page_title = self.driver.find_element(By.CSS_SELECTOR, '#content-area > section > div.navi > a:nth-child(3)').get_attribute('innerHTML')
        section_name = self.driver.find_element(By.CSS_SELECTOR, '#content > div.content-div > div.introduction > p:nth-child(6) > strong').get_attribute('innerHTML')
        table_loc = self.driver.find_element(By.CSS_SELECTOR, '#content > div.content-div > div:nth-child(3) > div.toggle_div > div > div:nth-child(2)').get_attribute('innerHTML')
        
        # Second part - extract table data
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
                'gov_page_title': gov_page_title,
                'section_name': section_name,
                'table_loc': table_loc,
                'case_no': case_no,
                'case_link': case_link,
                'provision': provision,
                'index': index_items,
            })

        with open(os.path.join(IRD_DATA_DIR, 'ird_results.json'), 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)


class IrdPdfMetadataScraper(SeleniumScraperBase):
    """
    A class to scrape the IRD PDF metadata from the specified URL and save the results to a JSON file.
    """

    def __init__(self, url: str = IRD_PDF_METADATA_URL):
        super().__init__(url=url)
        self.url = url

    def fetch_page(self):
        """
        A method to fetch and parse the IRD PDF metadata table from the webpage.
        """

        # First part - extract the headers part
        gov_page_title = self.driver.find_element(By.CSS_SELECTOR, '#content-area > section > div.navi > a:nth-child(3)').get_attribute('innerHTML')
        section_name = self.driver.find_element(By.CSS_SELECTOR, '#content > div.content-title-div > h1').get_attribute('innerHTML')
        
        # Second part - extract table data
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
                'gov_page_title': gov_page_title,
                'section_name': section_name,
                'table_loc': section_name,
                'pdf_no': extract_only_alphanumeric(text=pdf_no),
                'pdf_link': pdf_link,
                'pdf_notes': pdf_notes,
                'index': pdf_date,
            })

        with open(os.path.join(IRD_DATA_DIR, 'ird_pdf_results.json'), 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)


class IrdCaseContentSpider(scrapy.Spider):
    """
    A Scrapy spider to scrape IRD case contents from specified URLs and save them as Markdown files.
    """

    name = "ird_case_content_spider"
    start_urls = [IRD_CASE_URL.format(i) for i in [13, 16, 26, 44]]

    def parse(self, response):
        """
        A method to parse the IRD case content page and save the content as a Markdown file.
        """

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
    """
    A function to run a Scrapy spider.

    Args:
        spider (scrapy.Spider): The Scrapy spider to be run.
    """

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


@task(name="scrape_step", task_run_name="scrape_ird_data_task", log_prints=True)
def scrape_step():
    """
    A function to perform the scraping step by initializing and running the necessary scrapers and 
    spiders to collect IRD case and PDF metadata,
    """

    # init
    ird_table_scraper = IrdTableScraper()
    ird_pdf_metadata_scraper = IrdPdfMetadataScraper()

    # run
    ird_table_scraper.scrape
    run_spider(spider=IrdCaseContentSpider)

    ird_pdf_metadata_scraper.scrape
    # download_one_pdf(destination_directory=IRD_PDF_DIR)
    # download_pdfs(destination_directory=IRD_PDF_DIR)