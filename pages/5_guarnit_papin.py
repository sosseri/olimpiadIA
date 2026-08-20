import streamlit as st

st.set_page_config(page_title="El Guarnit del Carrer Papin", page_icon="🏟️", layout="centered", initial_sidebar_state="expanded")

from lib.decor import section_accent, nav_bar

nav_bar()

st.markdown("""
<style>
    .guarnit-header {
        background: linear-gradient(135deg, #880e4f 0%, #ad1457 50%, #c2185b 100%);
        border-radius: 16px; padding: 1.5rem; text-align: center; color: #fff;
        margin-bottom: 1.5rem; box-shadow: 0 2px 10px rgba(0,0,0,0.15);
    }
    .guarnit-header h1 { margin: 0; font-size: 1.5rem; }
    .guarnit-header p { margin: 0.3rem 0 0; font-size: 0.95rem; opacity: 0.9; }
    .info-box {
        background: #fce4ec; border-left: 4px solid #c2185b;
        padding: 1rem; border-radius: 0 8px 8px 0; margin: 0.8rem 0;
    }
    .material-card {
        background: #fff8f9; border: 1px solid #f8bbd9;
        border-radius: 10px; padding: 1rem; margin: 0.5rem 0;
    }
    .section-title {
        font-size: 1.1rem; font-weight: 700; color: #880e4f;
        border-bottom: 2px solid #c2185b; padding-bottom: 0.3rem;
        margin: 1.5rem 0 1rem;
    }
    .zone-title {
        font-weight: 700; color: #ad1457; font-size: 1rem; margin-top: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="guarnit-header">
    <h1>🏟️ El Guarnit del Carrer Papin 2026</h1>
    <p>L'Olimpíada Popular de Barcelona de 1936 — imaginant com hauria sigut</p>
</div>
""", unsafe_allow_html=True)

section_accent(0)
st.markdown('<div class="section-title">La idea</div>', unsafe_allow_html=True)
st.markdown("""
El **18 de juliol de 1936** Barcelona havia d'acollir la inauguració de l'**Olimpíada Popular**: una gran trobada internacional contra el feixisme i la guerra, pensada com a alternativa a les Olimpíades de Berlín. Una festa de la cultura i de l'esport popular que, malauradament, el cop d'estat va impedir que es celebrés.

El guarnit del Carrer Papin ens vol portar a aquell moment històric per imaginar com hauria sigut aquella inauguració que mai va tenir lloc.
""")

st.markdown("""
<div class="info-box">
<strong>Dimensions del carrer:</strong> 24 m de llargada × 8 m d'amplada = 192 m²<br>
<strong>Contacte de la comissió:</strong> Maica — 625 909 879
</div>
""", unsafe_allow_html=True)

section_accent(1)
st.markdown('<div class="section-title">El recorregut visual</div>', unsafe_allow_html=True)
st.markdown("""
En entrar i recórrer el carrer, trobareu quatre zones ben diferenciades:
""")

st.markdown("""
<div class="material-card">
<div class="zone-title">🚪 La portalada</div>
Elements introductoris i publicitaris de l'Olimpíada Popular: el cartell oficial, un avió amb la publicitat de la competició i una guita — figura de cultura popular present als grans esdeveniments festius i esportius de l'època.
</div>

<div class="material-card">
<div class="zone-title">🏟️ La paret lateral</div>
Les grades de l'estadi plenes de públic dels anys 30, amb esportistes de països i regions participants i banderoles dels esports de la competició.
</div>

<div class="material-card">
<div class="zone-title">☁️ El sostre</div>
El cel de l'estadi: coloms blancs que es llançaven en les inauguracions de les Olimpíades, i peces de confeti gegant amb els colors de l'Olimpíada Popular.
</div>

<div class="material-card">
<div class="zone-title">💣 La contraportalada</div>
L'inici de la guerra. Un mur mig derruït on hi ha enganxat el cartell de la inauguració de l'Olimpíada Popular, envoltat de bombes i coloms blancs morts.
</div>
""", unsafe_allow_html=True)

section_accent(2)
st.markdown('<div class="section-title">Com s\'ha construït</div>', unsafe_allow_html=True)
st.markdown("""
Tot el guarnit s'ha fet amb materials reciclats i reutilitzats. Aquí teniu el detall de cadascun:
""")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**📦 Cartró**")
    st.markdown("""
- Cartró fi de capses → peces dels coloms i confeti de l'estadi
- Cartró de dues capes → plafons de la barra (aspecte de bar esportiu)
- 7 capses de nevera → base de les grades de l'estadi
- Un rotlle de cartronet → públic de les grades (dibuixat i pintat)
- 8 planxes de cartró ploma (1×1,20 m) → peces de l'avió
- Un tub de cartró de 3 m (trobat al carrer) → coll de la guita
""")

    st.markdown("**🧱 Tetrabricks**")
    st.markdown("660 tetrabricks → el mur i els trossos de mur derruït de la contraportalada")

    st.markdown("**🪵 Fusta**")
    st.markdown("""
- 4 llistons (1×1×200 cm) → barres que sostenen les ales de l'avió
- 8 llistons (5×5×240 cm), alguns reutilitzats d'altres anys → estructura del cartell
- Fullola de 5 mm → figures del cartell i lletres
- 1 palet → base de la guita
""")

with col2:
    st.markdown("**🧵 Teles**")
    st.markdown("""
- Tela pintada blava → simula el cel de l'estadi
- Tela verda → cos de la guita
- 9 llençols vells → banderoles amb els logos dels esports
""")

    st.markdown("**🔧 Altres materials**")
    st.markdown("""
- **Malla de galliner** → dona forma al cos de la guita
- **Paper maixé** → cap de la guita, reforç dels coloms, folrat de l'avió, marcs dels plafons de la barra i empalme de les peces frontals de les grades
- **Pintura ecològica** → tot el color del guarnit
""")

section_accent(3)
st.markdown('<div class="section-title">El procés de construcció</div>', unsafe_allow_html=True)
st.markdown("Algunes fotos del treball de la comissió durant els mesos de preparació:")

GUARNIT_PHOTOS = [
    ("assets/guarnit/papin_01.jpeg", "Pintant les figures del públic de les grades — esportistes de les delegacions participants"),
    ("assets/guarnit/papin_03.jpeg", "Treballant les banderoles dels esports i els elements de la portalada"),
    ("assets/guarnit/papin_07.jpeg", "Pintant la tela blava del cel de l'estadi amb els núvols"),
    ("assets/guarnit/papin_09.jpeg", "Coloms de cartró per al sostre — un dels elements del cel de l'estadi"),
    ("assets/guarnit/papin_10.jpeg", "Muntant el mur de 660 tetrabricks de la contraportalada"),
    ("assets/guarnit/papin_12.jpeg", "El mur de tetrabricks ja col·locat, llest per pintar"),
]

import os
cols_per_row = 2
for i in range(0, len(GUARNIT_PHOTOS), cols_per_row):
    cols = st.columns(cols_per_row)
    for j, col in enumerate(cols):
        idx = i + j
        if idx < len(GUARNIT_PHOTOS):
            fpath, caption = GUARNIT_PHOTOS[idx]
            with col:
                if os.path.isfile(fpath):
                    st.image(fpath, use_container_width=True)
                st.markdown(
                    f"<div style='text-align:center;color:#555;font-size:0.82rem;"
                    f"font-style:italic;padding:0.2rem 0 0.8rem'>{caption}</div>",
                    unsafe_allow_html=True,
                )

section_accent(4)
st.markdown('<div class="section-title">La comissió</div>', unsafe_allow_html=True)
st.markdown("""
Tot el guarnit l'han fet els **veïns i veïnes del Carrer Papin**, treballant des del març fins a la festa. Cap professional, cap pressupost gran: només creativitat, treball en equip i molt de reciclatge.

- **Instagram:** [@comissiopapin](https://www.instagram.com/comissiopapin)
- **Punt de trobada:** Orfeó de Sants (C. Miquel Àngel, 54)
- La comissió va renéixer el 2014 i cada any ha crescut més.
""")

st.markdown("---")
st.caption("Guarnit del Carrer Papin · Festa Major de Sants 2026")
