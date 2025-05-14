from wsgiref.types import InputStream
import csv as reader
import numpy as np

from table_parsing.table_parser import TableParser
from utils.utils import get_absolute_path
import pandas as pd


def load_names_list() -> np.ndarray:
    """
    This method's role is to load the name list to a list array
    :param path: the path to the list
    :return: the np.array list
    """
    with open(get_absolute_path("names_list.csv"), "r") as file:
        r = reader.reader(file)
        listToReturn = [line[0] for line in r]
        return np.array(listToReturn)