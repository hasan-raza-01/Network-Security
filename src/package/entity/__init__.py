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


@dataclass
class DataValidationConfigEntity:
    ARITFACTS_ROOT_DIR_PATH = Path
    DATA_ROOT_DIR_PATH = Path
    VALIDATION_ROOT_DIR_PATH = Path

    VALID_ROOT_DIR_PATH = Path
    VALID_TRAIN_FILE_PATH = str
    VALID_TEST_FILE_PATH = str

    INVALID_ROOT_DIR_PATH = Path
    INVALID_TRAIN_FILE_PATH = str
    INVALID_TEST_FILE_PATH = str

    DRIFT_REPORT_ROOT_DIR_PATH = Path
    DRIFT_REPORT_FILE_PATH = str

    SCHEMA_FILE_PATH = Path


@dataclass
class DataTransformationConfigEntity:
    ARITFACTS_ROOT_DIR_PATH: Path
    DATA_ROOT_DIR_PATH: Path
    TRANSFORMATION_ROOT_DIR_PATH: Path
    PREPROCESSOR_PATH: Path
    TRAIN_FILE_PATH: Path
    TEST_FILE_PATH: Path
    TARGET_COLUMN_NAME: str
    PREPROCESSOR_PARAMS: dict


