from dataclasses import dataclass
from package.constants import DataIngestionConstants
import os


@dataclass
class DataIngestionConfig:
    ARITFACTS_ROOT_DIR_PATH = DataIngestionConstants.ARITFACTS_ROOT_DIR_NAME
    DATA_ROOT_DIR_PATH = os.path.join(ARITFACTS_ROOT_DIR_PATH, DataIngestionConstants.DATA_ROOT_DIR_NAME)
    INGESTION_ROOT_DIR_PATH = os.path.join(DATA_ROOT_DIR_PATH, DataIngestionConstants.INGESTION_ROOT_DIR_NAME)

    FEATURE_STORE_ROOT_DIR_PATH = os.path.join(INGESTION_ROOT_DIR_PATH, DataIngestionConstants.FEATURE_STORE_ROOT_DIR_NAME)
    RAW_FILE_PATH = os.path.join(FEATURE_STORE_ROOT_DIR_PATH, DataIngestionConstants.RAW_FILE_NAME)

    INGESTED_ROOT_DIR_PATH = os.path.join(INGESTION_ROOT_DIR_PATH, DataIngestionConstants.INGESTED_ROOT_DIR_NAME)
    TRAIN_FILE_PATH = os.path.join(INGESTED_ROOT_DIR_PATH, DataIngestionConstants.TRAIN_FILE_NAME)
    TEST_FILE_PATH = os.path.join(INGESTED_ROOT_DIR_PATH, DataIngestionConstants.TEST_FILE_NAME)

    SPLIT_RATIO = DataIngestionConstants.SPLIT_RATIO
    DATABASE_NAME = DataIngestionConstants.DATABASE_NAME
    COLLECTION_NAME = DataIngestionConstants.COLLECTION_NAME


