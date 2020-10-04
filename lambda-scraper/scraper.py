from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self):
        self.options = self._get_options()
        self.driver = webdriver.Chrome('/opt/chromedriver', chrome_options=self.options)

    @staticmethod
    def _get_options():
        """ Helper method to construct driver options """
        options = Options()
        options.binary_location = '/opt/headless-chromium'
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--single-process')
        options.add_argument('--disable-dev-shm-usage')
        return options

    def scrape_page(self, url):
        """ Method to fetch URL contents and return BeautifulSoup html parsed page source """
        self.driver.get(url)
        page = BeautifulSoup(self.driver.page_source, features="html.parser")
        return page

    def close(self):
        self.driver.close()

    def quit(self):
        self.driver.quit()
