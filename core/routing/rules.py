from __future__ import annotations

from typing import Dict, Tuple


RULE_KEYWORDS: Dict[str, Dict[str, Tuple[str, str]]] = {
    "consultoria": {
        "python": ("consultoria", "programacion"),
        "automatizacion": ("consultoria", "automatizacion"),
        "documentacion": ("consultoria", "documentacion"),
    },
    "inmobiliaria": {
        "alquiler": ("inmobiliaria", "alquiler"),
        "venta": ("inmobiliaria", "venta"),
        "hipoteca": ("inmobiliaria", "financiacion"),
    },
    "gestoria": {
        "tramite": ("gestoria", "tramites"),
        "fiscal": ("gestoria", "fiscal"),
    },
}


def route_by_keywords(text: str) -> Tuple[str, str, float, str]:
    lowered = text.lower()
    for vertical, keywords in RULE_KEYWORDS.items():
        for keyword, (v, lead_type) in keywords.items():
            if keyword in lowered:
                reasoning = f"Coincidencia de palabra clave '{keyword}'"
                return v, lead_type, 0.82, reasoning
    return "consultoria", "general", 0.55, "Sin coincidencias; fallback default"
