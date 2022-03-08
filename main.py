import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import zipfile

URL_SCRAPER = 'https://www.datosabiertos.gob.pe/'
CONTENT_TYPE = 'Dataset'
CATEGORY = 'Economía y Finanzas'
DOWNLOAD_FORMAT = 'csv'
REPORT_NAME = 'donaciones'


prefs = {"download.default_directory": os.getcwd()}
chrome_options = Options()
chrome_options.add_argument("start-maximized")
chrome_options.add_experimental_option("prefs", prefs)
chromeDriver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
chromeDriver.implicitly_wait(30)


# Custom function we will use to imitate slow typing and fool anti-bot software
def slow_typing(element, text):
    for character in text:
        element.send_keys(character)
        time.sleep(0.3)


def extract(url=URL_SCRAPER, report_name=REPORT_NAME):
    chromeDriver.get(url=url)
    dataset_content_type = chromeDriver.find_element(by=By.XPATH,
                                                     value='//a[@href="/search/type/dataset?sort_by=changed"]')
    dataset_content_type.click()
    time.sleep(3)
    ef_category = chromeDriver.find_element(by=By.XPATH, value='//a[@id="facetapi-link"]')
    ef_category.click()
    time.sleep(3)
    formats_dropdown = chromeDriver.find_element(by=By.XPATH,
                                                 value='//*[@id="main"]/div/section/div/div/div/div/div[1]/div/div['
                                                       '4]/h2')
    formats_dropdown.click()
    time.sleep(2)
    format_type = chromeDriver.find_element(by=By.XPATH, value='//a[@id="facetapi-link--9"]')
    time.sleep(3)
    format_type.click()
    search_element = chromeDriver.find_element(by=By.XPATH, value='//input[@id="edit-query"]')

    slow_typing(search_element, report_name)

    chromeDriver.find_element(by=By.XPATH, value='//*[@id="edit-submit-dkan-datasets"]').click()

    chromeDriver.find_element(by=By.XPATH,
                              value='//*[@id="main"]/div/section/div/div/div/div/div[2]/div/div/div/div/div['
                                    '3]/div/article/div[2]/h2/a').click()

    download_button = chromeDriver.find_element(by=By.XPATH,
                                                value='//*[@id="data-and-resources"]/div/div/ul/li[3]/div/span/a')
    download_button.click()


def decompress(path):
    password = None
    zip_file = zipfile.ZipFile(path, "r")
    try:
        print(zip_file.namelist())
        zip_file.extractall(pwd=password, path=os.getcwd())
    except:
        pass
    zip_file.close()


def transform(file_path, region):
    df = pd.read_csv(file_path, encoding='ISO-8859-1')
    df['REGION'] = str(region).upper()

    df.to_csv(''+region.lower()+'.csv')


if __name__ == "__main__":
    extract()
    time.sleep(10)
    decompress(os.getcwd()+'/pcm_donaciones.zip')
    transform(os.getcwd() + '/pcm_donaciones.csv', region='LIMA')
