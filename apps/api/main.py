from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apps.api.logging_config import configure_logging
from apps.api.routers import intake, knowledge, leads, metrics

configure_logging()

app = FastAPI(title="UNIFY-LEADS API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(intake.router, prefix="/api/v1")
app.include_router(leads.router, prefix="/api/v1")
app.include_router(knowledge.router, prefix="/api/v1")
app.include_router(metrics.router, prefix="/api/v1")


@app.get("/health")
def health() -> dict[str, str]:
    """Endpoint de verificación utilizado por orquestadores y tests."""

    return {"status": "ok"}
