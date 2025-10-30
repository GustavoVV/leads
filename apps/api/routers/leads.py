from datetime import datetime, timezone
from typing import Dict

from fastapi import APIRouter, HTTPException

from apps.api.logging_config import logger
from apps.api.schemas.base import (
    ComposerOutput,
    ComposeRequest,
    ExportResponse,
    LeadRecord,
    RouterOutput,
    SendRequest,
    SendResponse,
)
from apps.api.services.store import STORE
from core.orchestration.workflow import DEFAULT_WORKFLOW

router = APIRouter(prefix="/leads", tags=["leads"])


def _get_lead_or_404(lead_id: str) -> LeadRecord:
    lead = STORE.get_lead(lead_id)
    if lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead


@router.post("/{lead_id}/route", response_model=RouterOutput)
def route_lead(lead_id: str) -> RouterOutput:
    lead = _get_lead_or_404(lead_id)
    payload: Dict[str, str] = lead.payload
    routing = DEFAULT_WORKFLOW.route(payload)
    STORE.update_lead(lead_id, vertical=routing.vertical, lead_type=routing.lead_type)
    logger.info(
        "lead.routed",
        extra={
            "lead_id": lead_id,
            "vertical": routing.vertical,
            "lead_type": routing.lead_type,
            "confidence": routing.confidence,
        },
    )
    return routing


@router.post("/{lead_id}/compose", response_model=ComposerOutput)
def compose_response(lead_id: str, request: ComposeRequest) -> ComposerOutput:  # noqa: ARG001
    lead = _get_lead_or_404(lead_id)
    if not lead.vertical:
        routing = DEFAULT_WORKFLOW.route(lead.payload)
        STORE.update_lead(lead_id, vertical=routing.vertical, lead_type=routing.lead_type)
    else:
        routing = RouterOutput(
            vertical=lead.vertical,
            lead_type=lead.lead_type or "general",
            confidence=0.8,
            reasoning="Cache previa",
        )
    composed = DEFAULT_WORKFLOW.compose(lead.tenant_id, lead_id, lead.payload, routing)
    STORE.update_lead(
        lead_id,
        score=composed.score,
        categoria=composed.categoria,
        updated_at=datetime.now(timezone.utc),
    )
    return composed


@router.post("/{lead_id}/send", response_model=SendResponse)
def send_message(lead_id: str, request: SendRequest) -> SendResponse:
    _ = _get_lead_or_404(lead_id)
    logger.info(
        "lead.send",
        extra={"lead_id": lead_id, "canal": request.canal, "template": request.template_id},
    )
    provider_id = f"{request.canal}-{lead_id}"
    return SendResponse(provider_id=provider_id)


@router.get("/export", response_model=ExportResponse)
def export_leads(format: str = "csv") -> ExportResponse:
    if format not in {"csv", "sheet"}:
        raise HTTPException(status_code=400, detail="Formato no soportado")
    url = f"https://exports.unify-leads/{format}/latest"
    return ExportResponse(format=format, url=url)
