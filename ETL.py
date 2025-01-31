from package.logger import logging
from package.exception import CustomException
import sys
import pymongo
from typing import ClassVar
import pandas as pd
import json
import os
import certifi
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()
uri = os.getenv("URI")

ca = certifi.where()


@dataclass
class ExtractTransformLoad:
    __Client: ClassVar = pymongo.MongoClient(uri)
    __Database: ClassVar = __Client["Network-Security"]
    __Collection: ClassVar = __Database["Data"]

    def csv_to_json(self, path:str)-> list:
        """Converts csv file into a list of json

        Args:
            path (str): path of CSV file where data is available.

        Returns:
            list: list of json for the whole file.
        """
        try:
            data = pd.read_csv(path)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            logging.error(e)
            raise CustomException(e, sys)
        
    def push_to_db(self, records:list, collection:list)-> int:
        """pushes all records into collection of database

        Args:
            records (list): list of json
            collection (id): mongoclient database collection full id

        Returns:
            int: lenght of records
        """
        try:
            self.records = records
            self.collection = collection
            self.collection.insert_many(self.records)
            return len(records)
        except Exception as e:
            logging.error(e)
            raise CustomException(e, sys)
        
    def main(self)-> int:
        """Runs the full ETL process
        """
        path = "C:/Users/hasan/Documents/DS/Udemy/ML-Project-with-ETL-Pipeline/materials/networksecurity/Network_Data/phisingData.csv"
        collection = ExtractTransformLoad.__Collection
        records = self.csv_to_json(path)
        records_len = self.push_to_db(records, collection)
        return records_len
        


if __name__=="__main__":
    ETL_obj = ExtractTransformLoad()
    print(ETL_obj.main()) # length of records inserted
