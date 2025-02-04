from package.components.data_ingestion import DataIngestionComponents
from package.configuration import DataIngestionConfig
from package.logger import logging
from dataclasses import dataclass



@dataclass
class DataIngestionPipeline:

    def main(self)->None:
        """runs data ingestion full pipeline
        """
        logging.info(">>>>>>> Data Ingestion Initiated <<<<<<<")
        data_ingestion = DataIngestionComponents(data_ingestion_config=DataIngestionConfig)
        data_ingestion.collect_data()
        data_ingestion.get_splits()
        logging.info(">>>>>>> Data Ingestion completed <<<<<<<")





STAGE_NAME = "Data Ingestion"

if __name__=="__main__":
    print(f"\n>>>>>>>>>>>>>>>>>>>>> {STAGE_NAME} initiated <<<<<<<<<<<<<<<<<<<<<")
    obj = DataIngestionPipeline()
    obj.main()
    print(f"\n>>>>>>>>>>>>>>>>>>>>> {STAGE_NAME} completed <<<<<<<<<<<<<<<<<<<<<")
