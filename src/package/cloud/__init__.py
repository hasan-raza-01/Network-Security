import os, sys
from package.exception import CustomException
from package.logger import logging


def push_to_cloud():
    try:
        os.system("dvc push")
        logging.info("artifacts succcessfully pushed to cloud")
    except Exception as e:
        logging.exception(e)
        raise CustomException(e, sys)
