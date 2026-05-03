"""
agents/summarizer/agent.py
--------------------------
CrewAI Summarizer Agent and Task definitions.
"""

from crewai import Agent, Task
from core.config import basic_llm


def build_summarizer_agent() -> Agent:
    """Return a configured CrewAI Summarizer Agent."""
    return Agent(
        role="Summarizer Agent",
        goal=(
            "To provide a concise summary of any given document or text, "
            "ensuring clarity, accuracy, and output in a user-friendly PDF format."
        ),
        backstory="\n".join([
            "The agent is designed to assist users in quickly understanding the main points of lengthy documents or articles.",
            "It should distill complex information into easily digestible summaries while maintaining the original context and meaning.",
            "The agent can also summarize weekly thoughts, reflections, and tasks to support productivity.",
            "The agent should generate a PDF file containing the summary and save it to the output directory.",
            "The agent should support multiple languages and be able to summarize content in the user's preferred language.",
            "The agent should handle various document formats, including PDFs, articles, and plain text.",
        ]),
        llm=basic_llm,
        verbose=True,
    )


def build_summarizer_task(agent: Agent, pdf_text: str) -> Task:
    """Return a configured CrewAI Summarizer Task for the given pdf_text."""
    return Task(
        description=f"""
        Summarize the following PDF text: {pdf_text}

        Read through the document carefully and identify the key points, main ideas, and essential information.
        Create a concise summary that captures the essence of the original text while omitting unnecessary details.
        Ensure that the summary is clear, coherent, and easy to understand.
        Generate a PDF file containing the summary and save it to the output directory.
        """,
        expected_output="\n".join([
            "A well-structured summary containing a concise and accurate summary of the provided document in PDF format.",
            "The summary should be saved as a PDF file in the output directory.",
            "The summary should be clear and concise, formatted in short paragraphs or bullet points for easy reading.",
        ]),
        agent=agent,
    )
