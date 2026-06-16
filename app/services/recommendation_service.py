from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.models import Job, Resume
from app.services.feature_engineering import FeatureResult, build_feature_vector
from app.services.ranking_model import ranking_model_service


class ResumeNotFoundError(ValueError):
    pass


@dataclass
class RecommendationResult:
    job_id: int
    title: str
    company: str
    score: float
    matched_skills: list[str]
    missing_skills: list[str]
    reason: str


def rank_jobs_for_resume(db: Session, resume_id: int, user_id: int | None = None) -> list[RecommendationResult]:
    resume = db.get(Resume, resume_id)
    if resume is None:
        raise ResumeNotFoundError(f"Resume {resume_id} not found")

    jobs = db.query(Job).all()
    ranked: list[RecommendationResult] = []

    for job in jobs:
        features = build_feature_vector(db, resume, job, user_id)
        model_score = ranking_model_service.predict_score(features.vector)
        behavior_boost = 0.08 * features.user_click_score
        final_score = max(0.0, min(1.0, model_score + behavior_boost))

        ranked.append(
            RecommendationResult(
                job_id=job.id,
                title=job.title,
                company=job.company,
                score=round(final_score, 4),
                matched_skills=features.matched_skills,
                missing_skills=features.missing_skills,
                reason=build_reason(features),
            )
        )

    ranked.sort(key=lambda item: item.score, reverse=True)
    return ranked[: get_settings().top_k_jobs]


def build_reason(features: FeatureResult) -> str:
    reasons: list[str] = []

    if features.embedding_similarity >= 0.45:
        reasons.append("resume text is semantically close to the job description")
    if features.skill_overlap >= 0.5:
        reasons.append(f"{len(features.matched_skills)} required skills matched")
    if features.job_popularity > 0:
        reasons.append("this job has positive global engagement signals")
    if features.user_click_score > 0:
        reasons.append("your past behavior indicates interest in this job")
    if features.recency_score >= 0.8:
        reasons.append("the job is recent")
    if features.missing_skills:
        reasons.append("missing skills: " + ", ".join(features.missing_skills[:3]))

    return "; ".join(reasons) if reasons else "Recommended by the ML ranking model."

