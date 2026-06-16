from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.models import Job, UserEvent
from app.db.session import get_db
from app.schemas.events import FeedbackEventCreate, FeedbackEventResponse


router = APIRouter(prefix="/events", tags=["events"])


@router.post("/feedback", response_model=FeedbackEventResponse, status_code=status.HTTP_201_CREATED)
def create_feedback_event(payload: FeedbackEventCreate, db: Session = Depends(get_db)) -> UserEvent:
    job = db.get(Job, payload.job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    event = UserEvent(user_id=payload.user_id, job_id=payload.job_id, event_type=payload.event_type)
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

