"""
    Data Loaders for loading various datasets
"""
import json
import pickle
import codecs
from pathlib import Path
import pandas as pd


class DataReader:
    """
        Data loader class for loading datas and files
    """

    def __init__(self):
        """
            init method
        """

    @staticmethod
    def load_pkl(path: Path):
        """
            loading pickle files
        :param path:
        :return:
        """
        with codecs.open(path, 'rb') as file:
            data = pickle.load(file)
        return data

    @staticmethod
    def load_json(path: Path) -> json:
        """
            loading a json file
        :param path:
        :return:
        """
        with codecs.open(path, "r", encoding="utf-8") as json_file:
            json_data = json.load(json_file)
        return json_data

    @staticmethod
    def load_df(path: Path, columns: list=None) -> pd:
        """
            loading a csv file
        :param path:
        :return:
        """
        if columns is None:
            data_frame = pd.read_csv(path)
        else:
            data_frame = pd.read_csv(path, names=columns)
        
        return data_frame

    @staticmethod
    def load_csv(path: Path, names: list = None, sep: str=',', low_memory: bool= True, header: list=None) -> pd:
        """
            loading a csv file
        :param path:
        :return:
        """
        return pd.read_csv(path, sep=sep, header=header, low_memory=low_memory, names=names)
    
    @staticmethod
    def load_excel(path: Path) -> pd:
        """
            loading excel file
        :param path:
        :return:
        """
        excel = pd.read_excel(path)
        return excel

    @staticmethod
    def load_text(path: Path) -> str:
        """
            loading text file
        :param path:
        :return:
        """
        with codecs.open(path, 'r', encoding='utf8') as myfile:
            text = myfile.read()
        return text
