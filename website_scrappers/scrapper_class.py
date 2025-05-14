from abc import ABC, abstractmethod
import selenium as sl
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

DATAFRAME_HEADER = ["RANKING", "COUNTRY", "SPONSOR/BOAT", "CREW"]
class Scrapper(ABC):
    url = ""
    regata_name = None
    class_name = None
    """
        The variable containing the category elements
        """
    categoryElements = None
    participants_in_function_of_category = None
    dataframes_in_function_of_category = None
    driver = None

    def __init__(self, url):
        self.url = url
        self.driver = sl.webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.get(self.url)
        self.categoryElements = None
        self.regata_name = None
        self.class_name = None
        self.participants_in_function_of_category = {}
        self.dataframes_in_function_of_category = None

    @abstractmethod
    def scrape_website(self):
        """
        This method's role is to scrape the website and return a dataframe containing the necessary data
        to update the list
        Note: Its not guaranteed that the dataframe will have anything in those entries
        @:return a list of dataframes containing a dataframe for each category available in the website:
        RANKING: The index on the table
        COUNTRY: The country the crew is from
        SPONSOR/BOAT: The sponsor, name of the boat
        CREW: The name of the crew
        """
        pass

    @abstractmethod
    def get_last_update_date(self, categoryElement):
        """
        This method's responsibility is to find the last date the data was updated from
        :return: the last date the data was updated
        """
        pass

    @abstractmethod
    def get_total_number_of_participants(self):
        """
        This methods role is to get the total number of participants of a race for each category
        :return: the total number of participants for each category
        """
        pass

    @abstractmethod
    def get_regata_name(self):
        """
        This method's role is to get the name of the regata (the name of the competition we are scraping)
        :return: the name of the regata
        """
        pass

    def set_regata_name(self, regate_name):
        """
        Set the regata name for this scrapped website
        :return: the regata name for the scrapped website
        """
        self.regata_name = regate_name


    def get_sailing_class(self):
        """
        This method's role is to get the sailing class of the competition we are scraping
        :return: the sailing class of the competition
        """
        return self.class_name

    def set_sailing_class(self, class_name):
        self.class_name = class_name

    @abstractmethod
    def get_sailing_categories(self) -> list:
        pass

    @abstractmethod
    def get_sailing_categories_text_list(self) -> list:
        pass

    def quit_driver(self):
        if self.driver is not None:
            self.driver.quit()