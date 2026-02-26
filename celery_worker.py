from celery import Celery
from crewai import Crew, Process
from agents import financial_analyst, investment_advisor, risk_assessor
from task import analyze_financial_document, investment_analysis, risk_assessment
from database import SessionLocal, AnalysisJob
import os

celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

@celery_app.task(bind=True, max_retries=3)
def run_crew_task(self, job_id, query, file_path):

    db = SessionLocal()

    try:
        job = db.query(AnalysisJob).filter(AnalysisJob.id == job_id).first()

        if not job:
            return

        job.status = "processing"
        db.commit()

        # Secure file path
        SAFE_BASE = os.path.abspath("data")
        file_path = os.path.abspath(file_path)

        if not file_path.startswith(SAFE_BASE):
            raise ValueError("Invalid file path")

        crew = Crew(
            agents=[financial_analyst, investment_advisor, risk_assessor],
            tasks=[analyze_financial_document, investment_analysis, risk_assessment],
            process=Process.sequential
        )

        result = crew.kickoff(inputs={
            "query": query,
            "file_path": file_path
        })

        job.result = str(result)
        job.status = "completed"
        db.commit()

    except Exception as e:
        job.status = "failed"
        job.result = str(e)
        db.commit()
        raise self.retry(exc=e, countdown=10)

    finally:
        db.close()