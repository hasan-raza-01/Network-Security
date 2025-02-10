from package.pipeline import (
    stage_01_data_ingestion,
    stage_02_data_validation,
    stage_03_data_transformation,
    stage_04_model_trainer
)
from package.constants import TrainingPipelineConstants
from dataclasses import dataclass
from package.cloud import S3Sync
from package.exception import CustomException
import sys


@dataclass
class TrainingPipeline:
    stage_01 = stage_01_data_ingestion.DataIngestionPipeline()
    stage_02 = stage_02_data_validation.DataValidationPipeline()
    stage_03 = stage_03_data_transformation.DataTransformationPipeline()
    stage_04 = stage_04_model_trainer.ModelTrainerPipeline()

    ## local artifact is going to s3 bucket    
    def push_to_cloud(self):
        try:
            s3_bucket = TrainingPipelineConstants.AWS_BUCKET_NAME
            bucket_folder = TrainingPipelineConstants.AWS_BUCKET_FOLDER_NAME
            aws_s3_bucket_url = f"s3://{s3_bucket}/{bucket_folder}"
            local_folder = TrainingPipelineConstants.LOCAL_FOLDER_NAME
            # push artifacts to cloud
            syncer = S3Sync()
            syncer.sync(aws_s3_bucket_url, local_folder, cmd="push")
        except Exception as e:
            raise CustomException(e,sys)

    def run(self):
        self.stage_01.main()
        self.stage_02.main()
        self.stage_03.main()
        self.stage_04.main()
        self.push_to_cloud()
        
        


