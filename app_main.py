import streamlit as st

st.set_page_config(
    page_title="Festa Major de Sants 2026 — Carrer Papin",
    page_icon="🏟️",
    layout="centered",
    initial_sidebar_state="auto",
)

st.markdown("""
<style>
    body { background-color: #fafafa; font-family: 'Helvetica Neue', sans-serif; }
    .main-header {
        background: linear-gradient(135deg, #c62828 0%, #d84315 50%, #f9a825 100%);
        border-radius: 16px; padding: 2rem; text-align: center; color: #fff;
        margin-bottom: 1.5rem; box-shadow: 0 2px 10px rgba(0,0,0,0.15);
    }
    .main-header h1 { margin: 0; font-size: 1.8rem; text-shadow: 1px 1px 3px rgba(0,0,0,0.3); }
    .main-header h2 { margin-top: 0.5rem; font-weight: 400; color: #fff; font-size: 1.1rem; }
    .badge {
        display: inline-block; margin-top: 0.8rem; padding: 0.3rem 0.8rem;
        background: rgba(255,255,255,0.25); color: #fff; border-radius: 12px;
        font-size: 0.9rem; font-weight: 600; backdrop-filter: blur(4px);
    }
    .nav-card {
        background: #fff; border-radius: 12px; padding: 1.2rem;
        border: 1px solid #eee; margin-bottom: 0.8rem;
        box-shadow: 0 1px 4px rgba(0,0,0,0.05);
        transition: transform 0.2s;
    }
    .nav-card:hover { transform: translateY(-2px); }
    .nav-card h3 { margin: 0 0 0.3rem 0; font-size: 1.1rem; }
    .nav-card p { margin: 0; color: #666; font-size: 0.9rem; }
    .disclaimer-card {
        border-radius: 16px; padding: 14px 16px;
        border: 1px solid rgba(0,0,0,.08);
        background: linear-gradient(180deg, rgba(255,255,255,.7), rgba(255,255,255,.5));
        backdrop-filter: blur(6px); box-shadow: 0 8px 24px rgba(0,0,0,.06);
        margin: 18px 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>🏟️ Carrer Papin — Festa Major de Sants 2026</h1>
    <h2>L'Olimpíada Popular de Barcelona de 1936</h2>
    <div class="badge">22 — 30 d'agost de 2026</div>
</div>
""", unsafe_allow_html=True)

st.markdown("### Benvingudes a la Festa Major de Sants!")
st.markdown(
    "El carrer Papin us dóna la benvinguda! Enguany, el nostre guarnit està dedicat a "
    "**l'Olimpíada Popular de Barcelona de 1936**, l'alternativa antifeixista als Jocs "
    "Olímpics de Berlín organitzats pel règim nazi."
)

st.markdown("---")
st.markdown("### Navega per l'aplicació")

col1, col2 = st.columns(2)
with col1:
    st.page_link("pages/1_xat.py", label=(**Xat amb PapinIA**", icon="💬")
    st.caption("Parla amb la nostra intel·ligència artificial festiva")

    st.page_link("pages/2_programa.py", label="**Programa**", icon="📅")
    st.caption("Consulta el programa d'activitats dia a dia")

    st.page_link("pages/5_festa_major.py", label="**Festa Major de Sants**", icon="🎭")
    st.caption("Orígens i història de la festa")

with col2:
    st.page_link("pages/3_olimpiada.py", label="**L'Olimpíada Popular**", icon="🏟️")
    st.caption("La història de l'Olimpíada Popular de 1936")

    st.page_link("pages/4_arxiu.py", label="**Arxiu fotogràfic**", icon="📸")
    st.caption("Imatges de la festa i el carrer")

st.markdown("---")

st.markdown("""
<div class="disclaimer-card">
  <p style="font-weight:700; font-size:.95rem; margin:0 0 6px 0;">🤖 Avís</p>
  <p style="font-size:.85rem; line-height:1.4; margin:0;">
    Aquesta aplicació inclou una intel·ligència artificial feta per la Festa Major de Sants.
    Pot generar informació incorrecta i no ens fem responsables de l'ús inadequat.
    Pren-t'ho amb esperit festiu i, si tens dubtes, pregunta a la comissió!
  </p>
</div>
""", unsafe_allow_html=True)

st.markdown(
    "✊ **La Comissió del carrer Papin** és contrària a qualsevol guerra com a resolució de conflictes. "
    "Defensem la llibertat, l'autodeterminació dels pobles i la pau. 🕊️"
)
