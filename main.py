"""
GitHub Copilot Metrics Summarizer API.

This module provides an API for summarizing GitHub Copilot metrics data,
generating descriptive and inferential analysis using LLM services.
"""

import json
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from src.infrastructure.service.artifical_inteligence.llm.llm_service import llm_service
from src.infrastructure.service.artifical_inteligence.llm.prompt_template import (
    create_summary_prompt,
)
from src.presentation.schemas.schema_ai import CopilotMetricsRequest, SummaryResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle manager for the FastAPI application.

    Parameters
    ----------
    app : FastAPI
        The FastAPI application instance.

    Yields
    ------
    None
        Control is yielded back to the application during its lifetime.

    """
    # Code to run on startup
    llm_service.load_model()
    app.state.llm_service = llm_service
    yield
    app.state.llm_service.unload_model()


app = FastAPI(lifespan=lifespan, title="GitHub Copilot Metrics Summarizer")


@app.post("/summarize")
async def summarize_metrics(request: Request, metrics_data: CopilotMetricsRequest):
    """
    Generate a summary of GitHub Copilot metrics data.

    Parameters
    ----------
    request : Request
        The FastAPI request object.
    metrics_data : CopilotMetricsRequest
        The Copilot metrics data to summarize.

    Returns
    -------
    SummaryResponse
        An object containing the generated summary text.

    Raises
    ------
    HTTPException
        If there's an error during summary generation.

    """
    try:
        # Convert Pydantic model back to dict for JSON string formatting
        data_dict = metrics_data.model_dump()
        json_string = json.dumps(data_dict, indent=2)

        # Construct the prompt
        prompt = create_summary_prompt(json_string)

        # Access the service from app state and generate summary
        service = request.app.state.llm_service
        summary_text = service.generate_summary(prompt)

        return SummaryResponse(summary=summary_text)
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
