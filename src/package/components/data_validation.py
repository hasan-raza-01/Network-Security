from dataclasses import dataclass
from package.entity import DataIngestionConfigEntity, DataValidationConfigEntity
from package.exception import CustomException
from package.utils import create_dirs, read_yaml, save_yaml
from pathlib import Path
import pandas as pd
import sys


@dataclass
class DataValidationComponents:
    data_ingestion_config: DataIngestionConfigEntity
    data_validation_config: DataValidationConfigEntity

    @staticmethod
    def get_report(train_data:pd.DataFrame, test_data:pd.DataFrame,schema_org_path:Path)->dict[dict]:
        """validates columns and data types with schema

        Args:
            train_file (Path): path for train file to compare with schema
            test_file (Path): path for test file to compare with schema

        Returns:
            dict[dict]: 
                True: If file follows schema 
                False: If file don't follow schema

                output: {result:{key:value}}
                    key = type of data[train/test]
                   value = True/False

        Note: schema will be taken from Configuration
        """
        try:
            schema_org = read_yaml(schema_org_path)
            data_dict = {"Train Data":train_data, "Test Data":test_data}

            # verification
            schema = dict()
            columns_with_dtype = dict()
            numerical_columns = list()
            output = dict()
            final_output = dict()

            for data_type_name, data in data_dict.items():
                schema = dict()
                columns_with_dtype = dict()
                numerical_columns = list()
                for col in data.columns:
                    columns_with_dtype[col] = str(data[col].dtype)
                    if data[col].dtype!="O":
                        numerical_columns.append(col)

                schema["columns"] = columns_with_dtype
                schema["numerical_columns"] = numerical_columns

                if schema==schema_org:
                    status = True
                else:
                    status = False
                output[data_type_name] = status   
            final_output["result"] = output
            return final_output
        except Exception as e:
            raise CustomException(e, sys)
        
    def validate(self)->None:
        """create required directories, saves validated data and report
        """
        try:
            # create required directories
            create_dirs(self.data_validation_config.ARITFACTS_ROOT_DIR_PATH)
            create_dirs(self.data_validation_config.DATA_ROOT_DIR_PATH)
            create_dirs(self.data_validation_config.VALIDATION_ROOT_DIR_PATH)
            create_dirs(self.data_validation_config.VALID_ROOT_DIR_PATH)
            create_dirs(self.data_validation_config.INVALID_ROOT_DIR_PATH)
            create_dirs(self.data_validation_config.DRIFT_REPORT_ROOT_DIR_PATH)

            # get required variables and data
            schema_path = self.data_validation_config.SCHEMA_FILE_PATH
            report_path = self.data_validation_config.DRIFT_REPORT_FILE_PATH
            ingested_train_data = pd.read_csv(self.data_ingestion_config.TRAIN_FILE_PATH, index_col=False)
            ingested_test_data = pd.read_csv(self.data_ingestion_config.TEST_FILE_PATH, index_col=False)
            output = self.get_report(ingested_train_data, ingested_test_data, schema_path)

            # get valid and invalid file path for train and test data
            valid_path_dict = {"Train Data":self.data_validation_config.VALID_TRAIN_FILE_PATH, 
                               "Test Data":self.data_validation_config.VALID_TEST_FILE_PATH}
            invalid_path_dict = {"Train Data":self.data_validation_config.INVALID_TRAIN_FILE_PATH, 
                               "Test Data":self.data_validation_config.INVALID_TEST_FILE_PATH}

            
            # save validation report
            save_yaml(output, report_path)

            # save validated data
            for data_type_name, status in output["result"].items():
                if status:
                    path = valid_path_dict[data_type_name]
                else:
                    path = invalid_path_dict[data_type_name]

                if data_type_name=="Train Data":
                    ingested_train_data.to_csv(path, index=False, header=True)
                if data_type_name=="Test Data":
                    ingested_test_data.to_csv(path, index=False, header=True)

        except Exception as e:
            raise CustomException(e, sys)
        

