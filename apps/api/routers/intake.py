from fastapi import APIRouter

from apps.api.logging_config import logger
from apps.api.schemas.base import IntakeRequest, IntakeResponse
from apps.api.services.store import STORE

router = APIRouter(prefix="/intake", tags=["intake"])


@router.post("/message", response_model=IntakeResponse)
def receive_message(payload: IntakeRequest) -> IntakeResponse:
    record = STORE.create_lead(
        tenant_id=payload.tenant_id,
        canal=payload.canal,
        payload=payload.payload.model_dump(by_alias=True),
    )
    STORE.add_message(record.id, payload.payload.body)
    logger.info("lead.intake", extra={"lead_id": record.id, "tenant_id": record.tenant_id})
    return IntakeResponse(lead_id=record.id)
