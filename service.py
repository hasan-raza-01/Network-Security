import bentoml, dagshub
import numpy as Numpy
from package.pipeline.training_pipeline import TrainingPipeline
from package.pipeline.prediction_pipeline import PredictionPipeline
from package.configuration import DataTransformationConfig, ModelTrainerConfig
from package.utils import load_obj, load_json



@bentoml.service
class NetworkSecurity:

    @bentoml.api
    def train(self):
        pipeline = TrainingPipeline()
        pipeline.run()

        return "Training Completed"
    
    @bentoml.api
    def predict(self, input_data:Numpy.ndarray)->list:
        try:
            # Initialize Dagshub
            dagshub.init(repo_owner='hasan-raza-01', repo_name='Network-Security', mlflow=True)

            # # load model from mlflow
            model_name = load_json(ModelTrainerConfig.CONFIG_FILE_PATH)["model"]
            model = bentoml.mlflow.load_model(f"{model_name}:latest")
        except:
            model = load_obj(ModelTrainerConfig.ESTIMATOR_FILE_PATH)
        preprocessor = load_obj(DataTransformationConfig.PREPROCESSOR_PATH)
        pipeline = PredictionPipeline(model, preprocessor, data=input_data)
        pred = pipeline.main()
        return pred


