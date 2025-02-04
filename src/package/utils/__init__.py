from package.exception import CustomException
from box import ConfigBox
from pathlib import Path
import sys
import os
import yaml
import pickle


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
    
