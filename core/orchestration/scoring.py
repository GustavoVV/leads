from __future__ import annotations

from typing import Dict, Tuple

DEFAULT_BINS = {
    "presupuesto": {
        "weight": 0.35,
        "bins": [(0, 1500, 0.1), (1500, 5000, 0.6), (5000, 1e9, 1.0)],
    },
    "urgencia": {
        "weight": 0.25,
        "values": {"alta": 1.0, "media": 0.6, "baja": 0.2},
    },
    "decision_maker": {"weight": 0.15, "values": {"si": 1.0, "no": 0.4}},
    "encaje_servicio": {
        "weight": 0.25,
        "values": {"programacion": 1.0, "documentacion": 0.8, "otro": 0.5},
    },
}


class LeadScorer:
    """Calcula un score ponderado para clasificar la madurez del lead."""

    def __init__(self, config: Dict[str, Dict]) -> None:
        self.config = config or DEFAULT_BINS

    def score(self, features: Dict[str, str]) -> Tuple[float, str]:
        """Devuelve el score normalizado y su categoría discreta."""

        total = 0.0
        weights = 0.0
        for name, spec in self.config.items():
            weight = spec.get("weight", 0.0)
            weights += weight
            value = features.get(name)
            if value is None:
                continue
            if "bins" in spec:
                try:
                    numeric = float(value)
                except (TypeError, ValueError):
                    numeric = 0.0
                for low, high, score in spec["bins"]:
                    if low <= numeric < high:
                        total += score * weight
                        break
            elif "values" in spec:
                total += spec["values"].get(str(value).lower(), 0.0) * weight
        normalized = total / weights if weights else 0.0
        if normalized >= 0.75:
            categoria = "caliente"
        elif normalized >= 0.45:
            categoria = "tibio"
        else:
            categoria = "frio"
        return round(normalized, 3), categoria


DEFAULT_SCORER = LeadScorer(DEFAULT_BINS)
