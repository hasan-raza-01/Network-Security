from package.entity import DataTransformationConfigEntity
from package.exception import CustomException
from package.logger import logging
from package.utils import (load_json, save_json, create_dirs, save_obj, evaluate_models, get_performance_report)
from package.entity import ModelTrainerConfigEntity
from dataclasses import dataclass
import mlflow, dagshub, bentoml
from urllib.parse import urlparse
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
                    "RandomForestClassifier": RandomForestClassifier(verbose=1),
                    "DecisionTreeClassifier": DecisionTreeClassifier(),
                    "GradientBoostingClassifier": GradientBoostingClassifier(verbose=1),
                    "LogisticRegression": LogisticRegression(verbose=1),
                    "AdaBoostClassifier": AdaBoostClassifier(),
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
            best_params = model_performance_report[best_model_name]["params"]

            # login in dagshub
            # cmd: dagshub login --token <token from account>
            # connecting with dagshub repository
            dagshub.init(repo_owner='hasan-raza-01', repo_name='Network-Security', mlflow=True)

            # mlflow tracking
            with mlflow.start_run():
                # get best performed model from scratch
                model = models[best_model_name]

                # set best params for model
                model.set_params(**best_params)

                # train model
                model.fit(X_train, y_train)

                # save model
                model_file_path = self.model_trainer_config.ESTIMATOR_FILE_PATH
                save_obj(model, model_file_path)
                logging.info(f"model {best_model_name} saved at {model_file_path}")

                # model prediction
                train_y_pred = model.predict(X_train)
                test_y_pred = model.predict(X_test)

                # get evaluation score
                model_scores = get_performance_report(y_train, y_test, train_y_pred, test_y_pred)
                logging.info(f"model scores: {model_scores}")

                # create and save model config report
                model_config = {"model":best_model_name, "scores":model_scores, "params":best_params}
                config_file_path = self.model_trainer_config.CONFIG_FILE_PATH
                save_json(model_config, config_file_path)
                logging.info(f"model {best_model_name} configurations saved at {config_file_path}")

                # log parameters
                mlflow.log_params(best_params)

                # log metrics
                mlflow.log_metrics(model_scores["test"])

            
                # model signature for model registration
                infer_signature = mlflow.models.infer_signature(X_train, model.predict(X_train))
                
                uri = "https://dagshub.com/hasan-raza-01/Network-Security.mlflow"
                mlflow.set_tracking_uri(uri)
                
                tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

                if tracking_url_type_store != "file":
                    mlflow.sklearn.log_model(model, best_model_name,
                                            registered_model_name=best_model_name, 
                                            signature=infer_signature
                                    )
                else:
                    mlflow.sklearn.log_model(model, best_model_name,
                                            signature=infer_signature
                                    )
            logging.info("mlflow tracking and logging successful")

            logging.info("Out initiate_training")
        except Exception as e:
            raise CustomException(e, sys)
        

