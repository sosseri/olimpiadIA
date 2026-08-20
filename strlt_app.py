import streamlit as st

st.set_page_config(
    page_title="PapinIA — Festa Major de Sants",
    page_icon="![🏟️](https://fonts.gstatic.com/s/e/notoemoji/17.0/1f3df_fe0f/72.png)",
    layout="centered",
    initial_sidebar_state="expanded",
)

from lib.decor import add_background, nav_bar

add_background(count=3)
nav_bar()

st.markdown("""
<style>
    .hub-shell {
        max-width: 1100px;
        margin: 0 auto;
    }
    .hub-header {
        background: linear-gradient(135deg, #1E3FD0 0%, #F0281E 100%);
        border-radius: 18px; padding: 1.5rem 1.25rem; text-align: center; color: #fff;
        margin-bottom: 1.25rem; box-shadow: 0 8px 20px rgba(30,63,208,0.22);
        border-bottom: 6px solid #F5CE18;
    }
    .hub-header h1 { margin: 0; font-size: clamp(2rem, 4vw, 2.8rem); }
    .hub-header p { margin: 0.4rem 0 0; font-size: 1rem; opacity: 0.96; }
    .hub-badge {
        display: inline-block; margin-top: 0.8rem; padding: 0.45rem 0.8rem;
        background: #F5CE18; color: #3B0D0D; border-radius: 999px; font-size: 0.82rem;
        font-weight: 700;
    }
    .hub-cta { margin: 1rem 0 1.25rem; }
    .topic-card {
        background: rgba(255,255,255,0.82); border: 1px solid rgba(30,63,208,0.08);
        border-radius: 16px; padding: 1rem; margin: 0.5rem 0; box-shadow: 0 6px 18px rgba(0,0,0,0.05);
    }
    .topic-card h3 { margin: 0 0 0.4rem; font-size: 1.1rem; }
    .topic-card p { margin: 0 0 0.8rem; color: #444; font-size: 0.92rem; }
    .disclaimer-card{ border-radius: 16px; padding: 14px 16px; border: 1px solid rgba(0,0,0,.08); background: linear-gradient(180deg, rgba(255,255,255,.7), rgba(255,255,255,.5)); backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px); box-shadow: 0 8px 24px rgba(0,0,0,.06); margin: 1.2rem 0 18px 0; }
    .disclaimer-title{ display:flex; gap:.5rem; align-items:center; font-weight: 700; font-size: .95rem; margin: 0 0 6px 0; }
    .disclaimer-text{ font-size: .85rem; line-height: 1.4; margin: 0; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hub-shell">
  <div class="hub-header">
    <h1>🎉 Festa Major de Sants 2026</h1>
    <p>PapinIA</p>
    <div class="hub-badge">22–30 d'agost de 2026 · L'Olimpíada Popular de 1936</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='hub-cta'>", unsafe_allow_html=True)
st.page_link("pages/1_xatbot.py", label="![💬](https://fonts.gstatic.com/s/e/notoemoji/17.0/1f4ac/72.png) Obrir el xatbot", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

cards = [
    ("![🏟️](https://fonts.gstatic.com/s/e/notoemoji/17.0/1f3df_fe0f/72.png) L'Olimpíada Popular de 1936", "pages/3_olimpiada.py", "Què va ser l'Olimpíada Popular de 1936?", "Recupera la història i el context de l’Olimpíada Popular de 1936."),
    ("![📅](https://fonts.gstatic.com/s/e/notoemoji/17.0/1f4c5/72.png) Programa d'activitats", "pages/2_programa.py", "Què hi ha avui al carrer Papin?", "Consulta les activitats del carrer Papin i de la festa."),
    ("![🎨](https://fonts.gstatic.com/s/e/notoemoji/17.0/1f3a8/72.png) El guarnit del Papin", "pages/5_guarnit_papin.py", "Com està fet el guarnit d'aquest any?", "Descobreix el tema, els materials i la idea del guarnit."),
    ("![🏠](https://fonts.gstatic.com/s/e/notoemoji/17.0/1f3e0/72.png) Els carrers de la festa", "pages/6_festa_major.py", "Quins carrers participen a la festa?", "Coneix els carrers, les comissions i la tradició festiva del barri."),
    ("![📸](https://fonts.gstatic.com/s/e/notoemoji/17.0/1f4f8/72.png) Arxiu de fotos", "pages/4_arxiu.py", None, "Explora imatges històriques i material visual del barri i la festa."),
    ("![🙋](https://fonts.gstatic.com/s/e/notoemoji/17.0/1f64b/72.png) Participar a la comissió", "pages/7_participar.py", "Com puc participar a la comissió?", "Troba com sumar-te a la comissió de festes del carrer Papin."),
]

cols = st.columns(2)
for i, (title, page, seed, description) in enumerate(cards):
    with cols[i % 2]:
        st.markdown(f"<div class='topic-card'><h3>{title}</h3><p>{description}</p></div>", unsafe_allow_html=True)
        st.page_link(page, label="![📖](https://fonts.gstatic.com/s/e/notoemoji/17.0/1f4d6/72.png) Llegir més", use_container_width=True)
        if seed:
            def _make_callback(seed_value=seed):
                def _cb():
                    st.session_state["pending_question"] = seed_value
                    st.switch_page("pages/1_xatbot.py")
                return _cb
            st.button("![💬](https://fonts.gstatic.com/s/e/notoemoji/17.0/1f4ac/72.png) Pregunta-ho", on_click=_make_callback(), key=f"hub_{i}", use_container_width=True)

st.markdown("""
<div class="disclaimer-card">
  <div class="disclaimer-title">🤖 Avis de la festa</div>
  <p class="disclaimer-text">
    Aquesta és una intel·ligència artificial feta per la Festa Major de Sants. 🎉
    🕵️ Pot generar informació incorrecta i no ens fem responsables de l’ús inadequat
    que en puguin fer adults massa esverats o criatures 🎈.
    🍻 Pren-t’ho amb esperit festiu i, si tens dubtes seriosos, pregunta a la comissió! 🍻
  </p>
</div>
""", unsafe_allow_html=True)


