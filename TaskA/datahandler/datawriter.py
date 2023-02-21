"""
    Data Saver for saving various files
"""
import json
import codecs
from pathlib import Path
import pandas as pd
import pickle

class DataWriter:
    """
        Father class for definition of other data loaders
    """

    def __init__(self):
        """
            Init method
        """

    @staticmethod
    def write_pkl(data, path: Path):
        """
            write to pickle file
        :param data:
        :param path:
        :return:
        """
        with open(path, 'wb') as myfile:
            pickle.dump(data, myfile)

    @staticmethod
    def write_json(data:dict, path: Path):
        """
            Write json file
        :param data: json data
        :param path: to to save json file
        :return:
        """
        with codecs.open(path, "w", encoding="utf-8") as outfile:
            json.dump(data, outfile, indent=4, ensure_ascii=False)

    @staticmethod
    def write_csv(data: dict, path: Path):
        """
            Write CSV file
        :param data: csv data
        :param path: to save pandas file
        :return:
        """
        data_frame = pd.DataFrame(data=data)
        data_frame.to_csv(path, index=False)


    @staticmethod
    def write_df(data: pd, path: Path):
        """
            Write CSV file
        :param data: csv data
        :param path: to save pandas file
        :return:
        """
        data.to_csv(path, index=False)
    

    @staticmethod
    def write_excel(data: pd, path: Path):
        """
              Write Excel file
          :param data: excel data
          :param path: to save pandas file
          :return:
        """
        data.to_csv(path, index=False)
    
    @staticmethod
    def write_text(text: str, path: Path):
        """
            write text file
        :param text: text data
        :param path: to save text file
        :return:
        """
        with codecs.open(path, 'w', encoding='utf8') as myfile:
            myfile.write(text)