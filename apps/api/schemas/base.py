from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class LeadState(str, Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    WON = "won"
    LOST = "lost"


class IntakePayload(BaseModel):
    subject: Optional[str] = None
    body: str
    from_: str = Field(..., alias="from")
    meta: Dict[str, Any] = {}

    class Config:
        populate_by_name = True


class IntakeRequest(BaseModel):
    tenant_id: str
    canal: str
    payload: IntakePayload


class IntakeResponse(BaseModel):
    lead_id: str
    status: str = "received"


class RouterOutput(BaseModel):
    vertical: str
    lead_type: str
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: Optional[str] = None


class ComposeRequest(BaseModel):
    max_tokens: int = Field(600, ge=128, le=2000)


class AnswerPayload(BaseModel):
    asunto: str
    cuerpo: str
    preguntas_qual: List[str] = Field(default_factory=list, max_items=3)


class Citation(BaseModel):
    uri: str
    snippet: str


class ComposerOutput(BaseModel):
    answer: AnswerPayload
    citations: List[Citation]
    score: float
    categoria: str = Field(pattern="^(caliente|tibio|frio)$")
    siguientes_pasos: List[str]


class SendRequest(BaseModel):
    canal: str
    template_id: str
    params: Dict[str, Any] = {}


class SendResponse(BaseModel):
    status: str = "queued"
    provider_id: Optional[str] = None


class LeadRecord(BaseModel):
    id: str
    tenant_id: str
    vertical: Optional[str] = None
    lead_type: Optional[str] = None
    canal: str
    payload: Dict[str, Any]
    estado: LeadState = LeadState.NEW
    score: Optional[float] = None
    categoria: Optional[str] = None
    owner: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class MetricSummary(BaseModel):
    tenant_id: str
    from_ts: datetime
    to_ts: datetime
    tta_minutes_p50: float
    response_rate: float
    avg_score: float


class ExportResponse(BaseModel):
    format: str
    url: str


class KnowledgeSearchRequest(BaseModel):
    q: str
    scope: str = "tenant"
    tenant_id: str


class KnowledgeItem(BaseModel):
    titulo: str
    uri: str
    metadata: Dict[str, Any] = {}


class KnowledgeSearchResponse(BaseModel):
    items: List[KnowledgeItem]


class RateLimitConfig(BaseModel):
    default_per_minute: int = 20
    followup_per_day: int = 3


class FollowUpTemplate(BaseModel):
    template_id: str
    canal: str
    body: str
    schedule_offset_days: int
