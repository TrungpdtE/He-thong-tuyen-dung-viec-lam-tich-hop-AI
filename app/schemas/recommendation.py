from pydantic import BaseModel, Field


class JobRecommendationResponse(BaseModel):
    job_id: int
    title: str
    company: str
    score: float = Field(..., ge=0.0, le=1.0)
    matched_skills: list[str]
    missing_skills: list[str]
    reason: str

