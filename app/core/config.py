from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Job Tracker AI Engine V2"
    database_url: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/ai_job_tracker_ai_engine_v2"
    model_path: str = "app/ml/model.pkl"
    top_k_jobs: int = 10

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()

