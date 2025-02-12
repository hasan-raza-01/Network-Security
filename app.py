import sys
import os

import certifi
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()
mongo_db_url = os.getenv("URI")
print(mongo_db_url)
import pymongo
from package.exception import CustomException
from package.pipeline.training_pipeline import TrainingPipeline
from package.pipeline.prediction_pipeline import PredictionPipeline
from package.configuration import ModelTrainerConfig, DataTransformationConfig

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile,Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd
import numpy as Numpy
from package.utils import load_obj, load_json
import bentoml, dagshub




client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

from package.constants import DataIngestionConstants

database = client[DataIngestionConstants.DATABASE_NAME]
collection = database[DataIngestionConstants.COLLECTION_NAME]

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        train_pipeline=TrainingPipeline()
        train_pipeline.run()
        return Response("Training is successful")
    except Exception as e:
        raise CustomException(e,sys)
    
@app.post("/predict")
async def predict_route(request: Request,file: UploadFile = File(...)):
    try:
        df = pd.DataFrame(Numpy.load(file.file))
        input_data = df.iloc[:, :-1]
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
        #df['predicted_column'].replace(-1, 0)
        #return df.to_json()
        df["Result"] = pred
        table_html = df.to_html(classes='table table-striped')
        #print(table_html)
        return templates.TemplateResponse("index.html", {"request": request, "table": table_html})
        
    except Exception as e:
            raise CustomException(e,sys)

    
if __name__=="__main__":
    app_run(app,host="0.0.0.0",port=8000)
