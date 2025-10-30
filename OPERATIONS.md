# Operaciones UNIFY-LEADS

Este documento resume los procedimientos operativos mínimos para el MVP v1.0.

## Entornos
- **dev:** ejecución local utilizando `uvicorn` y base de datos SQLite temporal.
- **demo:** despliegue en Hugging Face Spaces, autenticado con variables `OPENAI_API_KEY` y `LANGSMITH_API_KEY`.
- **pre-prod:** despliegue Docker en EC2 con Postgres gestionado y Pinecone.

## Puesta en marcha local
1. Crear entorno virtual y ejecutar `pip install -e .[dev]`.
2. Exportar variables de entorno descritas en `.env.example`.
3. Levantar servicios auxiliares con `docker compose -f infra/docker/compose.dev.yaml up -d`.
4. Lanzar API con `uvicorn apps.api.main:app --reload`.
5. Ejecutar UI Streamlit con `streamlit run apps/ui/app.py`.

## Gestión de datos
- Migraciones con `alembic upgrade head`.
- Snapshots de Chroma semanales almacenados en `s3://unify-leads-vectors/`.
- Exportaciones CRM descargadas como CSV y sincronizadas con Google Sheets mediante `sdk/unify_leads/cli.py sync-sheets`.

## Incidencias
- Activar modo mantenimiento mediante variable `MAINTENANCE_MODE=1`.
- Registrar incidentes críticos en `ops/incidents/YYYY-MM-DD.md`.
- Post-mortem de 5 porqués obligatorio para incidentes P0/P1.

## SLOs iniciales
- Disponibilidad API ≥ 99% mensual.
- Tiempo medio de respuesta < 1.5s en endpoints `/intake` y `/compose`.
- Latencia de follow-up programado ±5 minutos respecto a ventana planificada.

## Automatizaciones
- GitHub Actions ejecuta pruebas y lint en cada PR.
- Despliegues demo automatizados al fusionar en rama `main` con tag `demo-*`.
- Backups diarios de Postgres gestionados por RDS.

## Roadmap operativo
- Instrumentar métricas con Prometheus en v1.1.
- Integrar alertas con PagerDuty en v1.2.
- Añadir runbooks detallados por vertical en v1.3.
