# Roadmap Técnico UNIFY-LEADS

## MVP (Semanas 1-2)
- Generar esqueleto API FastAPI y flujos LangGraph básicos.
- Configurar ingesta omnicanal con intake API + stub WhatsApp.
- Implementar router v0 basado en reglas y fallback LLM.
- Configurar RAG jerárquico con Chroma local y namespaces por tenant.
- Crear UI Streamlit mínima con panel TTA/tasa respuesta/score medio.
- Preparar playbooks para inmobiliaria y consultoría.

## v1 (Semanas 3-6)
- Automatizar follow-ups D0/D2/D7 con throttling y opt-out.
- Exportar leads a CSV/Google Sheets desde API y SDK.
- Añadir golden set + RAGAS en pipeline CI.
- Integrar LangSmith para trazas y evaluación continua.
- Completar panel con filtros por vertical y dueño.

## v2 (Semanas 7-10)
- Incorporar agentes de colaboración (Autogen/CrewAI) para enriquecimiento.
- Ajustar scoring dinámico con datos históricos.
- Añadir evaluación continua y dashboards de groundedness.
- Integrar Pinecone administrado y caching de embeddings.

## v3 (Semanas 11-16)
- Implementar PEFT/QLoRA por vertical con despliegue controlado.
- Introducir guardrails avanzados (verificación factual, tox, jailbreaks).
- Automatizar CI/CD completo con Docker y despliegues blue/green.
- Extender integraciones CRM (HubSpot, Pipedrive) y webhooks.

## Más allá de v3
- Búsqueda multimodal (texto+imagen).
- Model registry interno y versionado automático de prompts/modelos.
- Evaluaciones adversarias y red teaming continuo.
- Marketplace de playbooks por vertical.
