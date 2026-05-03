"""
api/routes/summarizer.py
-------------------------
POST /summarize  — Upload a PDF and receive a summary.

Uses the LangChain chain for fast HTTP responses.
A CrewAI flag can be passed to use the multi-agent version instead.
"""

import os
import tempfile

from fastapi import APIRouter, File, UploadFile, Query, HTTPException
from fastapi.responses import JSONResponse

from core.pdf_utils import read_pdf, save_output
from agents.summarizer.chain import run_summarizer_chain

router = APIRouter()


@router.post(
    "/",
    summary="Summarize a PDF document",
    response_description="JSON with summary text and path to the generated PDF",
)
async def summarize_pdf(
    file: UploadFile = File(..., description="PDF file to summarize"),
    save_pdf: bool = Query(True, description="Also save the summary as a PDF in the output/ directory"),
    use_crewai: bool = Query(False, description="Use the full CrewAI agent instead of the LangChain chain"),
):
    """
    Upload a PDF and receive a summary.

    - **file**: Any valid `.pdf` file.
    - **save_pdf**: When `true`, also writes `langchain_summary.pdf` to the output directory.
    - **use_crewai**: When `true`, runs the heavier CrewAI summarizer agent instead.
    """
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    # Write the uploaded file to a temp location so pdf_utils can read it
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

    if use_crewai:
        from agents.summarizer.agent import build_summarizer_agent, build_summarizer_task
        from crewai import Crew
        agent = build_summarizer_agent()
        task = build_summarizer_task(agent, pdf_text)
        crew = Crew(agents=[agent], tasks=[task])
        result = crew.kickoff()
        summary = result.tasks_output[0].raw
    else:
        summary = run_summarizer_chain(pdf_text)

    pdf_path = None
    if save_pdf:
        filename = "crewai_summary.pdf" if use_crewai else "langchain_summary.pdf"
        pdf_path = save_output(summary, filename)

    return JSONResponse(content={
        "summary": summary,
        "pdf_saved": pdf_path,
        "engine": "crewai" if use_crewai else "langchain",
    })
