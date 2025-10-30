import jsonschema

from apps.api.schemas.base import RouterOutput
from core.guardrails.schemas import ROUTER_OUTPUT_SCHEMA


def test_router_output_schema_validation():
    sample = RouterOutput(
        vertical="consultoria",
        lead_type="programacion",
        confidence=0.84,
        reasoning="Coincidencia",
    ).model_dump()
    jsonschema.validate(sample, ROUTER_OUTPUT_SCHEMA)
