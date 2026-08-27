from sqlalchemy.orm import Session

from app.db.repositories.job_repository import JobRepository


class JobService:

    def __init__(self, db: Session):
        self.repository = JobRepository(db)

    def create_job(
        self,
        job_id: str,
        job_name: str,
    ):
        return self.repository.create(
            job_id=job_id,
            job_name=job_name,
        )

    def get_job(
        self,
        job_id: str,
    ):
        return self.repository.get(job_id)

    def update_status(
        self,
        job_id: str,
        status: str,
    ):
        return self.repository.update_status(
            job_id=job_id,
            status=status,
        )