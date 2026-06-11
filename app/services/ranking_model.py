import math
import pickle
from pathlib import Path

from app.core.config import get_settings


class LogisticRankingModel:
    def __init__(self, weights: list[float] | None = None, bias: float = 0.0):
        self.weights = weights or [0.0, 0.0, 0.0, 0.0, 0.0]
        self.bias = bias

    def predict(self, features: list[float]) -> float:
        z = self.bias + sum(weight * value for weight, value in zip(self.weights, features))
        return 1.0 / (1.0 + math.exp(-z))


class RankingModelService:
    def __init__(self, model_path: str | None = None):
        self.model_path = Path(model_path or get_settings().model_path)
        self._model: LogisticRankingModel | None = None

    def load_model(self) -> LogisticRankingModel:
        if self._model is not None:
            return self._model

        if self.model_path.exists():
            with self.model_path.open("rb") as file:
                self._model = pickle.load(file)
        else:
            self._model = LogisticRankingModel(weights=[2.0, 2.8, 0.8, 1.4, 0.4], bias=-2.2)

        print("Model loaded successfully", flush=True)
        return self._model

    def predict_score(self, features: list[float]) -> float:
        score = self.load_model().predict(features)
        return max(0.0, min(1.0, score))


ranking_model_service = RankingModelService()
