import streamlit as st
import json
from datetime import date

st.set_page_config(page_title="Programa — Festa Major de Sants 2026", page_icon="📅", layout="centered")

@st.cache_data
def load_program():
    with open("data/programa.json", "r", encoding="utf-8") as f:
        return json.load(f)

program = load_program()
festa = program["festa"]

st.markdown("""
<style>
    .program-header {
        background: linear-gradient(135deg, #1565c0 0%, #0277bd 50%, #00838f 100%);
        border-radius: 16px; padding: 1.5rem; text-align: center; color: #fff;
        margin-bottom: 1.5rem; box-shadow: 0 2px 10px rgba(0,0,0,0.15);
    }
    .program-header h1 { margin: 0; font-size: 1.5rem; }
    .event-card {
        background: #fff; border-left: 4px solid #1565c0; border-radius: 8px;
        padding: 0.8rem 1rem; margin: 0.5rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }
    .event-time { font-weight: 700; color: #1565c0; font-size: 1rem; }
    .event-title { font-weight: 600; font-size: 0.95rem; margin-top: 2px; }
    .event-desc { color: #666; font-size: 0.85rem; margin-top: 2px; }
    .event-tags { margin-top: 4px; }
    .event-tag {
        display: inline-block; background: #e3f2fd; color: #1565c0;
        padding: 2px 8px; border-radius: 10px; font-size: 0.75rem; margin-right: 4px;
    }
    .event-tag-kids {
        display: inline-block; background: #e8f5e9; color: #2e7d32;
        padding: 2px 8px; border-radius: 10px; font-size: 0.75rem; margin-right: 4px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="program-header">
    <h1>📅 Programa — {festa['name']}</h1>
    <p style="margin:0.3rem 0 0; opacity:0.9;">{festa['carrer']} — {festa['theme']}</p>
</div>
""", unsafe_allow_html=True)

# --- Map image ---
st.markdown("### 🗺️ Mapa dels carrers guarnits")
st.markdown(
    "Consulta el [mapa interactiu dels carrers guarnits]"
    "(https://beteve.cat/cultura/mapa-festes-sants-2024-planol-carrers-guarnits-foto-pdf/) "
    "per trobar tots els carrers participants."
)

st.markdown("---")

# --- Filters ---
st.markdown("### Filtra el programa")

col1, col2, col3 = st.columns(3)

all_days = [(d["date"], d["day_label"]) for d in program["program"]]
day_options = ["Tots els dies"] + [f"{label}" for _, label in all_days]

all_types = sorted(set(
    ev["type"] for d in program["program"] for ev in d["events"]
))
type_options = ["Tots els tipus"] + all_types

with col1:
    selected_day = st.selectbox("Dia", day_options)
with col2:
    selected_type = st.selectbox("Tipus d'activitat", type_options)
with col3:
    only_kids = st.checkbox("Només activitats familiars", value=False)

st.markdown("---")

# --- Carrer Papin program ---
st.markdown("### 🟠 Programa del Carrer Papin")

shown = 0
for day in program["program"]:
    if selected_day != "Tots els dies" and day["day_label"] != selected_day:
        continue

    events = day["events"]
    if selected_type != "Tots els tipus":
        events = [e for e in events if e["type"] == selected_type]
    if only_kids:
        events = [e for e in events if e.get("for_kids")]

    if not events:
        continue

    st.markdown(f"#### 📅 {day['day_label']}")
    for ev in events:
        kids_tag = '<span class="event-tag-kids">👨‍👩‍👧 Familiar</span>' if ev.get("for_kids") else ""
        tags_html = "".join(f'<span class="event-tag">{t}</span>' for t in ev.get("tags", [])[:3])
        loc = f" — {ev['location']}" if ev.get("location") and ev["location"] != "Carrer Papin" else ""

        st.markdown(f"""
        <div class="event-card">
            <div class="event-time">{ev['time']}{loc}</div>
            <div class="event-title">{ev['title']}</div>
            <div class="event-desc">{ev.get('description', '')}</div>
            <div class="event-tags">{kids_tag} {tags_html}</div>
        </div>
        """, unsafe_allow_html=True)
        shown += 1

if shown == 0:
    st.info("No hi ha activitats amb els filtres seleccionats.")

# --- Unitari program ---
st.markdown("---")
st.markdown("### 🔵 Actes Unitaris (tots els carrers)")

for day in program.get("unitari", []):
    if selected_day != "Tots els dies":
        matching_label = day["day_label"]
        if selected_day != matching_label:
            continue

    st.markdown(f"#### 📅 {day['day_label']}")
    for ev in day["events"]:
        st.markdown(f"""
        <div class="event-card" style="border-left-color: #0277bd;">
            <div class="event-time">{ev['time']}</div>
            <div class="event-title">{ev['title']}</div>
        </div>
        """, unsafe_allow_html=True)

# --- Other streets ---
st.markdown("---")
st.markdown("### 🏘️ Altres carrers participants")

for street in program.get("other_streets", []):
    st.markdown(f"- **{street['name']}**: {street.get('theme', '')}")

st.markdown("---")
st.caption("El programa és provisional i pot canviar. Consulteu amb la comissió per confirmacions.")
