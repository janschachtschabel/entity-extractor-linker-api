"""QA endpoint `/qa` – generates question/answer pairs from compendium."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/v1", tags=["qa"])


class QARequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text content for QA generation (supports compendium markdown)")
    num_pairs: int = Field(10, ge=1, le=20)
    max_answer_length: int = Field(250, ge=50, le=1000)


class QAPair(BaseModel):
    question: str
    answer: str


class QAResponse(BaseModel):
    original_text: str
    qa: list[QAPair]


@router.post("/qa", response_model=QAResponse)
async def qa_endpoint(payload: QARequest) -> QAResponse:
    """Generate question-answer pairs from markdown text.

    This endpoint uses OpenAI to generate educational QA pairs from the provided
    markdown content. The number of pairs and maximum answer length can be configured.

    Parameters
    ----------
    payload : QARequest
        Request containing text, num_pairs, and max_answer_length

    Returns
    -------
    QAResponse
        Response containing original text and generated QA pairs

    Raises
    ------
    HTTPException
        400: If text is empty
        503: If OpenAI service is unavailable or misconfigured
        500: If QA generation fails for other reasons
    """
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="text required")

    from ...core import qa as qa_core

    try:
        pairs = qa_core.generate_qa_pairs(payload.text, payload.num_pairs, max_chars=payload.max_answer_length)
        return QAResponse(original_text=payload.text, qa=[QAPair(question=q, answer=a) for q, a in pairs])
    except RuntimeError as e:
        # OpenAI configuration or availability issues
        raise HTTPException(status_code=503, detail=f"QA generation service unavailable: {e!s}")
    except ValueError as e:
        # Invalid or empty OpenAI response
        raise HTTPException(status_code=500, detail=f"QA generation failed: {e!s}")
    except Exception as e:
        # Unexpected errors
        raise HTTPException(status_code=500, detail=f"Unexpected error during QA generation: {e!s}")
