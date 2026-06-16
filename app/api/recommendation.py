from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.recommendation import JobRecommendationResponse
from app.services.recommendation_service import ResumeNotFoundError, rank_jobs_for_resume


router = APIRouter(prefix="/recommend", tags=["recommendations"])


@router.get("/jobs/{resume_id}", response_model=list[JobRecommendationResponse])
def recommend_jobs(
    resume_id: int,
    user_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[JobRecommendationResponse]:
    try:
        results = rank_jobs_for_resume(db=db, resume_id=resume_id, user_id=user_id)
    except ResumeNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Resume not found") from exc

    return [JobRecommendationResponse(**result.__dict__) for result in results]

