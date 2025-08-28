import scrapy
from scrapy.crawler import CrawlerProcess
import html2text


class IrdTableSpider(scrapy.Spider):
    name = "ird_table_spider"
    start_urls = ['https://www.ird.gov.hk/eng/ppr/arc.htm']

    # custom_settings = {
    #     'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    # }

    def parse(self, response):
        # Select the table rows, skip the header
        print("start")
        print(f"response with: {response.status} and type: {type(response)}")
        
        rows = response.css('table.border_table tbody')
        print(f'rows with: {rows}')
        for row in rows:
            case_no = row.css('td:nth-child(1) a::text').get()
            case_link = row.css('td:nth-child(1) a::attr(href)').get()
            provision = row.css('td:nth-child(2)::text').get()
            index_items = row.css('td:nth-child(3) li::text').getall()
            yield {
                'case_no': case_no,
                'case_link': response.urljoin(case_link) if case_link else None,
                'provision': provision.strip() if provision else None,
                'index': [item.strip() for item in index_items],
            }

class IrdCaseContentSpider(scrapy.Spider):
    name = "ird_case_content_spider"
    start_urls = [f'https://www.ird.gov.hk/eng/ppr/advance{i}.htm' for i in [13, 16, 26, 44]]

    def parse(self, response):

        html_content = response.css('div#content').get()

        if html_content:
            # convert HTML to Markdown
            h = html2text.HTML2Text()
            h.ignore_links = False  # Set to True if you want to ignore links
            markdown_content = h.handle(html_content)

            # define filename
            filename = response.url.split("/")[-1].replace(".htm", ".md")
            with open(f'tests/output_files/ird_case_contents/{filename}', 'w', encoding='utf-8') as f:
                f.write(markdown_content)
                print(f'Saved file {filename}')



def run_spider_1(output_file: str, spider: scrapy.Spider):
    process = CrawlerProcess(settings={
        "LOG_LEVEL": "ERROR",
        "FEEDS": {output_file: {"format": "json"}},
    })
    process.crawl(spider)
    process.start()

def run_spider_2(output_file: str, spider: scrapy.Spider):
    process = CrawlerProcess(settings={
        "LOG_LEVEL": "ERROR",
    })
    process.crawl(spider)
    process.start()

if __name__ == "__main__":
    print("run script spider")

    output_file = "tests/ird_results.json"
    run_spider_1(output_file=output_file, spider=IrdTableSpider)

    # output_file = "tests/ird_case_content.json"
    # run_spider_2(output_file=output_file, spider=IrdCaseContentSpider)