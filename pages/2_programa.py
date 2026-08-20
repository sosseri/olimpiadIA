import streamlit as st
import streamlit.components.v1 as components
import json
import html as html_lib

MAP_EMBED_URL = "https://www.google.com/maps/d/embed?mid=1Mm-g7z6ukfmLSi5zEH3uvXwQ2secCTER&ll=41.3766953765755%2C2.134091757378447&z=15"

st.set_page_config(page_title="Programa — Festa Major de Sants 2026", page_icon="📅", layout="centered", initial_sidebar_state="expanded")

from lib.decor import section_accent, nav_bar

nav_bar()

@st.cache_data
def load_program():
    with open("data/programa.json", "r", encoding="utf-8") as f:
        return json.load(f)

program = load_program()
festa = program["festa"]
streets = program["streets"]

# Ordered list of streets for the dropdown (papin first, then alphabetical, unitari last)
STREET_ORDER = [
    ("papin", "🟠 Carrer Papin"),
    ("alcolea_baix", "Carrer d'Alcolea de Baix"),
    ("alcolea_dalt", "Carrer d'Alcolea de Dalt"),
    ("farga", "Plaça de la Farga"),
    ("finlandia", "Carrer de Finlàndia"),
    ("galileu", "Carrer de Galileu"),
    ("guadiana", "Carrer de Guadiana"),
    ("sagunt", "Carrer de Sagunt"),
    ("valladolid", "Carrer de Valladolid"),
    ("vallespir_baix", "Carrer de Vallespir de Baix"),
    ("vallespir_dalt", "Carrer de Vallespir de Dalt"),
    ("unitari", "🔵 Actes Unitaris"),
]
# Only show streets that exist in the data
available_streets = [(k, label) for k, label in STREET_ORDER if k in streets]

# All days across all streets, deduped and sorted
all_dates = sorted({
    date_key
    for s in streets.values()
    for date_key in s["days"].keys()
})
DAY_LABELS = {
    date_key: next(
        (day_data["day_label"] for s in streets.values()
         for dk, day_data in s["days"].items() if dk == date_key),
        date_key
    )
    for date_key in all_dates
}

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
    .street-header {
        background: #f5f5f5; border-radius: 8px; padding: 0.5rem 1rem;
        margin: 1rem 0 0.5rem; font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="program-header">
    <h1>📅 Programa — {festa['name']}</h1>
    <p style="margin:0.3rem 0 0; opacity:0.9;">{festa['carrer']} — {festa['theme']}</p>
</div>
""", unsafe_allow_html=True)

st.markdown("### Filtra el programa")

col1, col2 = st.columns(2)

day_options = ["Tots els dies"] + [DAY_LABELS[d] for d in all_dates]
street_dropdown_options = ["Tots els carrers"] + [label for _, label in available_streets]

with col1:
    selected_day_label = st.selectbox("Dia", day_options)
with col2:
    selected_street_label = st.selectbox("Carrer", street_dropdown_options)

# Resolve selected date key
selected_date = None
if selected_day_label != "Tots els dies":
    for dk, lbl in DAY_LABELS.items():
        if lbl == selected_day_label:
            selected_date = dk
            break

# Resolve selected street keys
if selected_street_label == "Tots els carrers":
    selected_keys = [k for k, _ in available_streets]
else:
    selected_keys = [k for k, label in available_streets if label == selected_street_label]

st.markdown("---")


def render_events(street_key, accent_color="#1565c0"):
    street_data = streets[street_key]
    days_to_show = sorted(street_data["days"].keys())
    if selected_date:
        days_to_show = [d for d in days_to_show if d == selected_date]

    shown = 0
    for dk in days_to_show:
        day_data = street_data["days"][dk]
        events = day_data["events"]
        if not events:
            continue

        st.markdown(f"#### 📅 {day_data['day_label']}")
        for ev in events:
            tags_html = "".join(f'<span class="event-tag">{t}</span>' for t in ev.get("tags", [])[:3])
            time_str = ev.get("time") or "—"
            title = html_lib.escape(ev.get("title", ""))
            desc = html_lib.escape(ev.get("description", ""))
            st.markdown(f"""
            <div class="event-card" style="border-left-color:{accent_color};">
                <div class="event-time" style="color:{accent_color};">{time_str}</div>
                <div class="event-title">{title}</div>
                <div class="event-desc">{desc}</div>
                <div class="event-tags">{tags_html}</div>
            </div>
            """, unsafe_allow_html=True)
            shown += 1
    return shown


ACCENT_COLORS = {
    "papin": "#e65100",
    "unitari": "#0277bd",
    "alcolea_baix": "#6a1b9a",
    "alcolea_dalt": "#ad1457",
    "farga": "#2e7d32",
    "finlandia": "#00695c",
    "galileu": "#1565c0",
    "guadiana": "#4527a0",
    "sagunt": "#c62828",
    "valladolid": "#558b2f",
    "vallespir_baix": "#4e342e",
    "vallespir_dalt": "#37474f",
}

accent_i = 0
for key in selected_keys:
    if key not in streets:
        continue
    street_data = streets[key]
    label = next((lbl for k, lbl in available_streets if k == key), street_data["name"])
    color = ACCENT_COLORS.get(key, "#1565c0")

    section_accent(accent_i)
    accent_i += 1
    st.markdown(f'<div class="street-header" style="border-left: 4px solid {color}; padding-left:1rem;">{label} — <em>{street_data.get("theme","")}</em></div>', unsafe_allow_html=True)

    shown = render_events(key, accent_color=color)
    if shown == 0:
        st.info(f"No hi ha activitats a {street_data['name']} amb els filtres seleccionats.")

st.markdown("---")
st.caption("El programa és provisional i pot canviar. Consulteu amb la comissió per confirmacions.")

section_accent(accent_i)
st.markdown("### 🗺️ Mapa dels carrers guarnits")
st.markdown(
    "Explora el mapa interactiu per trobar tots els carrers participants "
    "amb la seva ubicació i temàtica."
)
components.iframe(MAP_EMBED_URL, height=480)
