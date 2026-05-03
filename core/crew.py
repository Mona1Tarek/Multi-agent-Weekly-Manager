"""
core/crew.py
------------
Assembles and runs the full multi-agent CrewAI crew (Summarizer + Timetable).
"""

from crewai import Crew
from agents.summarizer.agent import build_summarizer_agent, build_summarizer_task
from agents.timetable.agent import build_timetable_agent, build_timetable_task
from core.pdf_utils import save_output


def run_crew(pdf_text: str, schedule_text: str) -> dict:
    """
    Run the full multi-agent crew with both Summarizer and Timetable agents.

    Args:
        pdf_text:      Text content extracted from a PDF.
        schedule_text: Plain-text task list for the timetable.

    Returns:
        dict with keys:
            - summary_text  (str)
            - timetable_text (str)
            - summary_pdf   (str) – absolute path
            - timetable_pdf (str) – absolute path
    """
    summarizer_agent = build_summarizer_agent()
    timetable_agent = build_timetable_agent()

    summarizer_task = build_summarizer_task(summarizer_agent, pdf_text)
    timetable_task = build_timetable_task(timetable_agent, schedule_text)

    crew = Crew(
        agents=[summarizer_agent, timetable_agent],
        tasks=[summarizer_task, timetable_task],
    )

    result = crew.kickoff({
        "task": "Summarize this PDF",
        "input": pdf_text,
        "schedule_text": schedule_text,
        "output_dir": "output/",
    })

    summary_text = result.tasks_output[0].raw
    timetable_text = result.tasks_output[1].raw

    summary_pdf_path = save_output(summary_text, "summary.pdf")
    timetable_pdf_path = save_output(timetable_text, "timetable.pdf", table=True)

    return {
        "summary_text": summary_text,
        "timetable_text": timetable_text,
        "summary_pdf": summary_pdf_path,
        "timetable_pdf": timetable_pdf_path,
    }
