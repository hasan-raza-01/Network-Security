from package.entity import DataIngestionConfigEntity
from package.exception import CustomException
from package.logger import logging
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
            logging.info("In collection_to_dataframe")

            # collection mongodb collection 
            df = pd.DataFrame(collection.find())
            logging.info("data successfully converted (mongodb collection ===> pandas DataFrame)")

            # converting mongodb collection into pandas dataframe
            df = df.drop("_id", axis=1)

            logging.info("Out collection_to_dataframe")
            return df
        except Exception as e:
            logging.exception(e)
            raise CustomException(e, sys)

    def collect_data(self)->None:
        """collects data from data base and saves locally
        """
        try:
            logging.info("In collect_data")

            # creating required directories
            create_dirs(self.data_ingestion_config.ARITFACTS_ROOT_DIR_PATH)
            create_dirs(self.data_ingestion_config.DATA_ROOT_DIR_PATH)
            create_dirs(self.data_ingestion_config.INGESTION_ROOT_DIR_PATH)
            create_dirs(self.data_ingestion_config.FEATURE_STORE_ROOT_DIR_PATH)
            create_dirs(self.data_ingestion_config.INGESTED_ROOT_DIR_PATH)
            logging.info("Required dir's creation completed")

            # loading vulnarable variables
            load_dotenv()
            MONGODB_URI = os.getenv("MONGODB_URI")
            
            # connecting to mongodb
            client = MongoClient(MONGODB_URI)
            logging.info("connected tot mongodb")
            
            database_name = self.data_ingestion_config.DATABASE_NAME
            collection_name = self.data_ingestion_config.COLLECTION_NAME
            
            # collection mongodb collection
            collection = client[database_name][collection_name]

            # converting mongodb collection into pandas dataframe
            self.data_frame = self.collection_to_dataframe(collection)
            logging.info(f"collected data from mongodb DATABASE: {database_name} and COLLECTION: {collection_name}")
            
            # saving data into local file path
            file_path = self.data_ingestion_config.RAW_FILE_PATH
            self.data_frame.to_csv(file_path, index=False, header=True)
            logging.info(f"Data saved at {file_path}")

            logging.info("Out collect_data")
        except Exception as e:
            logging.exception(e)
            raise CustomException(e, sys)
    
    def get_splits(self)->None:
        """Divide the collected data into train and test and saves locally
        """
        try:
            logging.info("In get_splits")

            split_ratio = self.data_ingestion_config.SPLIT_RATIO

            # getting train and test data according to split ratio
            train_data, test_data = train_test_split(self.data_frame, test_size=split_ratio, random_state=42)
            logging.info("data spliting completed")

            # saving train data into local file path
            train_file_path = self.data_ingestion_config.TRAIN_FILE_PATH
            train_data.to_csv(train_file_path, index=False, header=True)
            logging.info(f"Train data saved at {train_file_path}")

            # saving test data into local file path
            test_file_path = self.data_ingestion_config.TEST_FILE_PATH
            test_data.to_csv(test_file_path, index=False, header=True)
            logging.info(f"Test data saved at {test_file_path}")
            
            logging.info("Out get_splits")
        except Exception as e:
            logging.exception(e)
            raise CustomException(e, sys)
        
