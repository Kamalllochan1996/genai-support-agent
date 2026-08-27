import uuid

from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session

from app.api.background_tasks import run_background_job
from app.db.dependencies import get_db
from app.db.services.job_service import JobService


router = APIRouter(
    prefix="/background",
    tags=["Background Tasks"],
)


def example_job(
    job_id: str,
) -> None:
    # Actual job processing will be connected later.
    pass


@router.post("")
def run_background_task(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):

    job_id = str(uuid.uuid4())

    job_service = JobService(db)

    job_service.create_job(
        job_id=job_id,
        job_name="test-job",
    )

    background_tasks.add_task(
        run_background_job,
        "test-job",
        example_job,
        job_id,
    )

    return {
        "status": "accepted",
        "job_id": job_id,
    }

@router.get("/{job_id}")
def get_job_status(
    job_id: str,
    db: Session = Depends(get_db),
):

    job_service = JobService(db)

    job = job_service.get_job(job_id)

    if job is None:
        return {
            "status": "not_found",
            "job_id": job_id,
        }

    return {
        "job_id": job.id,
        "job_name": job.job_name,
        "status": job.status,
    }