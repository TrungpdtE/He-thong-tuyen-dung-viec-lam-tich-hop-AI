from dataclasses import dataclass
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.db.models import Job, Resume, UserEvent
from app.services.embedding_service import embedding_service


EVENT_WEIGHTS = {
    "click": 0.20,
    "save": 0.60,
    "apply": 1.00,
}


@dataclass
class FeatureResult:
    vector: list[float]
    matched_skills: list[str]
    missing_skills: list[str]
    embedding_similarity: float
    skill_overlap: float
    job_popularity: float
    user_click_score: float
    recency_score: float


def build_feature_vector(db: Session, resume: Resume, job: Job, user_id: int | None) -> FeatureResult:
    embedding_similarity = compute_embedding_similarity(resume, job)
    skill_overlap, matched_skills, missing_skills = compute_skill_overlap_score(resume.parsed_skills, job.required_skills)
    job_popularity = compute_job_popularity_score(db, job.id)
    user_click_score = compute_user_click_score(db, user_id, job.id)
    recency_score = compute_recency_score(job.created_at)

    return FeatureResult(
        vector=[embedding_similarity, skill_overlap, job_popularity, user_click_score, recency_score],
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        embedding_similarity=embedding_similarity,
        skill_overlap=skill_overlap,
        job_popularity=job_popularity,
        user_click_score=user_click_score,
        recency_score=recency_score,
    )


def compute_embedding_similarity(resume: Resume, job: Job) -> float:
    return embedding_service.similarity(resume.raw_text, job.description)


def compute_skill_overlap_score(resume_skills: list[str], job_skills: list[str]) -> tuple[float, list[str], list[str]]:
    resume_lookup = {skill.lower() for skill in resume_skills}
    matched = [skill for skill in job_skills if skill.lower() in resume_lookup]
    missing = [skill for skill in job_skills if skill.lower() not in resume_lookup]

    if not job_skills:
        return 0.0, matched, missing

    score = len(matched) / len(job_skills)
    return max(0.0, min(1.0, score)), matched, missing


def compute_job_popularity_score(db: Session, job_id: int) -> float:
    events = db.query(UserEvent).filter(UserEvent.job_id == job_id).all()
    raw_score = sum(EVENT_WEIGHTS.get(event.event_type, 0.0) for event in events)
    return max(0.0, min(1.0, raw_score / 5.0))


def compute_user_click_score(db: Session, user_id: int | None, job_id: int) -> float:
    if user_id is None:
        return 0.0

    events = db.query(UserEvent).filter(UserEvent.user_id == user_id, UserEvent.job_id == job_id).all()
    raw_score = sum(EVENT_WEIGHTS.get(event.event_type, 0.0) for event in events)
    return max(0.0, min(1.0, raw_score))


def compute_recency_score(created_at: datetime | None) -> float:
    if created_at is None:
        return 0.5

    now = datetime.now(timezone.utc)
    created = created_at if created_at.tzinfo else created_at.replace(tzinfo=timezone.utc)
    age_days = max(0, (now - created).days)
    return max(0.0, min(1.0, 1.0 - (age_days / 30.0)))

