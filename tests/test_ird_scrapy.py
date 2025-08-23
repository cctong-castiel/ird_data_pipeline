import scrapy
from scrapy.crawler import CrawlerProcess

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

def run_spider():
    process = CrawlerProcess(settings={
        "LOG_LEVEL": "ERROR",
        "FEEDS": {"results.json": {"format": "json"}},
    })
    process.crawl(IrdTableSpider)
    process.start()

if __name__ == "__main__":
    print("run script spider")
    run_spider()