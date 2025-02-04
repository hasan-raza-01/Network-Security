from package.utils import read_yaml
from dataclasses import dataclass
from pathlib import Path
import numpy as np


CONFIG = read_yaml("config/config.yaml")

@dataclass
class DataIngestionConstants:
    ARITFACTS_ROOT_DIR_NAME = CONFIG.ARITFACTS_ROOT_DIR_NAME
    DATA_ROOT_DIR_NAME = CONFIG.DATA.ROOT_DIR_NAME
    INGESTION_ROOT_DIR_NAME = CONFIG.DATA.INGESTION.ROOT_DIR_NAME

    FEATURE_STORE_ROOT_DIR_NAME = CONFIG.DATA.INGESTION.FEATURE_STORE.ROOT_DIR_NAME
    RAW_FILE_NAME = CONFIG.DATA.INGESTION.FEATURE_STORE.RAW_FILE_NAME

    INGESTED_ROOT_DIR_NAME = CONFIG.DATA.INGESTION.INGESTED.ROOT_DIR_NAME
    TRAIN_FILE_NAME = CONFIG.DATA.INGESTION.INGESTED.TRAIN_FILE_NAME
    TEST_FILE_NAME = CONFIG.DATA.INGESTION.INGESTED.TEST_FILE_NAME

    SPLIT_RATIO = 0.2
    DATABASE_NAME = "Network-Security"
    COLLECTION_NAME = "Data"


@dataclass
class DataValidationConstants:
    ARITFACTS_ROOT_DIR_NAME = CONFIG.ARITFACTS_ROOT_DIR_NAME
    DATA_ROOT_DIR_NAME = CONFIG.DATA.ROOT_DIR_NAME
    VALIDATION_ROOT_DIR_NAME = CONFIG.DATA.VALIDATION.ROOT_DIR_NAME

    VALID_ROOT_DIR_NAME = CONFIG.DATA.VALIDATION.VALID.ROOT_DIR_NAME
    VALID_TRAIN_FILE_NAME = CONFIG.DATA.VALIDATION.VALID.TRAIN_FILE_NAME
    VALID_TEST_FILE_NAME = CONFIG.DATA.VALIDATION.VALID.TEST_FILE_NAME

    INVALID_ROOT_DIR_NAME = CONFIG.DATA.VALIDATION.INVALID.ROOT_DIR_NAME
    INVALID_TRAIN_FILE_NAME = CONFIG.DATA.VALIDATION.INVALID.TRAIN_FILE_NAME
    INVALID_TEST_FILE_NAME = CONFIG.DATA.VALIDATION.INVALID.TEST_FILE_NAME

    DRIFT_REPORT_ROOT_DIR_NAME = CONFIG.DATA.VALIDATION.DRIFT_REPORT.ROOT_DIR_NAME
    DRIFT_REPORT_FILE_NAME = CONFIG.DATA.VALIDATION.DRIFT_REPORT.FILE_NAME

    SCHEMA_FILE_PATH = Path("schema/schema.yaml")


@dataclass
class DataTransformationConstants:
    ARITFACTS_ROOT_DIR_NAME = CONFIG.ARITFACTS_ROOT_DIR_NAME
    DATA_ROOT_DIR_NAME = CONFIG.DATA.ROOT_DIR_NAME
    TRANSFORMATION_ROOT_DIR_NAME = CONFIG.DATA.TRANSFORMATION.ROOT_DIR_NAME
    PREPROCESSOR_NAME = CONFIG.DATA.TRANSFORMATION.PREPROCESSOR_NAME
    TRAIN_FILE_NAME = CONFIG.DATA.TRANSFORMATION.TRAIN_FILE_NAME
    TEST_FILE_NAME = CONFIG.DATA.TRANSFORMATION.TEST_FILE_NAME
    TARGET_COLUMN_NAME = "Result"
    PREPROCESSOR_PARAMS = dict(
        missing_values = np.nan,
        strategy = "most_frequent"
    )


