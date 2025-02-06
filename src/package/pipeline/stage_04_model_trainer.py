from dataclasses import  dataclass
from package.configuration import DataTransformationConfig, ModelTrainerConfig
from package.components.model_trainer import ModelTrainerComponents


@dataclass
class ModelTrainerPipeline:

    def main(self)->None:
        """runs data ingestion full pipeline
        """
        mt = ModelTrainerComponents(DataTransformationConfig, ModelTrainerConfig)
        mt.initiate_training()




STAGE_NAME = "Model Training"

if __name__=="__main__":
    print(f"\n>>>>>>>>>>>>>>>>>>>>> {STAGE_NAME} initiated <<<<<<<<<<<<<<<<<<<<<")
    obj = ModelTrainerPipeline()
    obj.main()
    print(f"\n>>>>>>>>>>>>>>>>>>>>> {STAGE_NAME} completed <<<<<<<<<<<<<<<<<<<<<")


