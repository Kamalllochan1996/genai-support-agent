import logging

from app.db.database import SessionLocal
from app.db.services.job_service import JobService


logger = logging.getLogger(__name__)


def run_background_job(
    job_name: str,
    job_function,
    *args,
    **kwargs,
) -> None:

    job_id = kwargs.pop("job_id", None)

    db = SessionLocal()

    try:

        job_service = JobService(db)

        if job_id:
            job_service.update_status(
                job_id,
                "running",
            )

        logger.info(
            "Background job started | job=%s | job_id=%s",
            job_name,
            job_id,
        )

        job_function(
            *args,
            **kwargs,
        )

        if job_id:
            job_service.update_status(
                job_id,
                "completed",
            )

        logger.info(
            "Background job completed | job=%s | job_id=%s",
            job_name,
            job_id,
        )

    except Exception:

        if job_id:
            job_service.update_status(
                job_id,
                "failed",
            )

        logger.exception(
            "Background job failed | job=%s | job_id=%s",
            job_name,
            job_id,
        )

    finally:
        db.close()