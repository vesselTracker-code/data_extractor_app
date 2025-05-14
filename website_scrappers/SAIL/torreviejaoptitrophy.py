from unicodedata import category

from website_scrappers.scrapper_class import Scrapper, DATAFRAME_HEADER
import selenium as sl
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import utils.utils as ut
import unidecode as ud
from difflib import SequenceMatcher
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd
class TorreviejaoptitrophyScrapper(Scrapper):

    def __init__(self):
        super().__init__("https://www.torreviejaoptitrophy.com/es/default/races/race-resultsall")

    def scrape_website(self):
        categoryElements = self.get_sailing_categories()
        tables = ut.wait_for_page_elements_to_load_by(self.driver, By.TAG_NAME, "table", 20)
        dataframes_to_return = []
        for i in range(len(tables)):
            rows_list = []
            table = tables[i]
            categoryElements[i].click()
            rows = table.find_elements(By.TAG_NAME, "tr")
            for row in rows:
                objectToAppend = {}
                colons = row.find_elements(By.TAG_NAME, "td")
                try:
                    position = colons[0].text
                    country = colons[1].text
                    sponsor = colons[3].text
                    name = colons[4].text
                    rows_list.append([position, country, sponsor, name])
                except:
                    print("Colons were in Torreviejaoptitrophy:", colons)

            dataframes_to_return.append(pd.DataFrame(data=rows_list, columns=DATAFRAME_HEADER))
        self.dataframes_in_function_of_category = dataframes_to_return
        return self.dataframes_in_function_of_category

    def get_sailing_class(self):
        return self.class_name

    def get_regata_name(self):
        return self.regata_name

    def get_total_number_of_participants(self):
        categoryElements = self.get_sailing_categories()
        tables = ut.wait_for_page_elements_to_load_by(self.driver, By.TAG_NAME, "table", 20)
        for i in range(len(tables)):
            categoryElements[i].click()
            elementNumber = int(tables[i].find_elements(By.TAG_NAME, "tr")[-1].find_element(By.TAG_NAME, "td").text)
            self.participants_in_function_of_category.setdefault(categoryElements[i].text, elementNumber)
        return self.participants_in_function_of_category

    def get_last_update_date(self, categoryElement):
        pass


    def get_sailing_categories(self) -> list:
        self.categoryElements = ut.wait_for_page_elements_to_load_by(self.driver, By.CLASS_NAME, "rl", 20)
        return self.categoryElements

    def get_sailing_categories_text_list(self) -> list:
        if self.categoryElements is None:
            self.get_sailing_categories()

        if(self.categoryElements is None):
            return None
        else:
            return [category.text for category in self.categoryElements]


scrapper = TorreviejaoptitrophyScrapper()
print(scrapper.get_total_number_of_participants())
