import streamlit as st
import json
import plotly.graph_objects as go
from io import BytesIO

st.set_page_config(page_title="Self-Storage Dashboard", layout="wide")
st.title("📦 Shurgard Self‑Storage Business Dashboard")
st.caption("Nalepastraße 162 – Lagerräume mit Business-Center  \nwww.schimmel-automobile.de")

# --- Drag & Drop Upload ---
uploaded_file = st.file_uploader(
    "Dashboard-Datei hochladen",
    type=["xlsx"],
    accept_multiple_files=False,
    help="Ziehen Sie Ihre 'dashboard_summary.json' hierher oder klicken Sie zum Durchsuchen"
)

data = {}
if uploaded_file is not None:
    try:
        # Read file content as bytes and decode to string
        content = BytesIO(uploaded_file.getvalue()).read().decode('utf-8')
        data = json.loads(content)
        st.success("Daten erfolgreich geladen!")
    except Exception as e:
        st.error(f"Fehler beim Verarbeiten der Datei: {e}")
        st.stop()
else:
    st.info("Bitte laden Sie eine JSON-Datei per Drag & Drop hoch")
    st.stop()

# --- KPI Kacheln ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Belegte Einheiten", data.get("belegt", 0))
col2.metric("Freie Einheiten", data.get("frei", 0))
col3.metric("Ø Vertragsdauer (Monate)", round(data.get("vertragsdauer_durchschnitt", 0), 1))
col4.metric("Auto-Reminder gesendet", data.get("reminder_automat", 0))

# --- Social Media Stats & Weitere KPIs ---
col5, col6, col7, col8 = st.columns(4)
col5.metric("Facebook-Follower", data.get("social_facebook", 0))
col6.metric("Google Reviews", data.get("social_google", 0))
col7.metric("Ø Belegungsgrad (%)", data.get("belegungsgrad", 0))

# Calculate recommendation rate safely
kundenherkunft = data.get("kundenherkunft", {})
empfehlungen = kundenherkunft.get("Empfehlung", 0)
total_kunden = max(sum(kundenherkunft.values()), 1)  # Prevent division by zero
col8.metric("Empfehlungsrate (%)", round(100 * empfehlungen / total_kunden, 1))

# --- Auslastung Pie ---
auslastung_fig = go.Figure(data=[
    go.Pie(
        labels=["Belegt", "Frei"],
        values=[data.get("belegt", 0), data.get("frei", 0)],
        hole=.5,
        marker_colors=["royalblue", "lightgray"],
        textinfo="percent+value"
    )
])
auslastung_fig.update_layout(
    title="Auslastung Lagerräume",
    showlegend=True,
    margin=dict(t=40, b=20)
)

# --- Neukundenentwicklung ---
kunden_fig = go.Figure(data=[
    go.Bar(
        x=data.get("neukunden_labels", []),
        y=data.get("neukunden_monat", []),
        marker_color="orange",
        textposition="auto"
    )
])
kunden_fig.update_layout(
    title="Neukunden pro Monat",
    xaxis_title="Monat",
    yaxis_title="Neukunden",
    margin=dict(t=40, b=40)
)

# --- Zahlungsstatus ---
zahlungsstatus = data.get("zahlungsstatus", {})
zahlung_fig = go.Figure(data=[
    go.Bar(
        x=["Bezahlt", "Offen", "Überfällig"],
        y=[
            zahlungsstatus.get("bezahlt", 0),
            zahlungsstatus.get("offen", 0),
            zahlungsstatus.get("überfällig", 0)
        ],
        marker_color=["seagreen", "gold", "crimson"],
        textposition="auto"
    )
])
zahlung_fig.update_layout(
    title="Zahlungsstatus",
    yaxis_title="Anzahl Rechnungen",
    margin=dict(t=40, b=20)
)

# --- Kundenherkunft ---
kundenherkunft = data.get("kundenherkunft", {})
herkunft_fig = go.Figure(data=[
    go.Pie(
        labels=list(kundenherkunft.keys()),
        values=list(kundenherkunft.values()),
        hole=.4,
        textinfo="percent+label",
        marker_colors=px.colors.qualitative.Pastel
    )
])
herkunft_fig.update_layout(
    title="Kundenherkunft",
    showlegend=False,
    margin=dict(t=40, b=20),
    height=400
)

# --- Dashboard Layout ---
col9, col10 = st.columns(2)
with col9:
    st.plotly_chart(auslastung_fig, use_container_width=True)
    st.plotly_chart(kunden_fig, use_container_width=True)
with col10:
    st.plotly_chart(zahlung_fig, use_container_width=True)
    st.plotly_chart(herkunft_fig, use_container_width=True)

st.caption("Daten per Drag-and-Drop aktualisierbar | Kontakt: info@schimmel-automobile.de")
