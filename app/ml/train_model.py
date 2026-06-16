import os
import pickle
from pathlib import Path

from app.core.config import get_settings
from app.db.models import UserEvent
from app.db.session import SessionLocal
from app.services.ranking_model import LogisticRankingModel


SYNTHETIC_TRAINING_DATA = [
    ([0.95, 0.90, 0.10, 0.00, 1.00], 1),
    ([0.85, 0.80, 0.40, 0.20, 0.90], 1),
    ([0.70, 0.60, 0.30, 0.00, 0.80], 1),
    ([0.55, 0.50, 0.80, 1.00, 0.70], 1),
    ([0.30, 0.20, 0.10, 0.00, 0.60], 0),
    ([0.20, 0.10, 0.70, 0.00, 0.90], 0),
    ([0.40, 0.30, 0.30, 0.20, 0.20], 0),
    ([0.65, 0.70, 0.20, 0.60, 0.95], 1),
]


def train_model(training_data: list[tuple[list[float], int]], epochs: int = 800, learning_rate: float = 0.25) -> LogisticRankingModel:
    model = LogisticRankingModel()
    for _ in range(epochs):
        for features, label in training_data:
            prediction = model.predict(features)
            error = prediction - label
            model.weights = [weight - learning_rate * error * value for weight, value in zip(model.weights, features)]
            model.bias -= learning_rate * error
    return model


def load_event_training_data() -> list[tuple[list[float], int]]:
    if os.getenv("RETRAIN_WITH_USER_EVENTS", "false").lower() != "true":
        return []

    db = SessionLocal()
    try:
        events = db.query(UserEvent).all()
    except Exception:
        return []
    finally:
        db.close()

    samples: list[tuple[list[float], int]] = []
    for event in events:
        behavior = {"click": 0.2, "save": 0.6, "apply": 1.0}.get(event.event_type, 0.0)
        label = 1 if event.event_type in {"save", "apply"} else 0
        samples.append(([0.5, 0.5, 0.4, behavior, 0.8], label))
    return samples


def save_model(model: LogisticRankingModel) -> Path:
    model_path = Path(get_settings().model_path)
    model_path.parent.mkdir(parents=True, exist_ok=True)
    with model_path.open("wb") as file:
        pickle.dump(model, file)
    return model_path


def ensure_model_exists() -> Path:
    model_path = Path(get_settings().model_path)
    if model_path.exists():
        return model_path

    data = list(SYNTHETIC_TRAINING_DATA)
    data.extend(load_event_training_data())
    model = train_model(data)
    return save_model(model)


def main() -> None:
    data = list(SYNTHETIC_TRAINING_DATA)
    data.extend(load_event_training_data())
    model = train_model(data)
    model_path = save_model(model)
    print(f"Training samples: {len(data)}")
    print(f"Model saved to: {model_path}")
    print(f"Weights: {model.weights}")
    print(f"Bias: {model.bias}")


if __name__ == "__main__":
    main()

