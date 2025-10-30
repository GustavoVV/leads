ESPECIFICACIÓN DEL PROYECTO PARA CODEX
Proyecto: UNIFY-LEADS (multi-vertical)
Versión: 1.0 (MVP → v1.0)
Owner: @vidalvicentgustavo
Objetivo: Plataforma de orquestación de leads multi-vertical (inmobiliaria, consultoría, gestoría, programación y otros) con intake omnicanal, routing por vertical/lead_type, RAG jerárquico, scoring unificado y follow-ups automatizados. Listo para pilotos y escalable.

1. VISIÓN Y RESULTADOS ESPERADOS
   1.1 Problema
   Los leads entran por múltiples canales y sectores; se cualifican tarde y de forma desigual, se pierden contextos y no hay trazabilidad ni aprendizaje compuesto.

1.2 Solución
Núcleo común + “cápsulas” por vertical (playbooks). Flujo E2E: Intake → Normalización → Clasificación (vertical/lead_type) → Enriquecimiento → RAG jerárquico → Generación/Acción (respuesta/agenda/CRM) → Métricas/Evaluación.

1.3 KPIs (tablero 80/20)
– TTA (time-to-first-answer) < 10 min.
– ≥ 35% tasa de respuesta inicial.
– +35% leads “caliente”.
– Ahorro ≥ 10–15 h/semana/cliente.
– Groundedness RAG ≥ 0.9 en set dorado.
– Coste tokens/lead en rango objetivo (registrado y monitorizado).

2. ALCANCE (MVP → v1)
   Incluye
   – Ingesta por API/email/WhatsApp/web.
   – Router v0 (reglas) + fallback LLM (zero-shot) con salida JSON estricta.
   – Namespaces vectoriales por tenant/vertical/lead y retriever jerárquico con re-rank.
   – Scoring configurable por vertical (pesos y bins).
   – Respuestas y follow-ups D0/D2/D7 con throttling y opt-out.
   – CRM básico (CSV/Sheets) + panel mínimo (TTA, tasa respuesta, score medio).
   – Trazas, logs, versionado de prompts y datasets.
   – Seguridad base (PII masking, validación JSON Schema, rate limiting).
   Excluye (v1+)
   – Integraciones CRM avanzadas (HubSpot/Pipedrive API).
   – Fine-tuning/PEFT y búsqueda híbrida texto+imagen.
   – Canary y rollback automáticos.
   (Se planifican para v2/v3).

3. ARQUITECTURA (80/20, extensible)
   3.1 Stack
   Backend: FastAPI (Python 3.11+)
   Orquestación: LangGraph (sobre LangChain)
   Modelos: OpenAI/HF; opcional local (Ollama/LM Studio)
   Embeddings: SentenceTransformers/HF
   Vectores: Chroma (local) → Pinecone (gestionado)
   UI: Streamlit (MVP)
   Mensajería: SMTP; Twilio WhatsApp (intake/seguimiento)
   Trazas/Eval: LangSmith + RAGAS (v1)
   Infra: HF Spaces (demo) → Docker/EC2 (pre-prod)
   CI/CD: GitHub Actions
   Observabilidad: logs estructurados + métricas básicas

3.2 Diagrama lógico (texto)
Cliente/Canales → API Gateway (FastAPI) → Orquestador (LangGraph) →
[Normalizer] → [Classifier/Router] → [Enricher] → [Retriever RAG jerárquico] → [Generator + Guardrails] → [Actuator (email/WhatsApp/Calendly/CRM)] → [Logger/Telemetry]
↳ Persistencia: Postgres (metadatos), Object store (docs), Vector store (Chroma/Pinecone)

4. MODELO DE DATOS (Postgres + vector store)
   Tablas (campos mínimos):
   tenants(id, nombre, dominio, politicas_pii, created_at)
   verticals(id, slug, playbook_id, created_at)
   lead_types(id, vertical_id, nombre, schema_json, created_at)
   leads(id, tenant_id, vertical_id, lead_type_id, fuente, payload_json, estado, score, categoria, owner, created_at, updated_at)
   interactions(id, lead_id, canal, direction, contenido, metadata, ts)
   knowledge_items(id, tenant_id, vertical_id, lead_type_id, titulo, uri, metadata, created_at)
   indexes(id, store, namespace, scope, embedding_model, created_at)
   playbooks(id, vertical_id, version, config_json, created_at)

Vector namespaces:
tenant/{tenant_id}
tenant/{tenant_id}/vertical/{vertical_slug}
tenant/{tenant_id}/lead/{lead_id}

5. PLAYBOOKS (por vertical; YAML/JSON)
   Estructura (ejemplo abreviado):
   version: "1.1"
   vertical: "consultoria"
   scoring:
   presupuesto: {weight: 0.35, bins: [[0,1500,0.1],[1500,5000,0.6],[5000,1e9,1.0]]}
   urgencia: {weight: 0.25, values: {alta: 1.0, media: 0.6, baja: 0.2}}
   decision_maker: {weight: 0.15, values: {si: 1.0, no: 0.4}}
   encaje_servicio: {weight: 0.25, values: {programacion: 1.0, documentacion: 0.8, otro: 0.5}}
   followups:
   day0: "Gracias {nombre}… Preguntas: {preguntas_qual}"
   day2: "¿Revisamos propuesta?"
   day7: "Cierro hilo salvo que…"
   response_style: {voz: "profesional, directa", firma: "Equipo Val-IA"}
   required_fields: [email, problema, plazo]
   policies: {pii: true, disclaimers: ["…"]}

6. API (REST, FastAPI)
   Base path: /api/v1

6.1 Intake
POST /intake/message
Body:
{
"tenant_id":"t_123",
"canal":"whatsapp|email|web|api",
"payload": { "subject":"…", "body":"…", "from":"…", "meta":{}}
}
Resp: { "lead_id":"L123", "status":"received" }

6.2 Clasificación (si intake no la dispara)
POST /leads/{lead_id}/route
Resp (estándar):
{
"vertical":"consultoria",
"lead_type":"programacion",
"confidence":0.84,
"reasoning":"…"
}

6.3 RAG + Respuesta (preview)
POST /leads/{lead_id}/compose
Body: { "max_tokens": 600 }
Resp:
{
"answer":{ "asunto":"…", "cuerpo":"…", "preguntas_qual":["…"] },
"citations":[{"uri":"…","snippet":"…"}],
"score":0.78, "categoria":"caliente", "siguientes_pasos":["…"]
}

6.4 Acción (enviar)
POST /leads/{lead_id}/send
Body: { "canal":"email|whatsapp", "template_id":"day0", "params":{…} }
Resp: { "status":"queued", "provider_id":"…" }

6.5 CRM básico
GET /leads/export?format=csv|sheet
POST /crm/sync (v1: Sheets; v2: HubSpot/Pipedrive)

6.6 Gestión de conocimiento
POST /knowledge/index (cargar y reindexar)
GET /knowledge/search?q=…&scope=tenant|vertical|lead

6.7 Telemetría básica
GET /metrics/summary?tenant_id=…&from=…&to=…

7. CONTRATOS (JSON Schema)
   7.1 RouterOutput
   {
   "type":"object",
   "required":["vertical","lead_type","confidence"],
   "properties":{
   "vertical":{"type":"string"},
   "lead_type":{"type":"string"},
   "confidence":{"type":"number","minimum":0,"maximum":1},
   "reasoning":{"type":"string"}
   }
   }

7.2 ComposerOutput
{
"type":"object",
"required":["answer","citations","score","categoria","siguientes_pasos"],
"properties":{
"answer":{
"type":"object",
"required":["asunto","cuerpo"],
"properties":{
"asunto":{"type":"string"},
"cuerpo":{"type":"string"},
"preguntas_qual":{"type":"array","items":{"type":"string"}, "maxItems":3}
}
},
"citations":{"type":"array","items":{"type":"object"}},
"score":{"type":"number"},
"categoria":{"type":"string","enum":["caliente","tibio","frio"]},
"siguientes_pasos":{"type":"array","items":{"type":"string"}}
}
}

8. WORKFLOWS (LangGraph, nodos)
   Intake → Normalizer → Router → Enricher → Retriever (RAG jerárquico) → Generator (function calling habilitado) → Guardrails (JSON Schema + PII) → Actuator → Logger.
   RAG jerárquico (k por defecto): vertical(k=6) + lead(k=4, si existe) + tenant(k=2) → re-rank → citas.

9. HEURÍSTICAS Y REGLAS
   – Routing v0 (barato): keywords por canal + slugs de landing.
   – Routing v1 (robusto): LLM zero-shot con schema RouterOutput y temperatura baja.
   – Scoring: suma ponderada de features normalizadas (pesos por vertical desde playbook).
   – Throttling: máximo N mensajes/día/lead; respeto de opt-out.
   – Length budget: respuestas < 120 palabras por defecto (ajustable por vertical).

10. EVALUACIÓN Y CALIDAD
    – Conjunto dorado (golden set) para: routing, groundedness, formato JSON.
    – RAGAS + LangSmith para groundedness/recall.
    – Smoke tests automáticos:
    *test_router_json*: valida schema RouterOutput.
    *test_composer_schema*: valida ComposerOutput.
    *test_rag_groundedness*: score ≥ umbral.
    *test_rate_limits*: respeta límites.
    – Métricas: TTA, tasa respuesta, groundedness, coste tokens, errores de routing/formato.

11. SEGURIDAD Y CUMPLIMIENTO
    – PII masking en logs; cifrado en reposo (DB/objetos).
    – Prompt-injection: allow-list de tools, sanitización de URLs, verificador de citas.
    – Validación obligatoria contra JSON Schema antes de actuar.
    – Rate limiting por IP/cuenta/canal.
    – Registro de consentimiento y opt-out.
    – Auditoría básica (quién/qué/cuándo).

12. DEPLOY, CI/CD Y ENTORNOS
    Entornos: dev (local), demo (HF Spaces), pre-prod (Docker/EC2).
    CI/CD (GitHub Actions):
    – Lint/Format (ruff/black).
    – Tests unitarios + smoke tests (pytest).
    – Build Docker + push (pre-prod tag).
    – Deploy automatizado (pre-prod) con variables seguras.
    Observabilidad: logs estructurados (JSON), métricas agregadas (endpoint /metrics).
    Backups: base de datos diaria; vector store semanal (snapshot).

13. VARIABLES DE ENTORNO (ejemplo)
    APP_ENV, SECRET_KEY
    DB_URL (postgres)
    VECTOR_STORE (chroma|pinecone), PINECONE_API_KEY, PINECONE_ENV
    LLM_PROVIDER (openai|hf|ollama), OPENAI_API_KEY, HF_TOKEN
    EMBEDDING_MODEL (ej. sentence-transformers/all-MiniLM-L6-v2)
    SMTP_HOST/PORT/USER/PASS
    TWILIO_SID/TOKEN/WHATSAPP_FROM
    LANGSMITH_API_KEY
    RATE_LIMITS_JSON

14. ESTRUCTURA DE REPOSITORIO
    unify-leads/
    apps/api/ (FastAPI, routers, models, schemas)
    apps/ui/ (Streamlit)
    core/orchestration/ (LangGraph workflows)
    core/routing/ (rules, llm_router.py, schemas)
    core/rag/ (indexing, retrievers, rerank)
    core/guardrails/ (schemas, pii, validators)
    data/ (fixtures, samples)
    playbooks/ (inmobiliaria.yaml, consultoria.yaml, gestoria.yaml)
    infra/docker/ (Dockerfile, compose, deploy)
    sdk/unify_leads/ (cliente Python, ejemplos)
    tests/ (unit, e2e, smoke)
    README.md / OPERATIONS.md / SECURITY.md / ROADMAP.md

15. ROADMAP TÉCNICO (resumen)
    MVP (Semanas 1–2): núcleo multi-vertical, router v0 + fallback LLM, RAG jerárquico, UI mínima, playbooks inmobiliaria/consultoría.
    v1 (Semanas 3–6): follow-ups + throttling, panel simple, export CRM, golden set + RAGAS.
    v2 (Semanas 7–10): agentes (Autogen/CrewAI), evaluación continua, ajuste scoring con datos.
    v3 (Semanas 11–16): PEFT/QLoRA opcional, guardrails avanzados, Docker+CI/CD robusto, model registry, canary/rollback, integraciones CRM.

16. CRITERIOS DE ACEPTACIÓN (MVP)
    – Ingesta omnicanal funcional (POST /intake/message y WhatsApp webhook).
    – Routing produce JSON válido con confianza ≥ 0.7 en set dorado.
    – RAG devuelve respuesta con ≥ 0.9 groundedness (RAGAS) en golden set acotado.
    – Envío de day0 por email/WhatsApp con registro en interactions.
    – Export CSV/Sheets operativa.
    – Panel básico (TTA, tasa respuesta, score medio) accesible.
    – Logs, versionado de prompts y control de errores (sin crashes) bajo carga de prueba.

17. RIESGOS Y MITIGACIONES
    – Drift en prompts/clasificación → versionado + tests smoke + golden set semanal.
    – Costes de inferencia → caching, embeddings eficientes, límites por lead.
    – Datos sensibles → PII masking y cifrado, acceso por rol.
    – Dependencia de proveedor LLM → capa de abstracción (OpenAI/HF/Ollama).
    – Alucinaciones → RAG con citas obligatorias + validador de groundedness antes de actuar.

18. ALINEACIÓN CON FORMACIÓN (Roadmap AI Engineer)
    – Fase 1: APIs, prompts, function calling, deploy rápido, WhatsApp intake.
    – Fase 2: RAG, sub-question engine, agentes Autogen/CrewAI, evaluación RAGAS/LangSmith, logging/monitoring.
    – Fase 3: PEFT/QLoRA por vertical, model registry, tests automáticos, búsqueda híbrida, red teaming.

19. ANEXOS (plantillas)
    19.1 Prompt de respuesta (consultoría)
    [Rol] Asistente comercial técnico de {tenant}.
    [Objetivo] Responder en <120 palabras, confirmar encaje y proponer siguiente paso.
    [Contexto] Usa SOLO evidencia citada (RAG).
    [Salida] JSON {asunto, cuerpo, preguntas_qual[<=3]}.
    [Estilo] Profesional, directo, claro.

19.2 Pseudocódigo de scoring
score = w_pres*presupuesto_norm + w_urg*urg + w_dm*es_decisor + w_fit*encaje
categoria = (score≥0.75 ? "caliente" : score≥0.45 ? "tibio" : "frio")

19.3 Ejemplo de salida Router
{ "vertical":"consultoria", "lead_type":"programacion", "confidence":0.84, "reasoning":"Menciona integración Python y presupuesto" }

—
Con esta especificación, Codex puede generar el esqueleto del repositorio, los contratos JSON, los endpoints FastAPI, los flujos LangGraph, los esquemas de datos y la UI de Streamlit, además del arnés de tests y la canalización CI/CD mínima.
