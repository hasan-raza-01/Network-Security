from package.entity import DataValidationConfigEntity, DataTransformationConfigEntity
from package.exception import CustomException
from package.utils import create_dirs, save_obj, read_yaml
from dataclasses import dataclass
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from package.logger import logging
from pathlib import Path
import pandas as pd
import numpy as np
import sys



@dataclass
class DataTransformationComponents:
    data_validation_config: DataValidationConfigEntity
    data_transformation_config: DataTransformationConfigEntity

    def get_preprocessor(self)->Pipeline:
        try:
            logging.info("In get_preprocessor")
            params = self.data_transformation_config.PREPROCESSOR_PARAMS
            imputer = SimpleImputer(**params)
            preprocessor = Pipeline([("imputer", imputer)])
            logging.info("Out get_preprocessor")
            return preprocessor
        except Exception as e:
            raise CustomException(e, sys)
    
    def transform_data(self, train_data_path:Path, test_data_path:Path)->tuple[np.array]:
        """transform data with SimpleImputer only

        Args:
            train_data_path (Path): train file path
            test_data_path (Path): test file path

        Returns:
            tuple[np.array]: (train data, test data)
        """
        try:
            logging.info("In transform_data")

            # get data
            train_data = pd.read_csv(train_data_path)
            test_data = pd.read_csv(test_data_path)
            logging.info("validated data collection completed")

            # X, y for train data
            target_column = self.data_transformation_config.TARGET_COLUMN_NAME
            X_train  = train_data.drop(target_column, axis=1)
            y_train = train_data[target_column].replace(-1, 0)

            # X, y for test data
            target_column = self.data_transformation_config.TARGET_COLUMN_NAME
            X_test  = test_data.drop(target_column, axis=1)
            y_test = test_data[target_column].replace(-1, 0)
            
            # get preprocessor object
            preprocessor = self.get_preprocessor()
            logging.info("preprocessor collected")

            # transform data input features
            transformed_X_train = preprocessor.fit_transform(X_train)
            transformed_X_test = preprocessor.transform(X_test)
            logging.info("input features transformation completed")

            # save preprocessor
            preprocessor_path = self.data_transformation_config.PREPROCESSOR_PATH
            save_obj(preprocessor, preprocessor_path)
            logging.info(f"preprocessor object saved at {preprocessor_path}")

            # concatination of input and output features
            preprocessed_train_data = np.c_[transformed_X_train, np.array(y_train)]
            preprocessed_test_data = np.c_[transformed_X_test, np.array(y_test)]
            logging.info("concatination of X and y successfully completed")

            logging.info("Out transform_data")
            return (preprocessed_train_data, preprocessed_test_data)
        except Exception as e:
            raise CustomException(e, sys)

    def intiate_transformation(self):
        try:
            logging.info("In intiate_transformation")

            # create required dir's
            create_dirs(self.data_transformation_config.ARITFACTS_ROOT_DIR_PATH)
            create_dirs(self.data_transformation_config.DATA_ROOT_DIR_PATH)
            create_dirs(self.data_transformation_config.TRANSFORMATION_ROOT_DIR_PATH)
            logging.info("Required dir's creation completed")

            # get drift report
            drift_report = read_yaml(self.data_validation_config.DRIFT_REPORT_FILE_PATH).result
            logging.info("drift report collected")

            # verify drift status
            for _, status in drift_report.items():
                if not status:
                    pass
                else:
                    message = "data drift status is True"
                    logging.info(message)
                    raise CustomException(message, sys)
                
            # get train and test file path
            train_data_path = self.data_validation_config.VALID_TRAIN_FILE_PATH
            test_data_path = self.data_validation_config.VALID_TEST_FILE_PATH

            # get transformed data
            train_data, test_data = self.transform_data(train_data_path, test_data_path)

            # save transformed train data
            train_file_path = self.data_transformation_config.TRAIN_FILE_PATH
            np.save(train_file_path, train_data)
            logging.info(f"transformed train data saved at {train_file_path}")

            # save transformed test data
            test_file_path = self.data_transformation_config.TEST_FILE_PATH
            np.save(test_file_path, test_data)
            logging.info(f"transformed test data saved at {test_file_path}")
            
            logging.info("Out intiate_transformation")
        except Exception as e:
            raise CustomException(e, sys)


