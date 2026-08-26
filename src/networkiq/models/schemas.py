from pydantic import BaseModel, Field


class RootCauseAnalysis(BaseModel):
    """Structured telecom root-cause analysis."""

    primary_cause: str = Field(
        description="Most likely cause of the observed network issue."
    )

    confidence: str = Field(
        description="Confidence level: low, medium, or high."
    )

    evidence: list[str] = Field(
        description="Observed evidence supporting the hypothesis."
    )

    alternative_causes: list[str] = Field(
        default_factory=list,
        description="Other plausible causes."
    )