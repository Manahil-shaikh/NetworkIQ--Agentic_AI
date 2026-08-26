from pydantic import BaseModel, Field


class InvestigationRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=3,
        description="Natural language network investigation request.",
    )


class InvestigationResponse(BaseModel):
    cell_id: str | None = None
    region: str | None = None
    response: str