import streamlit as st

st.set_page_config(
    page_title="Participar",
    page_icon="![🙋](https://fonts.gstatic.com/s/e/notoemoji/17.0/1f64b/72.png)",
    layout="centered",
    initial_sidebar_state="expanded",
)

from lib.decor import add_background, section_accent, nav_bar

add_background(count=2)
nav_bar()

st.markdown("""
<style>
    .participar-header {
        background: linear-gradient(135deg, #1E3FD0 0%, #F0281E 100%);
        border-radius: 16px; padding: 1.5rem; text-align: center; color: #fff;
        margin-bottom: 1.5rem; box-shadow: 0 2px 10px rgba(0,0,0,0.15);
        border-bottom: 6px solid #F5CE18;
    }
    .participar-header h1 { margin: 0; font-size: 1.5rem; }
    .participar-header p { margin: 0.3rem 0 0; font-size: 0.95rem; opacity: 0.92; }
    .info-box {
        background: #fff; border-left: 4px solid #1E3FD0;
        padding: 1rem 1.2rem; border-radius: 0 8px 8px 0; margin: 0.8rem 0;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }
    .info-box a { color: #1E3FD0; font-weight: 600; text-decoration: none; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="participar-header">
    <h1>![🙋](https://fonts.gstatic.com/s/e/notoemoji/17.0/1f64b/72.png) Suma't a la Comissió del Carrer Papin</h1>
    <p>La festa la fem entre totes — vine a donar-nos un cop de mà!</p>
</div>
""", unsafe_allow_html=True)

section_accent(0)

st.markdown("""
## Com participar-hi

La **Comissió de Festes del Carrer Papin** va renéixer el **2014** gràcies a un grup de
veïnes que volien recuperar la tradició, i des d'aleshores no ha parat de créixer.
L'ambient és **inclusiu i obert a tothom**, i **no cal cap compromís constant**:
qualsevol ajuda és benvinguda, tant si pots venir sempre com de tant en tant. ![🎉](https://fonts.gstatic.com/s/e/notoemoji/17.0/1f389/72.png)
""")

st.markdown("""
<div class="info-box">
![📸](https://fonts.gstatic.com/s/e/notoemoji/17.0/1f4f8/72.png) <b>Instagram:</b> <a href="https://instagram.com/comissiopapin" target="_blank">@comissiopapin</a><br>
![📍](https://fonts.gstatic.com/s/e/notoemoji/17.0/1f4cd/72.png) <b>Punt de trobada / adreça:</b> Orfeó de Sants, C. Miquel Àngel, 54<br>
![🍻](https://fonts.gstatic.com/s/e/notoemoji/17.0/1f37b/72.png) <b>Nota:</b> Parla amb la comissió a la barra del carrer Papin durant la festa.
</div>
""", unsafe_allow_html=True)

st.markdown("### Tens dubtes? Pregunta-ho a la PapinIA")


def _ask_participar():
    st.session_state["pending_question"] = "Com puc participar a la comissió?"
    st.switch_page("pages/1_xatbot.py")


st.button("![💬](https://fonts.gstatic.com/s/e/notoemoji/17.0/1f4ac/72.png) Pregunta-ho al xatbot", on_click=_ask_participar, use_container_width=True)
