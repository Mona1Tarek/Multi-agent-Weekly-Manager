"""
api/routes/timetable.py
------------------------
POST /timetable  — Send a task list and receive a weekly timetable.

Uses the LangChain chain by default. Pass use_crewai=true for the agent version.
"""

from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from core.pdf_utils import save_output
from agents.timetable.chain import run_timetable_chain

router = APIRouter()


class TimetableRequest(BaseModel):
    """Request body for the timetable endpoint."""
    schedule_text: str = (
        "- Task 1: Complete project report (High Priority, 2 hours)\n"
        "- Task 2: Team meeting (Medium Priority, 1 hour)\n"
        "- Task 3: Respond to emails (Low Priority, 30 minutes)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "schedule_text": (
                    "- Task 1: Complete project report (High Priority, 2 hours)\n"
                    "- Task 2: Team meeting (Medium Priority, 1 hour)\n"
                    "- Task 3: Respond to emails (Low Priority, 30 minutes)"
                )
            }
        }


@router.post(
    "/",
    summary="Generate a weekly timetable",
    response_description="JSON with timetable text and path to the generated PDF",
)
async def generate_timetable(
    body: TimetableRequest,
    save_pdf: bool = Query(True, description="Also save the timetable as a PDF in the output/ directory"),
    use_crewai: bool = Query(False, description="Use the full CrewAI timetable agent instead of the LangChain chain"),
):
    """
    Generate a structured weekly timetable from a plain-text task list.

    - **schedule_text**: One task per line, with priority and estimated duration.
    - **save_pdf**: When `true`, also writes a `timetable.pdf` to the output directory.
    - **use_crewai**: When `true`, runs the heavier CrewAI timetable agent instead.
    """
    if not body.schedule_text.strip():
        raise HTTPException(status_code=400, detail="schedule_text must not be empty.")

    if use_crewai:
        from agents.timetable.agent import build_timetable_agent, build_timetable_task
        from crewai import Crew
        agent = build_timetable_agent()
        task = build_timetable_task(agent, body.schedule_text)
        crew = Crew(agents=[agent], tasks=[task])
        result = crew.kickoff()
        timetable = result.tasks_output[0].raw
    else:
        timetable = run_timetable_chain(body.schedule_text)

    pdf_path = None
    if save_pdf:
        filename = "crewai_timetable.pdf" if use_crewai else "langchain_timetable.pdf"
        pdf_path = save_output(timetable, filename, table=True)

    return JSONResponse(content={
        "timetable": timetable,
        "pdf_saved": pdf_path,
        "engine": "crewai" if use_crewai else "langchain",
    })
