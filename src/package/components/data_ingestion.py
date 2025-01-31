from package.entity import DataIngestionConfigEntity
from package.exception import CustomException
from package.utils import create_dirs
from dataclasses import dataclass
from dotenv import load_dotenv
from pymongo import MongoClient
from sklearn.model_selection import train_test_split
import pandas as pd
import sys
import os


@dataclass
class DataIngestionComponents:
    data_ingestion_config: DataIngestionConfigEntity

    @staticmethod
    def collection_to_dataframe(collection)->pd.DataFrame:
        """converts mongodb collection into pandas dataframe

        Args:
            collection (mongodb collection): collection which needs to convert into dataframe

        Returns:
            pandas.DataFrame
        """
        try:
            # collection mongodb collection 
            df = pd.DataFrame(collection.find())

            # converting mongodb collection into pandas dataframe
            df = df.drop("_id", axis=1)

            return df
        except Exception as e:
            raise CustomException(e, sys)

    def collect_data(self)->None:
        """collects data from data base and saves locally
        """
        try:
            # creating required directories
            create_dirs(self.data_ingestion_config.ARITFACTS_ROOT_DIR_PATH)
            create_dirs(self.data_ingestion_config.DATA_ROOT_DIR_PATH)
            create_dirs(self.data_ingestion_config.INGESTION_ROOT_DIR_PATH)
            create_dirs(self.data_ingestion_config.FEATURE_STORE_ROOT_DIR_PATH)
            create_dirs(self.data_ingestion_config.INGESTED_ROOT_DIR_PATH)

            # loading vulnarable variables
            load_dotenv()
            URI = os.getenv("URI")
            
            # connecting to mongodb
            client = MongoClient(URI)
            database_name = self.data_ingestion_config.DATABASE_NAME
            collection_name = self.data_ingestion_config.COLLECTION_NAME
            
            # collection mongodb collection
            collection = client[database_name][collection_name]

            # converting mongodb collection into pandas dataframe
            self.data_frame = self.collection_to_dataframe(collection)
            
            # saving data into local file path
            self.data_frame.to_csv(self.data_ingestion_config.RAW_FILE_PATH, index=False, header=True)

        except Exception as e:
            raise CustomException(e, sys)
    
    def get_splits(self)->None:
        """Divide the collected data into train and test and saves locally
        """
        try:
            split_ratio = self.data_ingestion_config.SPLIT_RATIO

            # getting train and test data according to split ratio
            train_data, test_data = train_test_split(self.data_frame, test_size=split_ratio, random_state=42)

            # saving train data into local file path
            train_data.to_csv(self.data_ingestion_config.TRAIN_FILE_PATH, index=False, header=True)

            # saving test data into local file path
            test_data.to_csv(self.data_ingestion_config.TEST_FILE_PATH, index=False, header=True)

        except Exception as e:
            raise CustomException(e, sys)
        
