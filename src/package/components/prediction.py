from dataclasses import dataclass
from package.exception import CustomException
from package.utils import create_dirs, save_json
from package.entity import PredictionConfigEntity
from package.logger import logging
from datetime import datetime
import sys


@dataclass
class PredictionComponents:
    prediction_config: PredictionConfigEntity

    def predict(self, model, preprocessor, data)->list:
        """makes model's prediction after transforming the data with preprocessor

        Args:
            model (sklearn model): model object for prediction
            preprocessor (): transformation object for data transformation
            data (dataframe): data for prediction

        Returns:
            list: _description_
        """
        try:
            logging.info("In predict")
            # create required dir's
            create_dirs(self.prediction_config.PREDICTION_ROOT_DIR_PATH)
            logging.info("created required dir's")

            # get model and preprocessor
            self.model = model
            self.preprocessor = preprocessor
            logging.info("Model and preprocessor loaded")

            # transform data and predict
            data = self.preprocessor.transform(data)
            prediction = self.model.predict(data).tolist()
            logging.info("Data transformed and predicted")

            # save prediction
            timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            prediction_file_path =f"{"\\".join(self.prediction_config.OUTPUT_FILE_PATH.split("\\")[:-1])}\\{timestamp}_{self.prediction_config.OUTPUT_FILE_PATH.split("\\")[-1]}"
            model_prediction_file_content = {"input":data.tolist(), "pred":prediction}
            save_json(model_prediction_file_content, prediction_file_path)
            logging.info(f"Prediction saved at {prediction_file_path}")

            logging.info("Out predict")            
            return prediction
        except Exception as e:
            logging.exception(e)
            raise CustomException(e, sys)
            

