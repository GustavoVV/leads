import jsonschema

from apps.api.schemas.base import ComposerOutput
from core.guardrails.schemas import COMPOSER_OUTPUT_SCHEMA


def test_composer_output_schema_validation():
    sample = ComposerOutput(
        answer={
            "asunto": "Seguimiento consultoria",
            "cuerpo": "Gracias por tu interés.",
            "preguntas_qual": ["¿Cuál es el presupuesto?"],
        },
        citations=[{"uri": "s3://demo", "snippet": "texto"}],
        score=0.8,
        categoria="caliente",
        siguientes_pasos=["Agendar llamada"],
    ).model_dump()
    jsonschema.validate(sample, COMPOSER_OUTPUT_SCHEMA)
