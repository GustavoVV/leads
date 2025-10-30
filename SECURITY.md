# Seguridad en UNIFY-LEADS

## Principios
- **Privacidad por diseño:** minimizar exposición de PII mediante enmascaramiento y control de acceso basado en rol.
- **Defensa en profundidad:** autenticación, rate limiting, validación de esquemas y auditoría de acciones.
- **Observabilidad:** trazas estructuradas y métricas para detectar anomalías.

## Controles técnicos
- Validación estricta de entradas con Pydantic y JSON Schema.
- Cifrado en reposo de base de datos y almacenamiento de objetos (KMS).
- Rotación trimestral de claves `OPENAI_API_KEY`, `PINECONE_API_KEY` y credenciales SMTP.
- Rate limiting configurable mediante `RATE_LIMITS_JSON` y almacenamiento redis.
- Mascarilla automática de campos sensibles (`email`, `phone`, `dni`) en logs.
- Webhooks autenticados con firmas HMAC (`X-UNIFY-SIGNATURE`).

## Gestión de secretos
- Almacenamiento en AWS Secrets Manager.
- Acceso restringido con IAM y políticas least privilege.
- `.env` únicamente en entornos locales, nunca comprometido.

## Seguridad LLM / RAG
- Prompt templates versionados en `core/guardrails/prompts/`.
- Respuestas validadas contra esquema `ComposerOutput` antes de enviarse.
- Verificación de groundedness con RAGAS y bloqueo de respuestas sin citas.
- Lista blanca de herramientas LangChain, rechazar URLs externas no validadas.

## Cumplimiento
- Registro de consentimientos y opt-out en tabla `interactions`.
- Logs de auditoría (`logger.audit`) conservados 365 días.
- DPIA para clientes europeos y DPA firmado.

## Roadmap de seguridad
- V1.1: SSO para panel Streamlit y escaneo SAST.
- V1.2: Gestión de secretos con Vault + rotación automática.
- V1.3: Red teaming interno y automatización de runbooks de respuesta.
