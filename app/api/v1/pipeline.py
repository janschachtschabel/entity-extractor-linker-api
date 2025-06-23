"""Orchestrator endpoint that chains Linker → Compendium → QA in one call."""

from __future__ import annotations

from typing import Literal

from fastapi import APIRouter, HTTPException
import httpx
from pydantic import BaseModel, Field

router = APIRouter(prefix="/v1", tags=["pipeline"])


class LinkerConfig(BaseModel):
    """Configuration for the linker step."""

    MODE: Literal["extract", "generate", "infer"] = "generate"
    MAX_ENTITIES: int = Field(10, ge=1, le=100)
    ALLOWED_ENTITY_TYPES: str | list[str] | Literal["auto"] = "auto"
    EDUCATIONAL_MODE: bool = False
    LANGUAGE: Literal["de", "en"] = "de"


class CompendiumConfig(BaseModel):
    """Configuration for the compendium step."""

    length: int = Field(6000, ge=1000, le=20000)
    enable_citations: bool = True
    educational_mode: bool = True
    language: Literal["de", "en"] = "de"


class QAConfig(BaseModel):
    """Configuration for the QA step."""

    num_pairs: int = Field(10, ge=1, le=20)
    max_answer_length: int = Field(250, ge=50, le=1000)


class PipelineConfig(BaseModel):
    """Combined configuration for all pipeline steps."""

    linker: LinkerConfig = Field(default_factory=LinkerConfig)
    compendium: CompendiumConfig = Field(default_factory=CompendiumConfig)
    qa: QAConfig = Field(default_factory=QAConfig)


class PipelineRequest(BaseModel):
    """Request for the complete pipeline."""

    text: str = Field(..., min_length=1, description="Input text to process through the complete pipeline")
    config: PipelineConfig = Field(default_factory=PipelineConfig)


class PipelineResponse(BaseModel):
    """Response containing outputs from all pipeline steps."""

    original_text: str
    linker_output: dict
    compendium_output: dict
    qa_output: dict
    pipeline_statistics: dict


@router.post("/pipeline", response_model=PipelineResponse)
async def pipeline_endpoint(payload: PipelineRequest) -> PipelineResponse:
    """Run complete pipeline: Linker → Compendium → QA.

    This orchestrator endpoint chains all three main endpoints:
    1. **Linker**: Extracts/generates entities and links them to Wikipedia
    2. **Compendium**: Generates educational markdown content from linker output
    3. **QA**: Creates question-answer pairs from the compendium

    ## Pipeline Flow:
    ```
    Input Text → Linker → Compendium → QA → Complete Output
    ```

    ## Configuration:
    - **Linker**: Entity extraction/generation settings
    - **Compendium**: Content generation and citation settings
    - **QA**: Question-answer pair generation settings

    ## Default Settings:
    - Linker mode: "generate" (creates comprehensive entity coverage)
    - Educational mode: enabled for both linker and compendium
    - Citations: enabled in compendium
    - Language: German (de)
    """
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="text is required")

    pipeline_stats = {"total_steps": 3, "completed_steps": 0, "processing_times": {}, "errors": []}

    try:
        # Step 1: Linker
        import time

        start_time = time.time()

        async with httpx.AsyncClient() as client:
            linker_request = {
                "text": payload.text,
                "config": {
                    "MODE": payload.config.linker.MODE,
                    "MAX_ENTITIES": payload.config.linker.MAX_ENTITIES,
                    "ALLOWED_ENTITY_TYPES": payload.config.linker.ALLOWED_ENTITY_TYPES,
                    "EDUCATIONAL_MODE": payload.config.linker.EDUCATIONAL_MODE,
                    "LANGUAGE": payload.config.linker.LANGUAGE,
                },
            }

            linker_response = await client.post(
                "http://localhost:8000/api/v1/linker", json=linker_request, timeout=60.0
            )

            if linker_response.status_code != 200:
                raise HTTPException(status_code=500, detail=f"Linker step failed: {linker_response.text}")

            linker_output = linker_response.json()
            pipeline_stats["processing_times"]["linker"] = time.time() - start_time
            pipeline_stats["completed_steps"] = 1

            # Step 2: Compendium
            start_time = time.time()

            compendium_request = {
                "input_type": "linker_output",
                "linker_data": linker_output,
                "config": {
                    "length": payload.config.compendium.length,
                    "enable_citations": payload.config.compendium.enable_citations,
                    "educational_mode": payload.config.compendium.educational_mode,
                    "language": payload.config.compendium.language,
                },
            }

            compendium_response = await client.post(
                "http://localhost:8000/api/v1/compendium", json=compendium_request, timeout=120.0
            )

            if compendium_response.status_code != 200:
                raise HTTPException(status_code=500, detail=f"Compendium step failed: {compendium_response.text}")

            compendium_output = compendium_response.json()
            pipeline_stats["processing_times"]["compendium"] = time.time() - start_time
            pipeline_stats["completed_steps"] = 2

            # Step 3: QA
            start_time = time.time()

            qa_request = {
                "text": compendium_output["markdown"],
                "num_pairs": payload.config.qa.num_pairs,
                "max_answer_length": payload.config.qa.max_answer_length,
            }

            qa_response = await client.post("http://localhost:8000/api/v1/qa", json=qa_request, timeout=60.0)

            if qa_response.status_code != 200:
                raise HTTPException(status_code=500, detail=f"QA step failed: {qa_response.text}")

            qa_output = qa_response.json()
            pipeline_stats["processing_times"]["qa"] = time.time() - start_time
            pipeline_stats["completed_steps"] = 3

            # Calculate total processing time
            pipeline_stats["total_processing_time"] = sum(pipeline_stats["processing_times"].values())

            return PipelineResponse(
                original_text=payload.text,
                linker_output=linker_output,
                compendium_output=compendium_output,
                qa_output=qa_output,
                pipeline_statistics=pipeline_stats,
            )

    except httpx.RequestError as e:
        pipeline_stats["errors"].append(f"Network error: {e!s}")
        raise HTTPException(status_code=503, detail=f"Pipeline communication error: {e!s}")
    except Exception as e:
        pipeline_stats["errors"].append(f"Unexpected error: {e!s}")
        raise HTTPException(status_code=500, detail=f"Pipeline execution failed: {e!s}")
