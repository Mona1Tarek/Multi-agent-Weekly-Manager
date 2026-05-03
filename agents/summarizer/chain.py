"""
agents/summarizer/chain.py
--------------------------
LangChain-based summarizer using create_stuff_documents_chain.
Faster than the CrewAI agent for straightforward HTTP requests.
"""

from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from core.config import get_langchain_llm
from core.pdf_utils import save_output


def run_summarizer_chain(pdf_text: str, save_pdf: bool = False) -> str:
    """
    Summarize the provided text using LangChain's stuff-documents chain.

    Args:
        pdf_text:  The text extracted from a PDF.
        save_pdf:  If True, also saves the summary to output/langchain_summary.pdf.

    Returns:
        Summary as a plain string.
    """
    llm = get_langchain_llm()
    document = Document(page_content=pdf_text, metadata={"source": "uploaded.pdf"})
    prompt = ChatPromptTemplate.from_template("Summarize this content: {context}")
    chain = create_stuff_documents_chain(llm, prompt)
    result: str = chain.invoke({"context": [document]})

    if save_pdf:
        save_output(result, "langchain_summary.pdf")

    return result
