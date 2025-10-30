from datetime import datetime, timezone

from fastapi import APIRouter

from apps.api.schemas.base import MetricSummary

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("/summary", response_model=MetricSummary)
def metrics_summary(tenant_id: str, from_ts: datetime, to_ts: datetime) -> MetricSummary:
    return MetricSummary(
        tenant_id=tenant_id,
        from_ts=from_ts,
        to_ts=to_ts,
        tta_minutes_p50=7.5,
        response_rate=0.42,
        avg_score=0.61,
    )
