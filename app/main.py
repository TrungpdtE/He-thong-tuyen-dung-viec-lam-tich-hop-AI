from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import events, recommendation
from app.db.models import Base
from app.db.seed import seed_database
from app.db.session import SessionLocal, engine
from app.ml.train_model import ensure_model_exists
from app.services.ranking_model import ranking_model_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()

    ensure_model_exists()
    ranking_model_service.load_model()
    print("API ready", flush=True)
    yield


app = FastAPI(
    title="AI Job Tracker AI Engine V2",
    description="Production-style FastAPI backend for AI-powered job recommendation with ML ranking and feedback loop.",
    version="2.0.0",
    lifespan=lifespan,
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(recommendation.router)
app.include_router(events.router)
