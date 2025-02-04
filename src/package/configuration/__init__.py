from dataclasses import dataclass
from pathlib import Path
import os
from package.constants import (
    DataIngestionConstants, 
    DataValidationConstants, 
    DataTransformationConstants
)


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


@dataclass
class DataValidationConfig:
    ARITFACTS_ROOT_DIR_PATH = Path(DataValidationConstants.ARITFACTS_ROOT_DIR_NAME)
    DATA_ROOT_DIR_PATH = os.path.join(ARITFACTS_ROOT_DIR_PATH, DataValidationConstants.DATA_ROOT_DIR_NAME)
    VALIDATION_ROOT_DIR_PATH = os.path.join(DATA_ROOT_DIR_PATH, DataValidationConstants.VALIDATION_ROOT_DIR_NAME)

    VALID_ROOT_DIR_PATH = os.path.join(VALIDATION_ROOT_DIR_PATH, DataValidationConstants.VALID_ROOT_DIR_NAME)
    VALID_TRAIN_FILE_PATH = os.path.join(VALID_ROOT_DIR_PATH, DataValidationConstants.VALID_TRAIN_FILE_NAME)
    VALID_TEST_FILE_PATH = os.path.join(VALID_ROOT_DIR_PATH, DataValidationConstants.VALID_TEST_FILE_NAME)

    INVALID_ROOT_DIR_PATH = os.path.join(VALIDATION_ROOT_DIR_PATH, DataValidationConstants.INVALID_ROOT_DIR_NAME)
    INVALID_TRAIN_FILE_PATH = os.path.join(INVALID_ROOT_DIR_PATH, DataValidationConstants.INVALID_TRAIN_FILE_NAME)
    INVALID_TEST_FILE_PATH = os.path.join(INVALID_ROOT_DIR_PATH, DataValidationConstants.INVALID_TEST_FILE_NAME)

    DRIFT_REPORT_ROOT_DIR_PATH = os.path.join(VALIDATION_ROOT_DIR_PATH, DataValidationConstants.DRIFT_REPORT_ROOT_DIR_NAME)
    DRIFT_REPORT_FILE_PATH = os.path.join(DRIFT_REPORT_ROOT_DIR_PATH, DataValidationConstants.DRIFT_REPORT_FILE_NAME)

    SCHEMA_FILE_PATH = DataValidationConstants.SCHEMA_FILE_PATH


@dataclass
class DataTransformationConfig:
    ARITFACTS_ROOT_DIR_PATH =  Path(DataTransformationConstants.ARITFACTS_ROOT_DIR_NAME)
    DATA_ROOT_DIR_PATH =  os.path.join(ARITFACTS_ROOT_DIR_PATH, DataTransformationConstants.DATA_ROOT_DIR_NAME)
    TRANSFORMATION_ROOT_DIR_PATH =  os.path.join(DATA_ROOT_DIR_PATH, DataTransformationConstants.TRANSFORMATION_ROOT_DIR_NAME)
    PREPROCESSOR_PATH =  os.path.join(TRANSFORMATION_ROOT_DIR_PATH, DataTransformationConstants.PREPROCESSOR_NAME)
    TRAIN_FILE_PATH =  os.path.join(TRANSFORMATION_ROOT_DIR_PATH, DataTransformationConstants.TRAIN_FILE_NAME)
    TEST_FILE_PATH =  os.path.join(TRANSFORMATION_ROOT_DIR_PATH, DataTransformationConstants.TEST_FILE_NAME)
    TARGET_COLUMN_NAME =  DataTransformationConstants.TARGET_COLUMN_NAME
    PREPROCESSOR_PARAMS =  DataTransformationConstants.PREPROCESSOR_PARAMS


