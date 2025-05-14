from csv import reader
import pandas as pd

from utils.utils import compare_strings, is_from_SUI, find_name_in_list, get_absolute_path, clean_str

HEADER_ONE = ["AthleteId", "Regatta", "Total number of participants", "Overall ranking", "Sailing Class"]
HEADER_TWO = ["Id", "external", "Number", "Number", "Radio"]
HEADER_THREE = ["athleteId", "Regatta", "total-number-of-participants", "overall-ranking", "sailing-class"]

header_list = [HEADER_ONE, HEADER_TWO, HEADER_THREE]
class TableParser:

    def __init__(self, path: str, name_colon_number: int, country_colon_number: int, ranking_colon_number: int,
                 regatta_name: str,
                 sailing_class_name: str):
        """
        Constructor to parse a table
        :param path: the path to the file containing the table
        :param name_colon_number: The index of the colon containing the names in the table starting from one
        :param country_colon_number: The index of the colon containing the countries starting from one
        :param ranking_colon_number The index of the colon containing the rankings starting from one
        :param regatta_name: the name of the regatta to put in the column
        :param sailing_class_name: the sailing class to put in the column conforming to the structure of the output document
        """
        self.path = path
        self.name_colon_number = name_colon_number
        self.country_colon_number = country_colon_number
        self.ranking_colon_name = ranking_colon_number
        self.regatta_name = regatta_name
        self.sailing_class_name = sailing_class_name

    def parse_table(self) -> pd.DataFrame:
        """
        Parses the table present in the file who's name is name to a dataframe to be able to filter and extract data
        from it
        :param file_name: the name of the file
        :return: a pandas dataframe containing all the information of the file
        """
        name = None
        nationality = None
        ranking = None
        dataframe = pd.DataFrame(columns=HEADER_ONE)
        total_number_of_participants = self.get_total_number_of_participants()
        with open(get_absolute_path(self.path), "r", encoding="utf-8") as file:
            r = list(reader(file))
            r = self.clean_rows_from_csv(r)
            for row in r:
                if row[self.name_colon_number - 1] != "":
                    name = row[self.name_colon_number - 1]
                if row[self.country_colon_number - 1] != "":
                    nationality = row[self.country_colon_number - 1]
                if row[self.ranking_colon_name - 1] != "":
                    ranking = row[self.ranking_colon_name - 1]
                if (is_from_SUI(nationality)):
                  dataframe.loc[len(dataframe)] = [name, self.regatta_name, total_number_of_participants, ranking,
                                                    self.sailing_class_name]
        return dataframe

    def filter_table_with_names_that_are_on_list(self, name_list: list, table: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
        indexes_with_names_on_list = []
        indexes_with_names_not_on_list = []
        for i in range(0, len(table)):
            name = table.iat[i, 0]
            index_in_name_list = find_name_in_list(name_list, name)
            if (index_in_name_list != -1):
                indexes_with_names_on_list.append(i)
                #update the name with the name on the list
                table.iat[i,0] = name_list[index_in_name_list]
            else:
                indexes_with_names_not_on_list.append(i)
        dataframe_with_names_on_list = pd.DataFrame(columns=HEADER_ONE, data=table.iloc[indexes_with_names_on_list])
        dataframe_with_names_not_on_list = pd.DataFrame(columns=HEADER_ONE,data=table.iloc[indexes_with_names_not_on_list])

        return dataframe_with_names_on_list, dataframe_with_names_not_on_list

    def get_total_number_of_participants(self) -> int:
        with open(get_absolute_path(self.path), "r", encoding="utf-8") as file:
            r = list(reader(file))
            length_of_list = len(r)
            i = length_of_list -1

            list_element = r[i][self.ranking_colon_name  - 1]
            while(list_element is None or list_element == ""):
                i = i - 1
                list_element = r[i][self.ranking_colon_name - 1]
            return r[i][self.ranking_colon_name - 1]

    def clean_rows_from_csv(self, rows_list: list) -> list:
        rows_list_to_return = []
        for row in rows_list:
            name = row[self.name_colon_number - 1]
            nationality = row[self.country_colon_number - 1]
            ranking = row[self.ranking_colon_name - 1]
            if name == "" and nationality == "" and ranking == "":
                continue
            row[self.ranking_colon_name - 1] = clean_str(ranking)
            row[self.name_colon_number -1] = clean_str(name)
            row[self.country_colon_number -1] = clean_str(nationality)
            rows_list_to_return.append(row)

        return rows_list_to_return

    def is_parsable(self):
        try:
            with open(get_absolute_path(self.path), "r", encoding="utf-8") as file:
                r = list(reader(file))
                row = r[1]
                row[self.name_colon_number - 1]
                row[self.country_colon_number - 1]
                row[self.ranking_colon_name - 1]
                return True
        except Exception as e:
            print(e)
            return False














