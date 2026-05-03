"""
api/routes/email.py
--------------------
POST /email/draft  — Create a Gmail draft email.

Requires token.json to exist (run the OAuth flow from main.ipynb first).
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from agents.email_drafter.schemas import DraftEmailRequest
from agents.email_drafter.agent import create_draft

router = APIRouter()


@router.post(
    "/draft",
    summary="Create a Gmail draft email",
    response_description="Confirmation with the created draft ID",
)
async def draft_email(body: DraftEmailRequest):
    """
    Create a Gmail draft using the provided fields.

    **Prerequisites:** `token.json` must exist in the project root.
    Run the Gmail OAuth flow from `main.ipynb` if it doesn't exist.

    - **message**: Email body text.
    - **to**: List of recipient addresses.
    - **subject**: Email subject.
    - **cc** / **bcc**: Optional CC and BCC recipients.
    """
    try:
        result = create_draft(
            message=body.message,
            to=body.to,
            subject=body.subject,
            cc=body.cc,
            bcc=body.bcc,
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    return JSONResponse(content={"result": result})
