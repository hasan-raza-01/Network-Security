from package.entity import DataTransformationConfigEntity
from package.exception import CustomException
from package.logger import logging
from package.utils import (load_json, save_json, create_dirs, save_obj, evaluate_models, get_performance_report)
from package.entity import ModelTrainerConfigEntity
from dataclasses import dataclass
import mlflow, bentoml, dagshub
from urllib.parse import urlparse
from retrying import retry
import sys
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)


@dataclass
class ModelTrainerComponents:
    data_transformation_config: DataTransformationConfigEntity
    model_trainer_config: ModelTrainerConfigEntity

    # @retry(stop_max_attempt_number=2, wait_fixed=10000)
    def track_with_mlflow(params:dict, metrics:dict, train_data:np.array, model, mlflow_tracking_uri:str,
                       dagshub_repo_owner:str, dagshub_repo_name:str, model_name:str)->str:
        """tracks and logging of parameters, metrics and model with version

        Args:
            params (dict): parameters to log
            metrics (dict): metrics to log
            train_data (np.array): train data for model signature
            model (sklearn model): model from sklearn module
            mlflow_tracking_uri (str): uri of user's mlflow page
            dagshub_repo_owner (str): dagshub repository owner name of above user(github username)
            dagshub_repo_name (str): dagshub repository name
            model_name (str): name of model belongs to sklearn module for mlflow registration

        Returns:
            str: message of log completion
        """
        try:
            with mlflow.start_run():

                # log parameters
                mlflow.log_params(params)

                # log metrics
                mlflow.log_metrics(metrics)

                # model signature for model registration
                infer_signature = mlflow.models.infer_signature(train_data, model.predict(train_data))

                # connecting with dagshub repository
                dagshub.init(repo_owner=dagshub_repo_owner, repo_name=dagshub_repo_name, mlflow=True)
                
                mlflow.set_tracking_uri(mlflow_tracking_uri)
                
                tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

                if tracking_url_type_store != "file":
                    mlflow.sklearn.log_model(model, model_name,
                                            registered_model_name=model_name, 
                                            signature=infer_signature
                                    )
                else:
                    mlflow.sklearn.log_model(model, model_name, 
                                            signature=infer_signature
                                    )

            # saving model locally
            bentoml.keras.save_model(model_name, model)

            return "mlflow tracking and logging successful"
        except Exception as e:
            raise CustomException(e, sys)
    


    def initiate_training(self):
        try:
            logging.info("In initiate_training")
            
            # create required dir's
            create_dirs(self.model_trainer_config.ARITFACTS_ROOT_DIR_PATH)
            create_dirs(self.model_trainer_config.MODEL_ROOT_DIR_PATH)
            create_dirs(self.model_trainer_config.ESTIMATOR_ROOT_DIR_PATH)
            logging.info("created required dir's")

            # models list
            models = {
                    "Random Forest": RandomForestClassifier(verbose=1),
                    "Decision Tree": DecisionTreeClassifier(),
                    "Gradient Boosting": GradientBoostingClassifier(verbose=1),
                    "Logistic Regression": LogisticRegression(verbose=1),
                    "AdaBoost": AdaBoostClassifier(),
                }
            
            # collect params
            params = load_json(self.model_trainer_config.PARAMS_FILE_PATH)
            logging.info("params collected")

            # transformed data collection
            train_data = np.load(self.data_transformation_config.TRAIN_FILE_PATH)
            test_data = np.load(self.data_transformation_config.TEST_FILE_PATH)
            logging.info("transformed data collected")

            # extract input and output features
            # train data
            X_train = train_data[:, :-1]
            y_train = train_data[:, -1]

            # test data
            X_test = test_data[:, :-1]
            y_test = test_data[:, -1]

            # get evaluation report
            model_performance_report = evaluate_models(X_train, y_train, X_test, y_test, models, params)
            logging.info("evaluation report collected")

            # save evaluation report
            evaluation_report_path = self.model_trainer_config.EVALUATION_FILE_PATH
            save_json(model_performance_report, evaluation_report_path)
            logging.info(f"saved evaluation report at {evaluation_report_path}")

            # get best model name 
            best_model_name, _ = max(sorted([(model_name, model_performance_report[model_name]["score"]) for model_name in model_performance_report.keys()]))

            # get best params for best model 
            best_params = model_performance_report[best_model_name]["best_params"]

            # get best performed model from scratch
            model = models[best_model_name]

            # set best params for model
            model.set_params(**best_params)

            # train model
            model.fit(X_train, y_train)

            # save model
            model_file_path = self.model_trainer_config.ESTIMATOR_FILE_PATH
            save_obj(model, model_file_path)
            logging.info(f"Estimator \'{str(model)}\' saved at {model_file_path}")

            # model prediction
            train_y_pred = model.predict(X_train)
            test_y_pred = model.predict(X_test)

            # get evaluation score
            model_scores = get_performance_report(y_train, y_test, train_y_pred, test_y_pred)
            logging.info(f"\'{str(model)}\' scores: {model_scores}")

            # mlflow tracking
            test_scores = model_scores["test"]
            uri = "https://dagshub.com/hasan-raza-01/Network-Security.mlflow/"
            repo_owner= 'hasan-raza-01'
            repo_name= 'Network-Security'
            model_name = "RandomForestClassifier"
            message = self.track_with_mlflow(best_params,  test_scores, X_train, model, 
                                             uri, repo_owner, repo_name, model_name)
            logging.info(message)

            # create and save model config report
            model_config = {"Estimator":str(model), "scores":model_scores, "params":best_params}
            config_file_path = self.model_trainer_config.CONFIG_FILE_PATH
            save_json(model_config, config_file_path)
            logging.info(f"Estimator \'{str(model)}\' configuration file saved at {config_file_path}")

            logging.info("Out initiate_training")
        except Exception as e:
            raise CustomException(e, sys)
        

