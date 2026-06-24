import streamlit as st
import os
import json

st.set_page_config(page_title="Arxiu fotogràfic", page_icon="📸", layout="centered")

st.markdown("""
<style>
    .arxiu-header {
        background: linear-gradient(135deg, #37474f 0%, #455a64 50%, #546e7a 100%);
        border-radius: 16px; padding: 1.5rem; text-align: center; color: #fff;
        margin-bottom: 1.5rem; box-shadow: 0 2px 10px rgba(0,0,0,0.15);
    }
    .arxiu-header h1 { margin: 0; font-size: 1.5rem; }
    .arxiu-header p { margin: 0.3rem 0 0; font-size: 0.95rem; opacity: 0.9; }
    .img-caption {
        text-align: center; color: #555; font-size: 0.85rem;
        padding: 0.3rem 0 0.2rem; font-style: italic;
    }
    .img-source {
        text-align: center; color: #999; font-size: 0.75rem;
        padding: 0 0 1rem;
    }
    .section-title {
        font-size: 1.1rem; font-weight: 700; color: #37474f;
        border-bottom: 2px solid #546e7a; padding-bottom: 0.3rem;
        margin: 1.5rem 0 1rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="arxiu-header">
    <h1>📸 Arxiu fotogràfic</h1>
    <p>Imatges de l'Olimpíada Popular de 1936 i la Festa Major de Sants</p>
</div>
""", unsafe_allow_html=True)

IMAGES_DIR = "assets/images"
METADATA_PATH = "data/images_metadata.json"

# Load historical images metadata
historical_images = []
if os.path.isfile(METADATA_PATH):
    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        historical_images = json.load(f)

SOURCE_LABELS = {
    "wanderer.es": "wanderer.es",
    "beteve.cat": "betevé",
    "noubarrisperlarepublica.org": "Nou Barris per la República",
    "patrimoni.gencat.cat": "Arxiu Nacional de Catalunya",
}

SOURCE_URLS = {
    "wanderer.es": "https://www.wanderer.es/barcelona-la-olimpiada-popular-que-quiso-derrotar-a-hitler/",
    "beteve.cat": "https://beteve.cat/va-passar-aqui/olimpiada-popular-cadci-1936/",
    "noubarrisperlarepublica.org": "https://noubarrisperlarepublica.org/cas/herramientas-republicanas/cultura-cas/la-olimpiada-popular-del-36/",
    "patrimoni.gencat.cat": "https://patrimoni.gencat.cat/es/catalunyapaisdarxius/recurso-digital/recurso/document/programa-de-lolimpiada-popular-de-barcelona/",
}

# --- Historical images section ---
if historical_images:
    st.markdown('<div class="section-title">🏟️ L\'Olimpíada Popular de Barcelona, 1936</div>', unsafe_allow_html=True)
    st.markdown("Imatges històriques relacionades amb l'Olimpíada Popular i el seu context. Fes clic a la font per veure l'article original.")

    cols_per_row = 2
    for i in range(0, len(historical_images), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            idx = i + j
            if idx < len(historical_images):
                meta = historical_images[idx]
                fpath = os.path.join(IMAGES_DIR, meta["file"])
                source_site = meta.get("source_site", "")
                source_label = SOURCE_LABELS.get(source_site, source_site)
                source_url = SOURCE_URLS.get(source_site, meta.get("source_url", ""))

                with col:
                    if os.path.isfile(fpath):
                        st.image(fpath, use_container_width=True)
                    st.markdown(f"<div class='img-caption'>{meta['caption']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='img-source'>Font: <a href='{source_url}' target='_blank'>{source_label}</a></div>", unsafe_allow_html=True)

# --- Festa Major / Carrer Papin section ---
st.markdown('<div class="section-title">🎉 Festa Major de Sants — Carrer Papin</div>', unsafe_allow_html=True)

festa_images = []
FESTA_DIR = "assets/festa"
if os.path.isdir(FESTA_DIR):
    festa_images = sorted([
        f for f in os.listdir(FESTA_DIR)
        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))
    ])

if festa_images:
    cols_per_row = 2
    for i in range(0, len(festa_images), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            idx = i + j
            if idx < len(festa_images):
                fname = festa_images[idx]
                fpath = os.path.join(FESTA_DIR, fname)
                caption = fname.replace("_", " ").rsplit(".", 1)[0]
                with col:
                    st.image(fpath, use_container_width=True)
                    st.markdown(f"<div class='img-caption'>{caption}</div>", unsafe_allow_html=True)
else:
    st.info(
        "Aquí apareixeran les fotos de la festa i el carrer Papin. "
        "Afegeix imatges a la carpeta `assets/festa/` i es mostraran automàticament."
    )

st.markdown("---")
st.caption(
    "Si tens fotografies de la festa major i vols compartir-les, "
    "contacta amb la comissió del carrer Papin a Instagram: @comissiopapin"
)
