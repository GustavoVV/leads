# UNIFY-LEADS

Plataforma mínima de orquestación de leads multi-vertical diseñada para probar el
flujo _intake → routing → RAG → generación → seguimiento_ con componentes
sustituibles. El objetivo del repositorio es servir como base de referencia para
experimentos rápidos y pilotos controlados.

## Características principales

- **API unificada (FastAPI)** para intake de mensajes, enrutado, composición de
  respuestas, envío simulado y exportaciones básicas.
- **Store en memoria** (`apps.api.services.store.InMemoryStore`) que mantiene el
  estado de los leads y sus interacciones durante la ejecución del proceso.
- **Motor de routing híbrido** con reglas por palabra clave y _fallback_ a un
  cliente LLM (`core.routing`), expuesto mediante el endpoint
  `/api/v1/leads/{lead_id}/route`.
- **RAG jerárquico determinista** (`core.rag.hierarchical.HierarchicalRetriever`)
  que devuelve citas simuladas en diferentes niveles (tenant, vertical, lead).
- **Scoring configurable** (`core.orchestration.scoring.LeadScorer`) con bins y
  pesos por atributo para clasificar leads en caliente/tibio/frío.
- **Trazabilidad básica** a través de logs estructurados y dependencias mínimas
  para extender la lógica a proveedores reales (OpenAI, Twilio, CRMs, etc.).

## Flujo de extremo a extremo

1. `POST /api/v1/intake/message` registra un nuevo lead y almacena el mensaje
   recibido.
2. `POST /api/v1/leads/{lead_id}/route` ejecuta las reglas locales y, si es
   necesario, consulta el _fallback_ LLM para determinar vertical y tipo de
   lead.
3. `POST /api/v1/leads/{lead_id}/compose` calcula el _score_, determina la
   categoría y construye la respuesta utilizando el retriever jerárquico.
4. `POST /api/v1/leads/{lead_id}/send` simula el envío de la comunicación y
   devuelve un identificador de proveedor.
5. `GET /api/v1/leads/export` devuelve una URL ficticia para exportar los leads
   en CSV o Google Sheets.

## Arquitectura lógica

```
Cliente/Canales  →  FastAPI (apps.api.main)  →  LeadWorkflow (core.orchestration)
                        ↓                          ↓
                    InMemoryStore              Router (reglas + LLM)
                        ↓                          ↓
                    Logs estructurados       Retriever jerárquico  →  Scoring
```

Cada componente está diseñado para reemplazarse fácilmente por implementaciones
contra bases de datos, proveedores de mensajería o APIs externas.

## Estructura del repositorio

- `apps/api/main.py`: punto de entrada FastAPI y configuración de routers.
- `apps/api/routers/`: endpoints de intake, leads, conocimiento y métricas.
- `apps/api/schemas/`: contratos pydantic utilizados por la API.
- `apps/api/services/store.py`: almacenamiento en memoria de leads y mensajes.
- `core/orchestration/`: _workflow_ y lógica de _scoring_.
- `core/routing/`: reglas por palabra clave y _fallback_ LLM.
- `core/rag/`: retriever jerárquico para componer respuestas con citas.

## Puesta en marcha local

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
uvicorn apps.api.main:app --reload
```

La API quedará disponible en `http://localhost:8000` e incluye documentación
interactiva en `/docs` y `/redoc`.

## Pruebas

```bash
pytest
```

Las pruebas cubren los flujos principales de intake, routing y composición. Se
recomienda ejecutarlas antes de publicar cambios.

## Próximos pasos sugeridos

- Sustituir el _store_ en memoria por una base de datos relacional o vectorial.
- Integrar proveedores reales para el _fallback_ LLM y canales de salida.
- Añadir autenticación multi-tenant y límites de uso por canal.
- Automatizar métricas de TTA, tasa de respuesta y _groundedness_.
