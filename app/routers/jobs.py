from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.models import Job, User
from app.deps import get_current_user, get_db
from app.schemas.job import JobCreate, JobDetail
from app.services.job_runner import run_job

router = APIRouter(prefix="/jobs")


@router.post("", response_model=JobDetail, status_code=status.HTTP_201_CREATED, summary="Create a scrape job")
def create_job(
    payload: JobCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> JobDetail:
    job = Job(
        owner_id=current_user.id,
        job_type=payload.job_type,
        target=str(payload.target),
        options_json=payload.options.model_dump_json() if payload.options else None,
        status="queued",
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    background_tasks.add_task(run_job, job.id)
    return JobDetail.model_validate(job)


@router.get("/{id}", response_model=JobDetail, summary="Get job state")
def get_job(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> JobDetail:
    job = db.query(Job).filter(Job.id == id, Job.owner_id == current_user.id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return JobDetail.model_validate(job)
