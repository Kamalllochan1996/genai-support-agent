import uuid


class JobManager:

    def __init__(self):
        self.jobs = {}

    def create_job(self) -> str:

        job_id = str(uuid.uuid4())

        self.jobs[job_id] = {
            "status": "pending",
        }

        return job_id

    def update_status(
        self,
        job_id: str,
        status: str,
    ) -> None:

        if job_id in self.jobs:
            self.jobs[job_id]["status"] = status

    def get_status(
        self,
        job_id: str,
    ) -> dict | None:

        return self.jobs.get(job_id)


job_manager = JobManager()