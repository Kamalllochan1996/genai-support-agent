from datetime import datetime

from sqlalchemy.orm import Session

from app.db.models import BackgroundJob


class JobRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        job_id: str,
        job_name: str,
    ) -> BackgroundJob:

        job = BackgroundJob(
            id=job_id,
            job_name=job_name,
            status="pending",
        )

        try:
            self.db.add(job)
            self.db.commit()
            self.db.refresh(job)

            return job

        except Exception:
            self.db.rollback()
            raise

    def get(
        self,
        job_id: str,
    ) -> BackgroundJob | None:

        return (
            self.db.query(BackgroundJob)
            .filter(
                BackgroundJob.id == job_id
            )
            .first()
        )

    def update_status(
        self,
        job_id: str,
        status: str,
    ) -> BackgroundJob | None:

        job = self.get(job_id)

        if job is None:
            return None

        try:
            job.status = status
            job.updated_at = datetime.utcnow()

            self.db.commit()
            self.db.refresh(job)

            return job

        except Exception:
            self.db.rollback()
            raise