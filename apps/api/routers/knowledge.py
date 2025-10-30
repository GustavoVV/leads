from fastapi import APIRouter

from apps.api.schemas.base import KnowledgeSearchResponse

router = APIRouter(prefix="/knowledge", tags=["knowledge"])


@router.get("/search", response_model=KnowledgeSearchResponse)
def search_knowledge(q: str, scope: str, tenant_id: str) -> KnowledgeSearchResponse:
    """Devuelve resultados simulados para probar la interfaz de búsqueda."""

    dummy_items = [
        {
            "titulo": f"Respuesta sobre {q}",
            "uri": f"https://docs.unify/{tenant_id}/{scope}/faq#{q}",
            "metadata": {"scope": scope},
        }
    ]
    return KnowledgeSearchResponse(items=dummy_items)
