import os
import subprocess
import scrapy
from scrapy.crawler import CrawlerProcess
import html2text
from src.config.settings import IRD_CASE_URL, IRD_CASE_DIR


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