from package.components.data_ingestion import DataIngestionComponents
from package.configuration import DataIngestionConfig
from dataclasses import dataclass



@dataclass
class DataIngestionPipeline:

    def main(self)->None:
        """runs data ingestion full pipeline
        """
        data_ingestion = DataIngestionComponents(data_ingestion_config=DataIngestionConfig)
        data_ingestion.collect_data()
        data_ingestion.get_splits()





STAGE_NAME = "Data Ingestion"

if __name__=="__main__":
    print(f"\n>>>>>>>>>>>>>>>>>>>>> {STAGE_NAME} initiated <<<<<<<<<<<<<<<<<<<<<")
    obj = DataIngestionPipeline()
    obj.main()
    print(f"\n>>>>>>>>>>>>>>>>>>>>> {STAGE_NAME} completed <<<<<<<<<<<<<<<<<<<<<")
