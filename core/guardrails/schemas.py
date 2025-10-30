ROUTER_OUTPUT_SCHEMA = {
    "type": "object",
    "required": ["vertical", "lead_type", "confidence"],
    "properties": {
        "vertical": {"type": "string"},
        "lead_type": {"type": "string"},
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        "reasoning": {"type": "string"},
    },
}


COMPOSER_OUTPUT_SCHEMA = {
    "type": "object",
    "required": ["answer", "citations", "score", "categoria", "siguientes_pasos"],
    "properties": {
        "answer": {
            "type": "object",
            "required": ["asunto", "cuerpo"],
            "properties": {
                "asunto": {"type": "string"},
                "cuerpo": {"type": "string"},
                "preguntas_qual": {
                    "type": "array",
                    "items": {"type": "string"},
                    "maxItems": 3,
                },
            },
        },
        "citations": {"type": "array", "items": {"type": "object"}},
        "score": {"type": "number"},
        "categoria": {"type": "string", "enum": ["caliente", "tibio", "frio"]},
        "siguientes_pasos": {"type": "array", "items": {"type": "string"}},
    },
}
