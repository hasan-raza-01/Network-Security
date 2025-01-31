from dataclasses import dataclass
from pathlib import Path


@dataclass
class DataIngestionConfigEntity:
    ARITFACTS_ROOT_DIR_PATH:Path
    DATA_ROOT_DIR_PATH:Path
    INGESTION_ROOT_DIR_PATH:Path

    FEATURE_STORE_ROOT_DIR_PATH:Path
    RAW_FILE_PATH:Path

    INGESTED_ROOT_DIR_PATH:Path
    TRAIN_FILE_PATH:Path
    TEST_FILE_PATH:Path

    SPLIT_RATIO:float
    DATABASE_NAME:str
    COLLECTION_NAME:str


