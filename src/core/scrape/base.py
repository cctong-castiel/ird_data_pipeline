
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time


class SeleniumScraperBase:
    options = Options()
    # options.headless = True
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    # options.add_argument('--disable-extensions')
    # options.add_argument('--dns-prefetch-disable')
    options.add_argument("--disable-dev-shm-usage")


    def __init__(self, url: str):    
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
        self.url = url

    def open(self, url: str):
        self.driver.get(url)
        time.sleep(5)  # wait for the page to load, adjust as necessary
        
    def fetch_page(self):
        return NotImplemented

    def close(self):
        self.driver.quit()

    @property
    def scrape(self):
        self.open(self.url)
        data = self.fetch_page()
        self.close()
        return data
