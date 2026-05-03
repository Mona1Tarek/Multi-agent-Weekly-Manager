"""
agents/email_drafter/schemas.py
--------------------------------
Pydantic schemas for the Email Drafter agent/tool.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class CreateDraftSchema(BaseModel):
    """Input schema for the GmailCreateDraft tool."""

    message: str = Field(..., description="The message body to include in the draft.")
    to: List[str] = Field(..., description="List of recipient email addresses.")
    subject: str = Field(..., description="Subject line of the email.")
    cc: Optional[List[str]] = Field(default=None, description="Optional CC recipients.")
    bcc: Optional[List[str]] = Field(default=None, description="Optional BCC recipients.")


class DraftEmailRequest(BaseModel):
    """FastAPI request body for the /draft-email endpoint."""

    message: str
    to: List[str]
    subject: str
    cc: Optional[List[str]] = None
    bcc: Optional[List[str]] = None
