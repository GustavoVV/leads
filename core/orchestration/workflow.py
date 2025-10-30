from __future__ import annotations

from typing import Dict

from apps.api.schemas.base import ComposerOutput, RouterOutput
from core.orchestration.scoring import DEFAULT_SCORER
from core.rag.hierarchical import DEFAULT_RETRIEVER
from core.routing.llm_router import get_router_client
from core.routing.rules import route_by_keywords


class LeadWorkflow:
    """Encapsula la orquestación mínima Intake → Routing → RAG → Generación."""

    def __init__(self) -> None:
        self.router_client = get_router_client()
        self.retriever = DEFAULT_RETRIEVER
        self.scorer = DEFAULT_SCORER

    def route(self, payload: Dict[str, str]) -> RouterOutput:
        text = f"{payload.get('subject', '')} {payload.get('body', '')}".strip()
        vertical, lead_type, confidence, reasoning = route_by_keywords(text)
        if confidence < 0.7:
            fallback = self.router_client.route(payload)
            if fallback.confidence > confidence:
                return fallback
        return RouterOutput(
            vertical=vertical,
            lead_type=lead_type,
            confidence=confidence,
            reasoning=reasoning,
        )

    def compose(self, tenant_id: str, lead_id: str, payload: Dict[str, str], routing: RouterOutput) -> ComposerOutput:
        citations = self.retriever.retrieve(tenant_id, routing.vertical, lead_id)
        features = {
            "presupuesto": payload.get("meta", {}).get("presupuesto", 0),
            "urgencia": payload.get("meta", {}).get("urgencia", "media"),
            "decision_maker": payload.get("meta", {}).get("decision_maker", "no"),
            "encaje_servicio": routing.lead_type,
        }
        score, categoria = self.scorer.score(features)
        body = payload.get("body", "Gracias por contactar con UNIFY-LEADS.")
        answer = {
            "asunto": f"Seguimiento {routing.vertical}",
            "cuerpo": body[:120],
            "preguntas_qual": ["¿Cuál es el plazo deseado?"],
        }
        siguientes_pasos = ["Agendar llamada de descubrimiento", "Registrar en CRM"]
        return ComposerOutput(
            answer=answer,
            citations=citations,
            score=score,
            categoria=categoria,
            siguientes_pasos=siguientes_pasos,
        )


DEFAULT_WORKFLOW = LeadWorkflow()
