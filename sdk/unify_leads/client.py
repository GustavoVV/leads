from __future__ import annotations

from typing import Any, Dict, Optional

import httpx


class UnifyLeadsClient:
    def __init__(self, base_url: str, api_key: Optional[str] = None, timeout: float = 10.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

    def _headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def intake(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(
                f"{self.base_url}/api/v1/intake/message",
                json=payload,
                headers=self._headers(),
            )
            response.raise_for_status()
            return response.json()

    def compose(self, lead_id: str, max_tokens: int = 600) -> Dict[str, Any]:
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(
                f"{self.base_url}/api/v1/leads/{lead_id}/compose",
                json={"max_tokens": max_tokens},
                headers=self._headers(),
            )
            response.raise_for_status()
            return response.json()

    def export_leads(self, format: str = "csv") -> Dict[str, Any]:
        with httpx.Client(timeout=self.timeout) as client:
            response = client.get(
                f"{self.base_url}/api/v1/leads/export",
                params={"format": format},
                headers=self._headers(),
            )
            response.raise_for_status()
            return response.json()
