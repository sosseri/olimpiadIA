import streamlit as st
import uuid
import html
import re
import base64
import os
from io import BytesIO
from gtts import gTTS
import streamlit.components.v1 as components

from lib.chatbot import load_program, generate_response

IMAGES_DIR = "assets/images"

def _render_bot_message(content: str):
    """Split bot content on [IMATGE:file] tags and render text + images."""
    parts = re.split(r'(\[IMATGE:[^\]]+\])', content)
    for part in parts:
        m = re.match(r'\[IMATGE:([^\]]+)\]', part)
        if m:
            fname = m.group(1).strip()
            fpath = os.path.join(IMAGES_DIR, fname)
            if os.path.isfile(fpath):
                st.image(fpath, use_container_width=True)
        else:
            text = part.strip()
            if text:
                st.markdown(
                    f"<div class='chat-bubble-bot'>🤖 {html.escape(text)}</div>",
                    unsafe_allow_html=True,
                )

def _strip_image_tags(text: str) -> str:
    return re.sub(r'\[IMATGE:[^\]]+\]', '', text).strip()

st.set_page_config(page_title="Xat amb PapinIA", page_icon="💬", layout="centered")

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

# --- CSS ---
st.markdown("""
<style>
    .chat-header {
        background: linear-gradient(135deg, #c62828 0%, #d84315 50%, #f9a825 100%);
        border-radius: 16px; padding: 1.5rem; text-align: center; color: #fff;
        margin-bottom: 1.5rem; box-shadow: 0 2px 10px rgba(0,0,0,0.15);
    }
    .chat-header h1 { margin: 0; font-size: 1.5rem; }
    .chat-header p { margin: 0.3rem 0 0; font-size: 0.95rem; opacity: 0.9; }
    .chat-bubble-user {
        background: #e1f5fe; padding: 0.7rem 1rem; border-radius: 16px;
        margin: 0.4rem 0; max-width: 85%;
        margin-left: auto; text-align: right;
    }
    .chat-bubble-bot {
        background: #fff3e0; padding: 0.7rem 1rem; border-radius: 16px;
        margin: 0.4rem 0; max-width: 85%;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="chat-header">
    <h1>💬 Xat amb PapinIA</h1>
    <p>La Intel·ligència Artificial del Carrer Papin</p>
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
