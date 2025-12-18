from prefect import flow, task
from src.core.scrape.scraper import IrdCaseContentSpider
from src.core.scrape.scraper import run_spider
from src.core.scrape.scraper import scrape_step


@task(name="scrape_step", task_run_name="scrape_ird_data_task", log_prints=True)
def scrape_step():
    """
    A function to perform the scraping step by initializing and running the necessary scrapers and 
    spiders to collect IRD case and PDF metadata,
    """

    # run
    run_spider(spider=IrdCaseContentSpider)


@flow(name="ird_scrape_data_dag", description="A DAG to scrape IRD data")
def ird_scrape_data_dag():

    """
    It is the main orchestrator function to run the entire IRD data pipeline including scraping, preprocessing, and RAG processing.
    """

    # Step 1: Scrape data
    scrape_step()
