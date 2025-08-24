from airflow.sdk import dag, task
from src.core.scrape.scraper import (
    IrdCaseContentSpider, IrdTableScraper, IrdPdfMetadataScraper,
    run_spider, download_pdfs, download_one_pdf
)
from src.config.settings import IRD_DATA_DIR


@dag(
    dag_id="dag_ird_data_pipeline",
    start_date=None,
    catchup=False,
    tags=["ird", "data_pipeline"],
)
def ird_data_pipeline_dag():

    @task(task_id="scrape_ird_data_task")
    def scrape_ird_data():
        """
        task to scrape ird data
        """

        # init
        ird_table_scraper = IrdTableScraper()
        ird_pdf_metadata_scraper = IrdPdfMetadataScraper()

        # run
        ird_table_scraper.scrape
        run_spider(spider=IrdCaseContentSpider)

        ird_pdf_metadata_scraper.scrape
        download_one_pdf(destination_directory=IRD_DATA_DIR)
        download_pdfs(destination_directory=IRD_DATA_DIR)

    scrape_ird_data()