from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.models import Job, User
from app.deps import get_current_user, get_db
from app.schemas.job import JobResult

router = APIRouter(prefix="/results")


@router.get("/{id}", response_model=JobResult, summary="Get job result")
def get_result(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> JobResult:
    job = db.query(Job).filter(Job.id == id, Job.owner_id == current_user.id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Result not found")

    if job.status != "completed":
        raise HTTPException(
            status_code=409,
            detail=f"Result not ready. Current status: {job.status}",
        )

    return JobResult.model_validate(job)
