# Multi-agent Weekly Manager

## Overview
The Multi-agent Weekly Manager is an AI-powered system designed to assist with weekly management tasks using multiple specialized agents. The current implementation includes a Summarizer Agent that processes PDF documents to generate concise summaries in PDF format, and a Timetable Agent that creates detailed weekly timetables based on user-provided tasks and priorities. The system is built using CrewAI for task orchestration and leverages powerful language models such as Groq's Llama and Ollama.

## Features
- **Summarizer Agent**: Summarizes lengthy PDF documents into clear, concise summaries saved as PDF files.
- **Timetable Agent**: Creates detailed weekly timetables based on user-provided tasks and priorities, saved as PDF files.
- Planned Agents:
  - Email Drafting Agent: Drafts emails based on summarized content.
  - Calendar Agent: Manages and books meetings.
  - Reminder Agent: Sends reminders for upcoming tasks and events.
  - Reporting Agent: Generates weekly or daily summary reports.

## Installation

### Prerequisites
- Python 3.8 or higher
- API keys for Groq and AgentOps (stored in a `.env` file)

### Dependencies
Install required Python packages:
```bash
pip install -r requirements.txt
```
or manually:
```bash
pip install crewai python-dotenv fpdf2 PyPDF2 agentops langchain langchain-core langchain-community langchain-groq
```

### Environment Setup
Create a `.env` file in the project root with the following keys:
```
GROQ_API_KEY=your_groq_api_key_here
AGENTOPS_API_KEY=your_agentops_api_key_here
```

## Usage
1. Place the PDF documents you want to summarize in the `input/` directory.
2. Modify the `schedule_text` variable in `main.ipynb` to specify your tasks and priorities for the timetable (e.g., "- Task 1: Complete project report (High Priority, 2 hours)").
3. Run the `main.ipynb` notebook to execute the summarization and timetable agents.
4. The summary PDF will be saved in the `output/` directory as `summary.pdf`.
5. The timetable PDF will be saved in the `output/` directory as `timetable.pdf`.

## Project Structure
- `main.ipynb`: Main notebook containing the agent setup and execution code.
- `input/`: Directory for input PDF files.
- `output/`: Directory where summary PDFs are saved.

## Contributing
Contributions are welcome! Please open issues or submit pull requests for improvements or new features.

## License
This project currently does not have a license specified.
