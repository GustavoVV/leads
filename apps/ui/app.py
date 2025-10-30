import json
from datetime import datetime, timezone

import pandas as pd
import streamlit as st

from apps.api.services.store import STORE

st.set_page_config(page_title="UNIFY-LEADS Panel", layout="wide")
st.title("Panel UNIFY-LEADS")

leads = list(STORE.all_leads())
if not leads:
    st.info("No hay leads registrados todavía. Usa el endpoint /intake para crear uno.")
else:
    df = pd.DataFrame(
        [
            {
                "Lead ID": lead.id,
                "Tenant": lead.tenant_id,
                "Vertical": lead.vertical,
                "Lead Type": lead.lead_type,
                "Score": lead.score,
                "Categoria": lead.categoria,
                "Creado": lead.created_at,
            }
            for lead in leads
        ]
    )
    st.metric("Leads totales", len(leads))
    st.metric("Score medio", round(df["Score"].fillna(0).mean(), 2))
    earliest = df["Creado"].min()
    if pd.notna(earliest):
        delta_minutes = (datetime.now(timezone.utc) - earliest).total_seconds() / 60
        st.metric("TTA estimado (min)", round(delta_minutes, 1))
    st.dataframe(df)

st.sidebar.header("Detalle Lead")
lead_id = st.sidebar.text_input("Lead ID")
if lead_id:
    lead = STORE.get_lead(lead_id)
    if lead:
        st.sidebar.json(json.loads(lead.model_dump_json()))
    else:
        st.sidebar.warning("Lead no encontrado")
