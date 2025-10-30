from functools import lru_cache
from typing import Optional

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    app_env: str = Field("dev", alias="APP_ENV")
    secret_key: str = Field(..., alias="SECRET_KEY")
    db_url: str = Field(..., alias="DB_URL")
    vector_store: str = Field("chroma", alias="VECTOR_STORE")
    pinecone_api_key: Optional[str] = Field(None, alias="PINECONE_API_KEY")
    pinecone_env: Optional[str] = Field(None, alias="PINECONE_ENV")
    llm_provider: str = Field("openai", alias="LLM_PROVIDER")
    openai_api_key: Optional[str] = Field(None, alias="OPENAI_API_KEY")
    hf_token: Optional[str] = Field(None, alias="HF_TOKEN")
    embedding_model: str = Field(
        "sentence-transformers/all-MiniLM-L6-v2", alias="EMBEDDING_MODEL"
    )
    smtp_host: str = Field(..., alias="SMTP_HOST")
    smtp_port: int = Field(587, alias="SMTP_PORT")
    smtp_user: Optional[str] = Field(None, alias="SMTP_USER")
    smtp_pass: Optional[str] = Field(None, alias="SMTP_PASS")
    twilio_sid: Optional[str] = Field(None, alias="TWILIO_SID")
    twilio_token: Optional[str] = Field(None, alias="TWILIO_TOKEN")
    twilio_whatsapp_from: Optional[str] = Field(
        None, alias="TWILIO_WHATSAPP_FROM"
    )
    langsmith_api_key: Optional[str] = Field(None, alias="LANGSMITH_API_KEY")
    rate_limits_json: str = Field("{}", alias="RATE_LIMITS_JSON")

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    return Settings()
