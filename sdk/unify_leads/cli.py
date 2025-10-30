from __future__ import annotations

import json
from typing import Optional

import typer

from sdk.unify_leads import UnifyLeadsClient

app = typer.Typer(help="CLI para interactuar con UNIFY-LEADS")


@app.command()
def intake(
    base_url: str = typer.Option(..., help="URL base de la API"),
    tenant_id: str = typer.Option(...),
    canal: str = typer.Option("web"),
    body: str = typer.Option(...),
    subject: str = typer.Option(""),
):
    client = UnifyLeadsClient(base_url)
    payload = {
        "tenant_id": tenant_id,
        "canal": canal,
        "payload": {"subject": subject, "body": body, "from": "cli@demo"},
    }
    response = client.intake(payload)
    typer.echo(json.dumps(response, indent=2))


@app.command()
def compose(
    base_url: str = typer.Option(...),
    lead_id: str = typer.Option(...),
    max_tokens: int = typer.Option(600),
):
    client = UnifyLeadsClient(base_url)
    response = client.compose(lead_id, max_tokens=max_tokens)
    typer.echo(json.dumps(response, indent=2))


if __name__ == "__main__":
    app()
