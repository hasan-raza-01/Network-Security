from package.exception import CustomException
from sklearn.model_selection import GridSearchCV
from box import ConfigBox
from pathlib import Path
import numpy as np
import sys
import os
import yaml
import pickle
import json
from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score

def create_dirs(path:str)->None:
    """creates directory if path do not exists

    Args:
        path (str): directory path for creation
    """
    try:
        os.makedirs(Path(path), exist_ok=True)
    except Exception as e:
        raise CustomException(e, sys)
    

def read_yaml(path:str)->ConfigBox:
    """reads the yaml file available in path

    Args:
        path (str): path of the yaml file

    Returns:
        ConfigBox: dict["key"] = value --------->  dict.key = value
    """
    try:
        with open(Path(path), "r") as yaml_file_obj:
            return ConfigBox(yaml.safe_load(yaml_file_obj))
    except Exception as e:
        raise CustomException(e, sys)
    

def save_yaml(content:any, file_path:str)->None:
    """saves the yaml file with provided content

    Args:
        content (any): content for the yaml file
        path (str): path to save the file
    """
    try:
        with open(Path(file_path), "w") as file:
            yaml.safe_dump(content, file)
    except Exception as e:
        raise CustomException(e, sys)
    

def save_obj(obj:any, path:str)->None:
    """saves the object on given path

    Args:
        obj (any): object to dump
        path (str): path to dump the object
    """
    try:
        with open(Path(path), "wb") as file:
            pickle.dump(obj, file)
    except Exception as e:
        raise CustomException(e, sys)
    

def load_obj(path:str):
    """load the object available in path

    Args:
        path (str): path of the object
    """
    try:
        with open(Path(path), "rb") as file:
            return pickle.load(file)
    except Exception as e:
        raise CustomException(e, sys)
    

def save_json(data:dict, path:str)->None:
    """saves the dictoanary into json file

    Args:
        data (dict): dictionary data to save in form of json
        path (str): path to save the file
    """
    try:
        # Serializing json
        json_object = json.dumps(data, indent=4)

        # Writing to sample.json
        with open(Path(path), "w") as outfile:
            outfile.write(json_object)
    except Exception as e:
        raise CustomException(e, sys)
    

def load_json(path:str)->dict:
    """reads the data present inside the file provided in \'path\' variable

    Args:
        path (str): path of the json file

    Returns:
        json: json of data inside file
    """
    try:
        # Opening JSON file
        with open(Path(path), 'r') as openfile:

            # Reading from json file
            json_object = json.load(openfile)
            return json_object
    except Exception as e:
        raise CustomException(e, sys)
    

def evaluate_models(X_train:np.array, y_train:np.array, X_test:np.array, y_test:np.array, models:dict, params:dict)->dict[dict]:
    """evaluates model with provided parameters and data

    Args:
        X_train (np.array): input features of train data
        y_train (np.array): output features of train data
        X_test (np.array): input features of test data
        y_test (np.array): output features of test data
        models (dict): dict(key=model_name, value=model_object)
        params (dict): dict(key=model_name, value=model_parameters)

    Returns:
        dict[dict]: dict(
            key=model_score (type=int) 
           value=dict(
                    key=model_name (type=str) 
                   value=model_params (type=dict) 
                )
        )
    """
    try:
        report = dict()
        for model_name, model in models.items():
            param = params[model_name]

            # hyper parameter tuning
            grid = GridSearchCV(model, param)
            grid.fit(X_train, y_train)

            # fit best params
            model.set_params(**grid.best_params_)
            model.fit(X_train, y_train)

            # predict test data 
            test_y_pred = model.predict(X_test)

            # model test data performance score calculation
            score = accuracy_score(y_test, test_y_pred)

            report[model_name] = {f"score":score, f"params":grid.best_params_}

        return report
    except Exception as e:
        raise CustomException(e, sys)
    

def get_performance_report(y_train:np.array, y_test:np.array, train_pred:np.array, test_pred:np.array)->dict:
    """gives evaluation report for scores of f1, precision, recall, accuracy

    Args:
        train_pred (np.array): _description_
        test_pred (np.array): _description_

    Returns:
        dict: _description_
    """
    try:
        # model performance score
        train_f1_score = f1_score(y_train, train_pred)
        train_precision_score = precision_score(y_train, train_pred)
        train_recall_score = recall_score(y_train, train_pred)
        train_accuracy_score = accuracy_score(y_train, train_pred)

        test_f1_score = f1_score(y_test, test_pred)
        test_precision_score = precision_score(y_test, test_pred)
        test_recall_score = recall_score(y_test, test_pred)
        test_accuracy_score = accuracy_score(y_test, test_pred)

        train_scores = {
            "f1_score": train_f1_score,
            "precision_score": train_precision_score,
            "recall_score": train_recall_score,
            "accuracy_score": train_accuracy_score
        }

        test_scores = {
            "f1_score": test_f1_score,
            "precision_score": test_precision_score,
            "recall_score": test_recall_score,
            "accuracy_score": test_accuracy_score
        }

        model_scores = {"train":train_scores, "test":test_scores}

        return model_scores
    except Exception as e:
        raise CustomException(e, sys)


