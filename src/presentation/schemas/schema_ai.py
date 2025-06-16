from pydantic import BaseModel
from typing import Dict, Any


class CopilotMetricsRequest(BaseModel):
    """
    Defines the structure for the incoming Copilot metrics data.
    Using a generic Dict allows for flexibility while still validating
    that the input is a valid JSON object.
    """

    metrics_date: str
    total_suggestions: int
    total_acceptances: int
    lines_of_code_suggested: int
    lines_of_code_accepted: int
    activate_user_count: int
    ides: Dict[str, Any]
    languages: Dict[str, Any]
    global_acceptance_rate: float
    line_acceptance_rate: float
    created_at: str


class SummaryResponse(BaseModel):
    """
    Defines the structure for the API's response.
    """

    summary: str
