import json
import time
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.db.models import Job
from app.db.session import SessionLocal


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def run_job(job_id: str) -> None:
    """
    Replace this function with the real SkunkScrape execution pipeline.

    Current behavior:
    - marks the job as running
    - simulates a unit of work
    - stores a simple result payload
    """
    db: Session = SessionLocal()

    try:
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            return

        job.status = "running"
        job.started_at = utcnow()
        db.add(job)
        db.commit()
        db.refresh(job)

        time.sleep(2)

        result = {
            "summary": "Job completed successfully",
            "target": job.target,
            "job_type": job.job_type,
            "records_found": 0,
            "items": [],
            "next_step": "Replace app/services/job_runner.py with your actual scraping engine.",
        }

        job.status = "completed"
        job.completed_at = utcnow()
        job.result_json = json.dumps(result)
        db.add(job)
        db.commit()
    except Exception as exc:
        job = db.query(Job).filter(Job.id == job_id).first()
        if job:
            job.status = "failed"
            job.error = str(exc)
            job.completed_at = utcnow()
            db.add(job)
            db.commit()
    finally:
        db.close()
