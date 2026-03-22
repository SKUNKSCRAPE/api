from datetime import datetime
from typing import Any

from pydantic import AnyHttpUrl, BaseModel, ConfigDict, Field


class JobOptions(BaseModel):
    max_pages: int | None = Field(default=5, ge=1, le=1000)
    depth: int | None = Field(default=1, ge=0, le=10)
    webhook_url: AnyHttpUrl | None = None
    source_hint: str | None = None


class JobCreate(BaseModel):
    job_type: str = Field(default="scrape", examples=["scrape", "enrich", "discover"])
    target: AnyHttpUrl
    options: JobOptions | None = None


class JobDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    owner_id: str
    job_type: str
    target: str
    status: str
    error: str | None = None
    created_at: datetime
    started_at: datetime | None = None
    completed_at: datetime | None = None
    updated_at: datetime


class JobResult(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    owner_id: str
    job_type: str
    target: str
    status: str
    error: str | None = None
    result_json: str | None = None
    created_at: datetime
    started_at: datetime | None = None
    completed_at: datetime | None = None
    updated_at: datetime
