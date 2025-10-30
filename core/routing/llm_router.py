from __future__ import annotations

from typing import Any, Dict

from apps.api.schemas.base import RouterOutput


class RouterLLMClient:
    """Cliente stub que simula un router LLM de respaldo."""

    def route(self, payload: Dict[str, Any]) -> RouterOutput:
        """Devuelve una predicción determinista basada en el cuerpo del mensaje."""

        body = payload.get("body", "")
        if "integracion" in body.lower():
            return RouterOutput(
                vertical="consultoria",
                lead_type="programacion",
                confidence=0.74,
                reasoning="Fallback LLM detecta contexto de integraciones",
            )
        return RouterOutput(
            vertical="consultoria",
            lead_type="general",
            confidence=0.51,
            reasoning="Fallback LLM sin evidencia fuerte",
        )


def get_router_client() -> RouterLLMClient:
    """Permite inyectar un cliente alternativo en tests o integraciones reales."""

    return RouterLLMClient()
