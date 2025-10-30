import logging
from logging.config import dictConfig


def configure_logging() -> None:
    """Configura logging estructurado en JSON para toda la aplicación."""

    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "json": {
                    "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                    "fmt": "%(asctime)s %(levelname)s %(name)s %(message)s",
                }
            },
            "handlers": {
                "default": {
                    "level": "INFO",
                    "class": "logging.StreamHandler",
                    "formatter": "json",
                }
            },
            "loggers": {
                "": {"handlers": ["default"], "level": "INFO"},
                "uvicorn": {"handlers": ["default"], "level": "INFO", "propagate": False},
            },
        }
    )


logger = logging.getLogger("unify_leads")
