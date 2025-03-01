from dataclasses import  dataclass
from package.configuration import DataValidationConfig, DataTransformationConfig
from package.components.data_transformation import DataTransformationComponents
from package.logger import logging


@dataclass
class DataTransformationPipeline:

    def main(self)->None:
        """runs data ingestion full pipeline
        """
        logging.info(">>>>>>> Data Transformation Initiated <<<<<<<")
        data_transformation = DataTransformationComponents(DataValidationConfig, DataTransformationConfig)
        data_transformation.intiate_transformation()
        logging.info(">>>>>>> Data Transformation completed <<<<<<<")



STAGE_NAME = "Data Transformation"

if __name__=="__main__":
    print(f"\n>>>>>>>>>>>>>>>>>>>>> {STAGE_NAME} initiated <<<<<<<<<<<<<<<<<<<<<")
    obj = DataTransformationPipeline()
    obj.main()
    print(f"\n>>>>>>>>>>>>>>>>>>>>> {STAGE_NAME} completed <<<<<<<<<<<<<<<<<<<<<")


