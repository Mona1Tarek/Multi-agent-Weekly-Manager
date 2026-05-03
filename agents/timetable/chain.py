"""
agents/timetable/chain.py
--------------------------
LangChain-based timetable generator using a plain prompt chain.
"""

from langchain_core.prompts import ChatPromptTemplate
from core.config import get_langchain_llm
from core.pdf_utils import save_output


_TIMETABLE_PROMPT = """\
Make a timetable for a whole week for the following tasks: {schedule_text}

Output MUST be in the following structured format (no extra text):
Day | Time Slot | Task | Duration | Priority
Example:
Monday | 09:00 - 11:00 | Complete project report | 2 hours | High
Monday | 11:00 - 12:00 | Team meeting | 1 hour | Medium
"""


def run_timetable_chain(schedule_text: str, save_pdf: bool = False) -> str:
    """
    Generate a weekly timetable from a plain-text task list using LangChain.

    Args:
        schedule_text: Plain-text task list (e.g. "- Task 1: ... (High, 2h)").
        save_pdf:      If True, also saves the result to output/langchain_timetable.pdf.

    Returns:
        Pipe-delimited timetable string.
    """
    llm = get_langchain_llm()
    prompt = ChatPromptTemplate.from_template(_TIMETABLE_PROMPT)
    chain: RunnableSequence = prompt | llm

    result = chain.invoke({"schedule_text": schedule_text})
    # chain returns an AIMessage; extract content
    text: str = result.content if hasattr(result, "content") else str(result)

    if save_pdf:
        save_output(text, "langchain_timetable.pdf", table=True)

    return text
