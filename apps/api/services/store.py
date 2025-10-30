from __future__ import annotations

import itertools
import random
import string
from collections import defaultdict
from datetime import datetime, timezone
from typing import Dict, Iterable, List, Optional

from apps.api.schemas.base import LeadRecord


class InMemoryStore:
    """Almacén ligero que persiste los leads en memoria durante la ejecución.

    Sirve como _stand-in_ para una base de datos o CRM real y permite probar el
    flujo completo de la API sin dependencias externas.
    """

    def __init__(self) -> None:
        self._leads: Dict[str, LeadRecord] = {}
        self._lead_messages: Dict[str, List[str]] = defaultdict(list)
        self._id_counter = itertools.count(1)

    def _generate_id(self) -> str:
        """Genera un identificador estable del tipo `L0001ABCD`."""

        counter = next(self._id_counter)
        suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
        return f"L{counter:04d}{suffix}"

    def create_lead(self, tenant_id: str, canal: str, payload: Dict[str, str]) -> LeadRecord:
        """Crea un lead y lo almacena en memoria.

        Parameters
        ----------
        tenant_id:
            Identificador del tenant que origina el lead.
        canal:
            Canal por el que se recibió la interacción (email, whatsapp, etc.).
        payload:
            Cuerpo del mensaje normalizado.
        """

        now = datetime.now(timezone.utc)
        lead_id = self._generate_id()
        record = LeadRecord(
            id=lead_id,
            tenant_id=tenant_id,
            canal=canal,
            payload=payload,
            created_at=now,
            updated_at=now,
        )
        self._leads[lead_id] = record
        return record

    def update_lead(self, lead_id: str, **kwargs) -> LeadRecord:
        """Actualiza un lead existente y devuelve la versión persistida."""

        record = self._leads[lead_id]
        data = record.model_dump()
        data.update(kwargs)
        data["updated_at"] = datetime.now(timezone.utc)
        updated = LeadRecord(**data)
        self._leads[lead_id] = updated
        return updated

    def add_message(self, lead_id: str, body: str) -> None:
        """Añade el cuerpo de un mensaje asociado al lead."""

        self._lead_messages[lead_id].append(body)

    def get_lead(self, lead_id: str) -> Optional[LeadRecord]:
        """Recupera un lead por identificador o `None` si no existe."""

        return self._leads.get(lead_id)

    def all_leads(self) -> Iterable[LeadRecord]:
        """Itera sobre todos los leads almacenados."""

        return self._leads.values()

    def lead_messages(self, lead_id: str) -> List[str]:
        """Devuelve el histórico de mensajes asociados a un lead."""

        return self._lead_messages.get(lead_id, [])


STORE = InMemoryStore()
