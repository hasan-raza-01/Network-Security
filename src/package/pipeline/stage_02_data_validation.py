from dataclasses import  dataclass
from package.logger import logging
from package.configuration import DataIngestionConfig, DataValidationConfig
from package.components.data_validation import DataValidationComponents


@dataclass
class DataValidationPipeline:

    def main(self)->None:
        logging.info(">>>>>>> Data Validation Initiated <<<<<<<")
        """runs data validation full pipeline
        """
        data_validation = DataValidationComponents(DataIngestionConfig, DataValidationConfig)
        data_validation.validate()
        logging.info(">>>>>>> Data Validation completed <<<<<<<")





STAGE_NAME = "Data Validation"

if __name__=="__main__":
    print(f"\n>>>>>>>>>>>>>>>>>>>>> {STAGE_NAME} initiated <<<<<<<<<<<<<<<<<<<<<")
    obj = DataValidationPipeline()
    obj.main()
    print(f"\n>>>>>>>>>>>>>>>>>>>>> {STAGE_NAME} completed <<<<<<<<<<<<<<<<<<<<<")
