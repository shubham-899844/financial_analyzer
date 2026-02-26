import os
import json
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from database import init_db, get_db, AnalysisResult
from tools import extract_text_from_pdf
from agents import create_financial_analysis_crew

# Load environment variables
load_dotenv()

# 1️⃣ CREATE APP FIRST
app = FastAPI(title="Financial Document Analyzer")

# 2️⃣ THEN mount static
app.mount("/static", StaticFiles(directory="static"), name="static")

# 3️⃣ Initialize DB
init_db()

# 4️⃣ Setup templates
templates = Jinja2Templates(directory="templates")


# -------------------
# Home Route
# -------------------
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


# -------------------
# Analyze Route
# -------------------
@app.post("/analyze", response_class=HTMLResponse)
async def analyze_document(
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    try:
        text = extract_text_from_pdf(file.file)

        crew = create_financial_analysis_crew(text)
        crew_output = crew.kickoff()

        if hasattr(crew_output, "raw"):
            result_text = crew_output.raw
        else:
            result_text = str(crew_output)

        result_text = result_text.strip()

        if result_text.startswith("```"):
            result_text = result_text.replace("```json", "")
            result_text = result_text.replace("```", "")
            result_text = result_text.strip()

        if result_text.lower().startswith("json"):
            result_text = result_text[4:].strip()

        try:
            result_json = json.loads(result_text)
        except json.JSONDecodeError:
            result_json = {
                "error": "Model did not return valid JSON",
                "raw_output": result_text
            }

        entry = AnalysisResult(
            filename=file.filename,
            result=json.dumps(result_json)
        )

        db.add(entry)
        db.commit()
        db.refresh(entry)

        return templates.TemplateResponse(
            "result.html",
            {
                "request": request,
                "filename": file.filename,
                "analysis": result_json
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))