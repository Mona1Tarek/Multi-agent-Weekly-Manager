"""
api/routes/crew.py
-------------------
POST /crew/run  — Run the full multi-agent CrewAI crew.

Accepts a PDF upload + task list, runs both the Summarizer and Timetable agents,
and returns both outputs with paths to the generated PDFs.
"""

import os
import tempfile

from fastapi import APIRouter, File, Form, UploadFile, HTTPException
from fastapi.responses import JSONResponse

from core.pdf_utils import read_pdf
from core.crew import run_crew

router = APIRouter()


@router.post(
    "/run",
    summary="Run the full multi-agent CrewAI crew",
    response_description="JSON with summary and timetable text plus PDF paths",
)
async def run_full_crew(
    file: UploadFile = File(..., description="PDF file to summarize"),
    schedule_text: str = Form(
        ...,
        description="Plain-text task list for the timetable (one task per line)",
        example=(
            "- Task 1: Complete project report (High Priority, 2 hours)\n"
            "- Task 2: Team meeting (Medium Priority, 1 hour)\n"
            "- Task 3: Respond to emails (Low Priority, 30 minutes)"
        ),
    ),
):
    """
    Run both the **Summarizer Agent** and **Timetable Agent** as a single CrewAI crew.

    - **file**: A `.pdf` file whose content will be summarized.
    - **schedule_text**: Task list string used to generate the weekly timetable.

    Both outputs are saved as PDFs in the `output/` directory.
    """
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    if not schedule_text.strip():
        raise HTTPException(status_code=400, detail="schedule_text must not be empty.")

    # Save uploaded file to a temp path
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        pdf_text = read_pdf(tmp_path)
    except Exception as exc:
        raise HTTPException(status_code=422, detail=f"Failed to read PDF: {exc}")
    finally:
        os.unlink(tmp_path)

    if not pdf_text.strip():
        raise HTTPException(status_code=422, detail="The PDF appears to contain no extractable text.")

    try:
        result = run_crew(pdf_text=pdf_text, schedule_text=schedule_text)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Crew run failed: {exc}")

    return JSONResponse(content={
        "summary": result["summary_text"],
        "timetable": result["timetable_text"],
        "summary_pdf": result["summary_pdf"],
        "timetable_pdf": result["timetable_pdf"],
    })
