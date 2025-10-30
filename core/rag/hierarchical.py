from __future__ import annotations

from typing import Dict, List

from apps.api.schemas.base import Citation


class HierarchicalRetriever:
    """Retriever determinista con jerarquía tenant → vertical → lead."""

    def retrieve(self, tenant_id: str, vertical: str | None, lead_id: str | None) -> List[Citation]:
        """Genera citas simuladas para explicar la respuesta del modelo."""

        citations: List[Citation] = []
        if vertical:
            citations.append(
                Citation(
                    uri=f"s3://knowledge/{tenant_id}/{vertical}/playbook.pdf",
                    snippet=f"Resumen del playbook para {vertical}",
                )
            )
        citations.append(
            Citation(
                uri=f"s3://knowledge/{tenant_id}/faq.md",
                snippet="Políticas generales del tenant",
            )
        )
        if lead_id:
            citations.append(
                Citation(
                    uri=f"crm://leads/{lead_id}",
                    snippet="Historial previo del lead",
                )
            )
        return citations


DEFAULT_RETRIEVER = HierarchicalRetriever()
