import base64
import os

import streamlit as st

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ESPORTS_DIR = os.path.join(ROOT_DIR, "assets", "esports")
# Sport illustration -> corner it decorates. Each appears once, low-opacity,
# fixed to the viewport so it reads as a light background accent.
_SPORTS = ["Ciclisme.png", "Natacio.png", "Boxa.png", "Gimnastica.png", "Escacs.png"]
_POSITIONS = [
    ("bottom: 2%; right: 1%;", "rotate(0deg)"),
    ("top: 30%; left: -2%;", "rotate(0deg)"),
    ("bottom: 30%; right: -1%;", "scaleX(-1)"),
    ("top: 55%; right: 2%;", "rotate(0deg)"),
    ("bottom: 3%; left: 1%;", "scaleX(-1)"),
]


@st.cache_data
def _encoded():
    out = []
    for fname in _SPORTS:
        fpath = os.path.join(ESPORTS_DIR, fname)
        if os.path.isfile(fpath):
            with open(fpath, "rb") as fh:
                out.append(base64.b64encode(fh.read()).decode())
        else:
            out.append(None)
    return out


def add_background(count=3, opacity=0.08, size="150px"):
    """Scatter `count` sport PNGs as fixed, faint background accents."""
    encoded = _encoded()
    layers = []
    for i in range(min(count, len(_SPORTS))):
        b64 = encoded[i]
        if not b64:
            continue
        pos, transform = _POSITIONS[i]
        layers.append(
            f"""
            <div style="position: fixed; {pos} z-index: 0; pointer-events: none;
                        opacity: {opacity}; transform: {transform};
                        width: {size}; height: {size};
                        background-image: url('data:image/png;base64,{b64}');
                        background-size: contain; background-repeat: no-repeat;">
            </div>"""
        )
    if layers:
        st.markdown("".join(layers), unsafe_allow_html=True)


# Sides alternate so consecutive sections don't stack their accents.
_SIDES = [
    ("right: -10px;", "scaleX(-1)"),
    ("left: -10px;", "rotate(0deg)"),
]


def section_accent(index, opacity=0.10, size="130px"):
    """Anchor one faint sport PNG behind the next content section.

    The image scrolls with the section it precedes. `index` selects which
    sport (cycled) and which side, so call once per section with i=0,1,2,...
    """
    encoded = _encoded()
    b64 = encoded[index % len(_SPORTS)]
    if not b64:
        return
    side, transform = _SIDES[index % len(_SIDES)]
    st.markdown(
        f"""
        <div style="position: relative; height: 0; overflow: visible; z-index: 0;">
            <div style="position: absolute; top: -10px; {side}
                        pointer-events: none; opacity: {opacity}; transform: {transform};
                        width: {size}; height: {size};
                        background-image: url('data:image/png;base64,{b64}');
                        background-size: contain; background-repeat: no-repeat;">
            </div>
        </div>""",
        unsafe_allow_html=True,
    )


def nav_bar():
    """Mobile-first in-body navigation: a 2-column grid of full-width page links.

    Call at the top of every page so users don't depend on the sidebar '>>' toggle.
    """
    import streamlit as st

    links = [
        ("strlt_app.py", "![🏠](https://fonts.gstatic.com/s/e/notoemoji/17.0/1f3e0/72.png) Inici"),
        ("pages/1_xatbot.py", "![💬](https://fonts.gstatic.com/s/e/notoemoji/17.0/1f4ac/72.png) Xatbot"),
        ("pages/2_programa.py", "![📅](https://fonts.gstatic.com/s/e/notoemoji/17.0/1f4c5/72.png) Programa"),
        ("pages/3_olimpiada.py", "![🏟️](https://fonts.gstatic.com/s/e/notoemoji/17.0/1f3df_fe0f/72.png)  Olimpíada"),
        ("pages/5_guarnit_papin.py", "![🎨](https://fonts.gstatic.com/s/e/notoemoji/17.0/1f3a8/72.png) Guarnit"),
        ("pages/4_arxiu.py", "![📸](https://fonts.gstatic.com/s/e/notoemoji/17.0/1f4f8/72.png) Arxiu"),
        ("pages/6_festa_major.py", "![🎭](https://fonts.gstatic.com/s/e/notoemoji/17.0/1f3ad/72.png) Festa Major"),
        ("pages/7_participar.py", "![🙋](https://fonts.gstatic.com/s/e/notoemoji/17.0/1f64b/72.png) Participar"),
    ]

    cols = st.columns(2)
    for i, (target, label) in enumerate(links):
        with cols[i % 2]:
            st.page_link(target, label=label, use_container_width=True)
    st.markdown("<hr style='margin:0.6rem 0 1rem; opacity:0.25;'>", unsafe_allow_html=True)
