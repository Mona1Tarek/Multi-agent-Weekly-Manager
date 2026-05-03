"""
agents/email_drafter/agent.py
------------------------------
Gmail draft creation tool, extracted from main.ipynb.
Uses Google's Gmail API with OAuth2 credentials stored in token.json.
"""

import base64
import os
from email.message import EmailMessage
from typing import List, Optional, Type

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_google_community.gmail.base import GmailBaseTool
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

from agents.email_drafter.schemas import CreateDraftSchema

# Path to the OAuth token relative to project root
_TOKEN_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "token.json")
_GMAIL_SCOPES = ["https://www.googleapis.com/auth/gmail.compose"]


def build_gmail_service():
    """
    Build and return an authenticated Gmail API service object.
    Requires token.json to exist (generated via the OAuth flow in main.ipynb).

    Raises:
        FileNotFoundError: If token.json is missing.
    """
    if not os.path.exists(_TOKEN_PATH):
        raise FileNotFoundError(
            f"token.json not found at {_TOKEN_PATH}. "
            "Please run the Gmail OAuth flow using the Google Auth library to generate token.json."
        )
    creds = Credentials.from_authorized_user_file(_TOKEN_PATH, _GMAIL_SCOPES)
    return build("gmail", "v1", credentials=creds)


class GmailCreateDraft(GmailBaseTool):
    """LangChain tool that creates a Gmail draft email."""

    name: str = "create_gmail_draft"
    description: str = "Use this tool to create a draft email with the provided message fields."
    args_schema: Type[CreateDraftSchema] = CreateDraftSchema

    def _prepare_draft_message(
        self,
        message: str,
        to: List[str],
        subject: str,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
    ) -> dict:
        draft_message = EmailMessage()
        draft_message.set_content(message)
        draft_message["To"] = ", ".join(to)
        draft_message["Subject"] = subject
        if cc:
            draft_message["Cc"] = ", ".join(cc)
        if bcc:
            draft_message["Bcc"] = ", ".join(bcc)
        encoded = base64.urlsafe_b64encode(draft_message.as_bytes()).decode()
        return {"message": {"raw": encoded}}

    def _run(
        self,
        message: str,
        to: List[str],
        subject: str,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        try:
            body = self._prepare_draft_message(message, to, subject, cc, bcc)
            draft = (
                self.api_resource.users()
                .drafts()
                .create(userId="me", body=body)
                .execute()
            )
            return f"Draft created. Draft Id: {draft['id']}"
        except Exception as exc:
            raise Exception(f"An error occurred while creating the draft: {exc}") from exc


def create_draft(
    message: str,
    to: List[str],
    subject: str,
    cc: Optional[List[str]] = None,
    bcc: Optional[List[str]] = None,
) -> str:
    """
    Convenience function: build a Gmail service and create a draft.

    Returns:
        Confirmation string with the draft ID.
    """
    service = build_gmail_service()
    tool = GmailCreateDraft(api_resource=service)
    return tool.run({"message": message, "to": to, "subject": subject, "cc": cc, "bcc": bcc})
