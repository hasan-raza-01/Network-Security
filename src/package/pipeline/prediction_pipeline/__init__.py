from package.configuration import PredictionConfig
from package.components.prediction import PredictionComponents
from dataclasses import dataclass
import numpy as np


@dataclass
class PredictionPipeline:
    model: any
    preprocessor: any
    data: np.ndarray

    def main(self)->list:
        predictor = PredictionComponents(PredictionConfig)
        return predictor.predict(self.model, self.preprocessor, self.data)


