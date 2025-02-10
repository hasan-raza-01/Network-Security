from package.pipeline import (
    stage_01_data_ingestion,
    stage_02_data_validation,
    stage_03_data_transformation,
    stage_04_model_trainer
)
from dataclasses import dataclass
from package.cloud import push_to_cloud


@dataclass
class TrainingPipeline:
    stage_01 = stage_01_data_ingestion.DataIngestionPipeline()
    stage_02 = stage_02_data_validation.DataValidationPipeline()
    stage_03 = stage_03_data_transformation.DataTransformationPipeline()
    stage_04 = stage_04_model_trainer.ModelTrainerPipeline()

    def run(self):
        self.stage_01.main()
        self.stage_02.main()
        self.stage_03.main()
        self.stage_04.main()
        
        # push artifacts to cloud
        push_to_cloud()

