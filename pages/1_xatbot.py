import streamlit as st
from gtts import gTTS
from io import BytesIO
import base64
import re
import json
import os
import requests
import streamlit.components.v1 as components
import uuid
import html

from lib.chatbot import generate_response, load_program

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
IMAGES_DIR = os.path.join(ROOT_DIR, "assets", "images")

_IMAGES_META = None


def _load_images_meta():
    global _IMAGES_META
    if _IMAGES_META is None:
        path = os.path.join(ROOT_DIR, "data", "images_metadata.json")
        try:
            with open(path, "r", encoding="utf-8") as f:
                _IMAGES_META = json.load(f)
        except Exception:
            _IMAGES_META = []
    return _IMAGES_META


def _fetch_image_bytes(url: str, timeout: int = 8):
    try:
        r = requests.get(url, timeout=timeout)
        if r.status_code == 200:
            return r.content
    except Exception:
        return None
    return None


def _get_image_bytes_by_name(fname: str):
    fpath = os.path.join(IMAGES_DIR, fname)
    if os.path.isfile(fpath):
        try:
            with open(fpath, "rb") as fh:
                return fh.read()
        except Exception:
            return None
    for meta in _load_images_meta():
        if meta.get("file") == fname:
            url = meta.get("source_url")
            if url:
                return _fetch_image_bytes(url)
    return None


def _find_best_image_filename(requested: str):
    tokens_req = re.findall(r"[a-z0-9]+", os.path.splitext(requested)[0].lower())
    tokens_req = [t for t in tokens_req if len(t) > 2]
    if not tokens_req:
        return None
    best = None
    best_score = 0
    for meta in _load_images_meta():
        fname = meta.get("file", "")
        tokens_meta = re.findall(r"[a-z0-9]+", os.path.splitext(fname)[0].lower())
        tokens_meta = [t for t in tokens_meta if len(t) > 2]
        if not tokens_meta:
            continue
        overlap = len(set(tokens_req) & set(tokens_meta))
        if overlap > best_score:
            best_score = overlap
            best = fname
    return best if best_score > 0 else None


def _resolve_image_bytes(ref: str):
    fname = ref.strip().strip("\"'[]() ")
    if not fname:
        return None, None
    img_bytes = _get_image_bytes_by_name(fname)
    used_fname = fname
    if not img_bytes:
        candidate = _find_best_image_filename(fname)
        if candidate:
            used_fname = candidate
            img_bytes = _get_image_bytes_by_name(candidate)
    return img_bytes, used_fname


def _extract_image_references(text: str):
    refs = []
    seen = set()
    tag_pattern = re.compile(r'\[(?:IMATGE|IMAGE|IMAGEN):([^\]]+)\]', flags=re.IGNORECASE)
    for match in tag_pattern.finditer(text):
        ref = match.group(1).strip().strip("\"'[]() ")
        if ref and ref not in seen:
            refs.append(ref)
            seen.add(ref)
    bare_pattern = re.compile(
        r'(?i)(?:\b(?:imatge|image|imagen|foto|photo|imatges|images)\s*[:\-]?\s*|\b)'
        r'([A-Za-z0-9_./ -]+?\.(?:jpe?g|png|gif|webp|bmp|svg))'
    )
    for match in bare_pattern.finditer(text):
        ref = match.group(1).strip().strip("\"'[]() ")
        if ref and ref not in seen:
            refs.append(ref)
            seen.add(ref)
    return refs


def _render_bot_message(content: str):
    pattern = re.compile(r'(\[(?:IMATGE|IMAGE|IMAGEN):[^\]]+\])', flags=re.IGNORECASE)
    parts = pattern.split(content)
    rendered_image_refs = set()

    for part in parts:
        image_refs = _extract_image_references(part)
        for ref in image_refs:
            if ref in rendered_image_refs:
                continue
            rendered_image_refs.add(ref)
            img_bytes, used_fname = _resolve_image_bytes(ref)
            if img_bytes:
                st.image(img_bytes, use_container_width=True)
                if used_fname != ref:
                    st.caption(f"Mostrat: {used_fname}")
                continue
            st.markdown("*(Imatge no disponible)*")

        if re.match(r'\[(?:IMATGE|IMAGE|IMAGEN):([^\]]+)\]', part, flags=re.IGNORECASE):
            continue

        text = part.strip()
        if text:
            st.markdown(f"<div class='chat-bubble-bot'>🤖 {html.escape(text)}</div>", unsafe_allow_html=True)


@st.cache_data
def get_program():
    return load_program(os.path.join(ROOT_DIR, "data", "programa.json"))


def reset_conversation():
    st.session_state["messages"] = []
    st.session_state["processing"] = False
    st.session_state["user_input"] = ""
    st.rerun()


st.set_page_config(
    page_title="Xat amb PapinIA",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="expanded",
)

from lib.decor import add_background, nav_bar

add_background(count=2)
nav_bar()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "processing" not in st.session_state:
    st.session_state.processing = False
if "play_request" not in st.session_state:
    st.session_state.play_request = None
if "user_input" not in st.session_state:
    st.session_state.user_input = ""


def _strip_image_tags(text: str) -> str:
    return re.sub(r'\[(?:IMATGE|IMAGE|IMAGEN):[^\]]+\]', '', text, flags=re.IGNORECASE).strip()


def generate_audio_base64(text: str) -> str:
    clean_text = _strip_image_tags(text)
    tts = gTTS(text=clean_text, lang='ca')
    buf = BytesIO()
    tts.write_to_fp(buf)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode()


def process_message(user_message: str):
    if not user_message.strip() or st.session_state.processing:
        return

    st.session_state.processing = True
    st.session_state.messages.append({
        "id": uuid.uuid4().hex,
        "role": "user",
        "content": user_message.strip(),
    })

    program_data = get_program()
    history = [
        {"role": "assistant" if m["role"] == "bot" else m["role"], "content": m["content"]}
        for m in st.session_state.messages[:-1]
    ]

    bot_response = "❌ Error: no response"
    try:
        with st.spinner("⏳ Processant..."):
            bot_response = generate_response(user_message.strip(), history, program_data)
    except Exception as e:
        bot_response = f"❌ Error: {str(e)}"

    st.session_state.messages.append({
        "id": uuid.uuid4().hex,
        "role": "bot",
        "content": bot_response,
        "audio_b64": None,
    })
    st.session_state.processing = False


def send_callback():
    text = st.session_state.get("user_input", "").strip()
    if not text:
        return
    process_message(text)
    st.session_state.user_input = ""


def send_suggested(q: str):
    process_message(q)


st.markdown("""
<style>
    :root {
        --op-blue: #1E3FD0;
        --op-red: #F0281E;
        --op-yellow: #F5CE18;
        --op-maroon: #3B0D0D;
        --op-cream: #FBF7EC;
    }
    body { background-color: var(--op-cream); font-family: 'Helvetica Neue', sans-serif; }
    .stApp { background-color: var(--op-cream); }
    .main-header {
        background: linear-gradient(135deg, var(--op-blue) 0%, var(--op-red) 100%);
        border-radius: 16px; padding: 2rem 1.5rem; text-align: center; color: #fff;
        margin-bottom: 1.5rem; box-shadow: 0 4px 16px rgba(30,63,208,0.25);
        border-bottom: 6px solid var(--op-yellow);
    }
    .main-header h1 { margin: 0; font-size: 1.9rem; letter-spacing: 0.5px; }
    .main-header h2 { margin-top: 0.4rem; font-weight: 400; color: #ffe; opacity: 0.95; font-size: 1.05rem; }
    .badge { display: inline-block; margin-top: 0.9rem; padding: 0.35rem 0.9rem; background: var(--op-yellow); color: var(--op-maroon); border-radius: 12px; font-size: 0.9rem; font-weight: 700; }
    .sport-strip { display:flex; justify-content:center; gap:6px; margin: -0.5rem 0 1.2rem; }
    .sport-strip img { height: 74px; width:auto; }
    .chat-bubble-user { background: #dbe4ff; color: var(--op-maroon); padding: 0.7rem 1rem; border-radius: 16px 16px 4px 16px; margin: 0.4rem 0; max-width: 80%; align-self: flex-end; margin-left: auto; border-right: 4px solid var(--op-blue); }
    .chat-bubble-bot { background: #fff; color: var(--op-maroon); padding: 0.7rem 1rem; border-radius: 16px 16px 16px 4px; margin: 0.4rem 0; max-width: 80%; align-self: flex-start; margin-right: auto; border-left: 4px solid var(--op-red); box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
    .small-note { color: #666; font-size: 0.9rem; }
    .play-button { border: none; background: transparent; cursor: pointer; font-size: 1.1rem; }
    .input-row { display:flex; gap:8px; align-items:center; }
    .send-btn { padding:8px 12px; border-radius:8px; }
    .suggestions { margin-top: 0.6rem; display:flex; flex-wrap:wrap; gap:0.4rem; }
    .stButton>button { border-radius: 12px; border: 1.5px solid var(--op-blue); color: var(--op-blue); font-weight: 600; }
    .stButton>button:hover { background: var(--op-blue); color: #fff; border-color: var(--op-blue); }
</style>
""", unsafe_allow_html=True)

poster_path = os.path.join(ROOT_DIR, "assets", "olimpiada_popular_poster.jpeg")
_poster_b64 = ""
if os.path.isfile(poster_path):
    with open(poster_path, "rb") as fh:
        _poster_b64 = base64.b64encode(fh.read()).decode()


@st.cache_data
def _sport_strip_html():
    sports = ["Ciclisme.png", "Natacio.png", "Boxa.png", "Gimnastica.png", "Escacs.png"]
    imgs = []
    for fname in sports:
        fpath = os.path.join(ROOT_DIR, "assets", "esports", fname)
        if os.path.isfile(fpath):
            with open(fpath, "rb") as fh:
                enc = base64.b64encode(fh.read()).decode()
            imgs.append(f'<img src="data:image/png;base64,{enc}" alt="{fname}">')
    if not imgs:
        return ""
    return '<div class="sport-strip">' + "".join(imgs) + "</div>"


st.markdown("""
<div class="main-header">
    <h1>💬 Xat amb PapinIA</h1>
    <h2>La Intel·ligència Artificial del Carrer Papin</h2>
    <div class="badge">🎉 Festa Major de Sants 2026 · L'Olimpíada Popular de 1936 🎉</div>
</div>
""", unsafe_allow_html=True)

st.markdown(_sport_strip_html(), unsafe_allow_html=True)

program_data = get_program()
if st.session_state.get("pending_question"):
    q = st.session_state.pop("pending_question")
    process_message(q)

if not st.session_state.messages:
    st.markdown("### 🏟️ Benvingudes a la Festa Major de Sants!")
    st.markdown(
        "Podeu preguntar-me sobre:\n"
        "- 🏟️ El **tema** del carrer Papin: l'**Olimpíada Popular** de 1936.\n"
        "- 🎨 El **guarnit** del carrer Papin i com està fet.\n"
        "- 🏠 Els altres **carrers** que participen i les seves decoracions.\n"
        "- 📅 El **programa** d’activitats del carrer Papin i d'altres carrers.\n"
        "- 🙋‍♂️ Com **participar** a la comissió de festa major del Carrer Papin.\n"
    )

for i, msg in enumerate(st.session_state.messages):
    if msg["role"] == "user":
        st.markdown(f"<div class='chat-bubble-user'>🧑 {html.escape(msg['content'])}</div>", unsafe_allow_html=True)
    else:
        cols = st.columns([0.95, 0.05])
        with cols[0]:
            _render_bot_message(msg["content"])
        with cols[1]:
            def make_on_click(mid=msg['id']):
                def _cb():
                    st.session_state.play_request = mid
                return _cb
            st.button("🔊", key=f"play_{msg['id']}", help="Click to synthesize and play this message", on_click=make_on_click())

if st.session_state.play_request:
    play_id = st.session_state.play_request
    target = None
    for m in st.session_state.messages:
        if m['id'] == play_id and m['role'] == 'bot':
            target = m
            break

    if target is None:
        st.warning("Requested message not found.")
        st.session_state.play_request = None
    else:
        if target.get('audio_b64'):
            audio_b64 = target['audio_b64']
        else:
            with st.spinner('Generating audio...'):
                try:
                    sanitized = _strip_image_tags(target['content']).replace('*', '').replace('#', '')
                    audio_b64 = generate_audio_base64(sanitized)
                    target['audio_b64'] = audio_b64
                except Exception as e:
                    st.error(f"TTS generation failed: {e}")
                    st.session_state.play_request = None
                    audio_b64 = None

        if audio_b64:
            audio_element_id = f"audio_{target['id']}"
            status_id = f"status_{target['id']}"
            player_html = f"""
            <div style='display:flex; align-items:center; gap:12px;'>
                <div style='font-size:1.4rem;'>🔊</div>
                <div>
                    <div style='font-size:0.95rem; color:#333'> </div>
                    <div id='{status_id}' style='color:#666; font-size:0.9rem; display:none;'>Llegint...</div>
                    <audio id='{audio_element_id}' autoplay>
                        <source src='data:audio/mp3;base64,{audio_b64}' type='audio/mp3'>
                        Your browser does not support the audio element.
                    </audio>
                </div>
            </div>
            <script>
            (function() {{
                const audio = document.getElementById('{audio_element_id}');
                const status = document.getElementById('{status_id}');
                function show() {{ status.style.display = 'block'; }}
                function hide() {{ status.style.display = 'none'; }}
                audio.addEventListener('play', function() {{ show(); }});
                audio.addEventListener('ended', function() {{ hide(); }});
                audio.addEventListener('pause', function() {{ hide(); }});
                setTimeout(()=>{{ show(); }}, 50);
            }})();
            </script>
            """
            components.html(player_html, height=120)
            st.session_state.play_request = None

st.markdown("<div class='input-row'>", unsafe_allow_html=True)
cols = st.columns([4,1])
with cols[0]:
    st.text_input("Escriu el teu missatge...", key="user_input", placeholder="Escriu... i premi Envia")
with cols[1]:
    st.button("📨 Envia", key="send_button", on_click=send_callback, args=())
st.markdown("</div>", unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown("<div class='suggestions'>", unsafe_allow_html=True)
    suggestions = [
        "Quin és el tema del carrer Papin?",
        "Què va ser l'Olimpíada Popular de 1936?",
        "Quin era l'himne de l'Olimpíada Popular?",
        "Qui era Marina Ginestà?",
        "Podries explicar-me el guarnit d’aquest any?",
        "Quins són els altres carrers de la festa?",
        "Què hi ha avui al carrer Papin?",
        "Què hi ha demà al carrer Papin?",
        "Què concerts hi ha avui a la Festa Major de Sants?",
        "Com puc participar a la comissió de festes?",
    ]
    for i, q in enumerate(suggestions):
        st.button(q, key=f"sugg_{i}", on_click=send_suggested, args=(q,), use_container_width=False)
    st.markdown("</div>", unsafe_allow_html=True)

st.button("🔄 Reiniciar conversa", on_click=reset_conversation)

if st.session_state.processing:
    st.markdown("""
    <div style="display:flex; align-items:center; gap:8px; font-size:1rem; color:#444;">
        <span>🤖 Processant la pregunta</span>
        <span class="dot-anim">.</span>
        <span class="dot-anim">.</span>
        <span class="dot-anim">.</span>
    </div>
    <style>
    @keyframes blink {
        0% { opacity: 0.2; }
        20% { opacity: 1; }
        100% { opacity: 0.2; }
    }
    .dot-anim {
        animation: blink 1.4s infinite both;
        font-weight: bold;
    }
    .dot-anim:nth-child(2) { animation-delay: 0.2s; }
    .dot-anim:nth-child(3) { animation-delay: 0.4s; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
<div class='footer-note'>
    🔊 Clica l'altaveu per escoltar les respostes 🔊
</div>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.disclaimer-card{
  border-radius: 16px;
  padding: 14px 16px;
  border: 1px solid rgba(0,0,0,.08);
  background: linear-gradient(180deg, rgba(255,255,255,.7), rgba(255,255,255,.5));
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
  box-shadow: 0 8px 24px rgba(0,0,0,.06);
  margin: 8px 0 18px 0;
}
.disclaimer-title{
  display:flex; gap:.5rem; align-items:center;
  font-weight: 700; font-size: .95rem; margin: 0 0 6px 0;
}
.disclaimer-text{
  font-size: .85rem; line-height: 1.4; margin: 0;
}
@media (prefers-color-scheme: dark) {
  .disclaimer-card{
    background: linear-gradient(180deg, rgba(255,255,255,.06), rgba(255,255,255,.03));
    border: 1px solid rgba(255,255,255,.18);
    box-shadow: 0 8px 24px rgba(0,0,0,.35);
    position: sticky; bottom: 8px; z-index: 999;
  }
}
</style>
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
