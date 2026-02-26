Financial Document Analyzer

AI-powered financial PDF analysis system built using FastAPI + CrewAI + OpenRouter + SQLAlchemy.

Overview

This system analyzes financial PDFs such as:

10-K reports
10-Q reports
Earnings releases
Quarterly updates
Investor presentations
It extracts structured financial insights including:

Revenue
Gross profit
Net income
EPS
Cash position
Business segments
YoY changes

Risk factors
Results are rendered in a clean executive-style UI with chart visualization.

Bugs Identified & Fixed

1️⃣ CrewAI Task Validation Error

Missing expected_output
Added required field to ensure deterministic execution

2️⃣ CrewOutput Parsing Crash

Handled CrewOutput object safely
Extracted .raw output correctly

3️⃣ JSON Markdown Wrapping

Removed ```json fences before parsing
Enforced strict JSON output

4️⃣ Static Folder Runtime Error

Fixed app mounting order
Created proper static/ and templates/ structure

5️⃣ Python Version Conflict

Used Python 3.11 virtual environment for compatibility

6️⃣ Dependency Conflicts

Resolved chromadb / embedchain version mismatch

Prompt Optimization

Original prompts:

1.Allowed markdown output
2.Returned inconsistent structures
3.Hallucinated commentary
4.Improved prompts:
5.Enforced strict JSON
6.Defined explicit schema
7.Disallowed markdown
8.Required numeric values
9.Prevented extra explanation

This made output deterministic and production-safe.

Database Integration
Uses SQLAlchemy to store:
Analysis ID
Filename
JSON result
Timestamp
Ensures persistence and scalability.

UI Features

Modern landing page
Drag-and-drop upload
Executive-style results page
Chart.js visualization
Dark mode toggle
Responsive layout

Project Structure
financial_analyzer/
│
├── main.py
├── agents.py
├── tools.py
├── database.py
├── celery_worker.py
│
├── templates/
├── static/
│
└── requirements.txt

⚙️ Setup Instructions

1️⃣ Clone Repository
git clone https://github.com/shubham-899844/financial_analyzer.git
cd financial_analyzer
2️⃣ Create Virtual Environment
python3.11 -m venv venv
source venv/bin/activate
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Configure Environment
Create .env:
OPENROUTER_API_KEY=your_api_key_here
5️⃣ Run Application
python -m uvicorn main:app --reload

Open:
http://127.0.0.1:8000

API Documentation
After running server:
http://127.0.0.1:8000/docs
POST /analyze
Accepts:
Mulipart PDF file
Returns:
Structured financial JSON

Bonus Enhancements
1.Database persistence
2.Prompt enforcement
3.Clean architecture
4.Chart visualization
5.UI improvements
6.Production-ready structure