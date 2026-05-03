"""
agents/timetable/agent.py
--------------------------
CrewAI Timetable Agent and Task definitions.
"""

from crewai import Agent, Task
from core.config import basic_llm


def build_timetable_agent() -> Agent:
    """Return a configured CrewAI Timetable Agent."""
    return Agent(
        role="Timetable Agent",
        goal=(
            "To create a detailed weekly timetable based on user-provided tasks and priorities, "
            "ensuring optimal time management and productivity."
        ),
        backstory="\n".join([
            "The agent is designed to assist users in organizing their weekly schedule by allocating time slots for various tasks and activities.",
            "It should consider task priorities, deadlines, and estimated durations to create an efficient timetable.",
            "The agent should generate a PDF file containing the timetable and save it to the output directory.",
            "The agent should support multiple languages and be able to create timetables in the user's preferred language.",
            "The agent should handle various input formats, including plain text, lists, and structured data (e.g., JSON).",
        ]),
        llm=basic_llm,
        verbose=True,
    )


def build_timetable_task(agent: Agent, schedule_text: str) -> Task:
    """Return a configured CrewAI Timetable Task for the given schedule_text."""
    return Task(
        description=f"""
        Create a timetable for a whole week based on the following tasks and priorities: {schedule_text}
        Analyze each task and its priority level.
        Distribute the tasks across the week while ensuring an efficient workload balance.
        Include short breaks, rest periods, and buffer time between major tasks.
        Ensure the timetable is clear, easy to read, and organized by day and hour.

        Output MUST be in the following structured format (no extra text):
        Day | Time Slot | Task | Duration | Priority
        Monday | 09:00 - 11:00 | Complete project report | 2 hours | High
        Monday | 11:00 - 12:00 | Team meeting | 1 hour | Medium
        ...
        """,
        expected_output="\n".join([
            "A well-structured weekly timetable in PDF format, saved in the output directory.",
            "The timetable should clearly display each day of the week with assigned time slots for all tasks.",
            "It should include task names, durations, priorities, and any free or break periods.",
            "The final PDF should be saved in the output directory as 'timetable.pdf'.",
            "",
            "A clean, consistent table text with five columns separated by '|':",
            "Day | Time Slot | Task | Duration | Priority.",
            "No explanations or comments.",
        ]),
        agent=agent,
    )
