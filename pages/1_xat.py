import streamlit as st
import uuid
import html
import re
import base64
import os
import json
import requests
from io import BytesIO
from gtts import gTTS
import streamlit.components.v1 as components

from lib.chatbot import load_program, generate_response

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
IMAGES_DIR = os.path.join(ROOT_DIR, "assets", "images")


_IMAGES_META = None


def _load_images_meta():
    global _IMAGES_META
    if _IMAGES_META is None:
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "images_metadata.json"))
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
    # Check local file first
    fpath = os.path.join(IMAGES_DIR, fname)
    if os.path.isfile(fpath):
        try:
            with open(fpath, "rb") as fh:
                return fh.read()
        except Exception:
            return None

    # Look up metadata for remote source_url
    meta_list = _load_images_meta()
    for meta in meta_list:
        if meta.get("file") == fname:
            url = meta.get("source_url")
            if url:
                return _fetch_image_bytes(url)
    return None


def _find_best_image_filename(requested: str):
    """Try to find the best matching filename from metadata for a requested name."""
    # split on underscores and non-alphanumeric characters (avoid keeping underscores as part of tokens)
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
        # count token overlap
        overlap = len(set(tokens_req) & set(tokens_meta))
        if overlap > best_score:
            best_score = overlap
            best = fname
    # require at least one overlapping token
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
    """Return image filenames from exact tags or plain filename mentions."""
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
    """Split bot content on image tags and render actual images instead of raw filenames."""
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
            st.markdown(
                f"<div class='chat-bubble-bot'>🤖 {html.escape(text)}</div>",
                unsafe_allow_html=True,
            )

def _strip_image_tags(text: str) -> str:
    return re.sub(r'\[(?:IMATGE|IMAGE|IMAGEN):[^\]]+\]', '', text, flags=re.IGNORECASE).strip()

st.set_page_config(page_title="Xat amb PapinIA", page_icon="💬", layout="centered")

from lib.decor import add_background
add_background(count=2)

# --- Session state ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = None
if "processing" not in st.session_state:
    st.session_state.processing = False
if "play_request" not in st.session_state:
    st.session_state.play_request = None
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

@st.cache_data
def get_program():
    return load_program()

program_data = get_program()

# --- TTS ---
def generate_audio_base64(text: str) -> str:
    tts = gTTS(text=text, lang='ca')
    buf = BytesIO()
    tts.write_to_fp(buf)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode()

# --- Process message ---
def process_message(user_message: str):
    if not user_message.strip() or st.session_state.processing:
        return
    st.session_state.processing = True

    st.session_state.messages.append({
        "id": uuid.uuid4().hex,
        "role": "user",
        "content": user_message.strip()
    })

    conversation_history = [
        {"role": m["role"] if m["role"] != "bot" else "assistant", "content": m["content"]}
        for m in st.session_state.messages[:-1]
    ]

    bot_response = "Error: sense resposta"
    try:
        with st.spinner("Pensant... la primera interacció pot trigar fins a 1 minut"):
            bot_response = generate_response(
                user_message.strip(),
                conversation_history,
                program_data
            )
    except Exception as e:
        bot_response = f"Hi ha hagut un error: {e}"

    st.session_state.messages.append({
        "id": uuid.uuid4().hex,
        "role": "bot",
        "content": bot_response,
        "audio_b64": None
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

def reset_conversation():
    st.session_state.messages = []
    st.session_state.conversation_id = None
    st.session_state.processing = False
    st.session_state.user_input = ""
    st.rerun()

# --- Load poster image as base64 ---
import base64 as _b64
_poster_b64 = ""
_poster_path = "assets/olimpiada_popular_poster.jpeg"
if os.path.isfile(_poster_path):
    with open(_poster_path, "rb") as _f:
        _poster_b64 = _b64.b64encode(_f.read()).decode()

# --- CSS ---
st.markdown("""
<style>
    .chat-header {
        background: #ffffff;
        border-radius: 16px;
        border: 2px solid #e8e8e8;
        box-shadow: 0 2px 12px rgba(0,0,0,0.07);
        margin-bottom: 1.5rem;
        position: relative; overflow: hidden; min-height: 120px;
        display: flex; align-items: center;
    }
    .chat-header-text {
        position: relative; z-index: 2;
        padding: 1.5rem 1rem 1.5rem 1.8rem;
        flex: 1;
    }
    .chat-header h1 {
        margin: 0; font-size: 1.6rem; color: #1a1a1a; font-weight: 800;
        letter-spacing: -0.5px;
    }
    .chat-header p {
        margin: 0.3rem 0 0; font-size: 0.95rem; color: #555;
    }
    .chat-header-accent {
        display: block; width: 5px; height: 100%;
        position: absolute; left: 0; top: 0;
        background: linear-gradient(180deg, #F0281E 0%, #F5CE18 100%);
        border-radius: 16px 0 0 16px;
    }
    .chat-header-poster-wrap {
        flex-shrink: 0;
        height: 140px;
        position: relative;
        display: flex; align-items: center;
    }
    .chat-header-poster-wrap::before {
        content: '';
        position: absolute; left: 0; top: 0; bottom: 0; width: 48px;
        background: linear-gradient(to right, #ffffff, transparent);
        z-index: 2; pointer-events: none;
    }
    .chat-header-poster {
        height: 140px;
        display: block;
        pointer-events: none;
    }
    .chat-bubble-user {
        background: #fff5f5; color: #1a1a1a; padding: 0.7rem 1rem;
        border-radius: 16px 16px 4px 16px;
        margin: 0.4rem 0; max-width: 85%; border-right: 3px solid #F0281E;
        margin-left: auto; text-align: right;
    }
    .chat-bubble-bot {
        background: #fff; color: #1a1a1a; padding: 0.7rem 1rem;
        border-radius: 16px 16px 16px 4px;
        margin: 0.4rem 0; max-width: 85%; border-left: 3px solid #1a1aaa;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }
</style>
""", unsafe_allow_html=True)

_poster_img_tag = (
    f'<div class="chat-header-poster-wrap"><img class="chat-header-poster" src="data:image/jpeg;base64,{_poster_b64}" alt=""></div>'
    if _poster_b64 else ""
)
st.markdown(f"""
<div class="chat-header">
    <span class="chat-header-accent"></span>
    <div class="chat-header-text">
        <h1>💬 Xat amb PapinIA</h1>
        <p>La Intel·ligència Artificial del Carrer Papin</p>
    </div>
    {_poster_img_tag}
</div>
""", unsafe_allow_html=True)

# --- Welcome ---
if not st.session_state.messages:
    st.markdown("### Benvingudes a la Festa Major de Sants!")
    st.markdown(
        "Podeu preguntar-me sobre:\n"
        "- 🏟️ El **tema** del carrer Papin: l'Olimpíada Popular de 1936\n"
        "- 📅 El **programa** d'activitats del carrer i de la festa\n"
        "- 🎨 El **guarnit** i com està fet\n"
        "- 🏠 Els altres **carrers** que participen\n"
        "- 🙋 Com **participar** a la comissió de festes\n"
    )

# --- Chat messages ---
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f"<div class='chat-bubble-user'>🧑 {html.escape(msg['content'])}</div>",
            unsafe_allow_html=True,
        )
    else:
        cols = st.columns([0.93, 0.07])
        with cols[0]:
            _render_bot_message(msg["content"])
        with cols[1]:
            def make_on_click(mid=msg["id"]):
                def _cb():
                    st.session_state.play_request = mid
                return _cb
            st.button("🔊", key=f"play_{msg['id']}", on_click=make_on_click())

# --- Audio playback ---
if st.session_state.play_request:
    play_id = st.session_state.play_request
    target = next((m for m in st.session_state.messages if m["id"] == play_id and m["role"] == "bot"), None)
    if target:
        if not target.get("audio_b64"):
            with st.spinner("Generant àudio..."):
                try:
                    sanitized = _strip_image_tags(target["content"]).replace("*", "").replace("#", "")
                    target["audio_b64"] = generate_audio_base64(sanitized)
                except Exception as e:
                    st.error(f"Error TTS: {e}")
        if target.get("audio_b64"):
            audio_id = f"audio_{target['id']}"
            components.html(f"""
            <audio id="{audio_id}" autoplay>
                <source src="data:audio/mp3;base64,{target['audio_b64']}" type="audio/mp3">
            </audio>
            """, height=50)
    st.session_state.play_request = None

# --- Input ---
cols = st.columns([4, 1])
with cols[0]:
    st.text_input("Escriu el teu missatge...", key="user_input", placeholder="Escriu i prem Envia")
with cols[1]:
    st.button("📨 Envia", on_click=send_callback)

# --- Suggested questions ---
if not st.session_state.messages:
    suggestions = [
        "Quin és el tema del carrer Papin?",
        "Què va ser l'Olimpíada Popular de 1936?",
        "Què hi ha avui al carrer Papin?",
        "Quins són els altres carrers de la festa?",
        "Com puc participar a la comissió?",
        "Què hi ha demà?",
    ]
    cols = st.columns(2)
    for i, q in enumerate(suggestions):
        with cols[i % 2]:
            st.button(q, key=f"sugg_{i}", on_click=send_suggested, args=(q,))

st.button("🔄 Reiniciar conversa", on_click=reset_conversation)

st.markdown("---")
st.caption("🔊 Clica l'altaveu per escoltar les respostes")
