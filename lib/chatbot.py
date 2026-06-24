import os
import json
import re
import groq
from datetime import date, datetime
from dotenv import load_dotenv
from lib.rag import retrieve, format_context

load_dotenv()

# Streamlit Cloud stores secrets in st.secrets — fall back to env var for local/Render
try:
    import streamlit as st
    if "GROQ_API_KEY" in st.secrets:
        os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
except Exception:
    pass

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

_client = None
def _get_client():
    global _client
    if _client is None:
        key = os.getenv("GROQ_API_KEY")
        if not key:
            raise ValueError("Cal configurar la variable d'entorn GROQ_API_KEY.")
        _client = groq.Client(api_key=key)
    return _client


def load_program(path="data/programa.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _program_summary_for_date(program_data, target_date_str):
    lines = []
    for day in program_data.get("program", []):
        if day["date"] == target_date_str:
            lines.append(f"\n📅 {day['day_label']} — Carrer Papin:")
            for ev in day["events"]:
                lines.append(f"  {ev['time']} — {ev['title']}: {ev.get('description', '')}")
    for day in program_data.get("unitari", []):
        if day["date"] == target_date_str:
            lines.append(f"\n📅 {day['day_label']} — Actes Unitaris:")
            for ev in day["events"]:
                lines.append(f"  {ev['time']} — {ev['title']}")
    return "\n".join(lines) if lines else None


def _full_program_text(program_data):
    lines = ["Programa complet del Carrer Papin:"]
    for day in program_data.get("program", []):
        lines.append(f"\n📅 {day['day_label']}:")
        for ev in day["events"]:
            loc = f" ({ev['location']})" if ev.get("location") and ev["location"] != "Carrer Papin" else ""
            lines.append(f"  {ev['time']} — {ev['title']}{loc}")
            if ev.get("description"):
                lines.append(f"         {ev['description']}")
    lines.append("\n\nActes Unitaris:")
    for day in program_data.get("unitari", []):
        lines.append(f"\n📅 {day['day_label']}:")
        for ev in day["events"]:
            lines.append(f"  {ev['time']} — {ev['title']}")
    return "\n".join(lines)


def _kids_events(program_data):
    lines = ["Activitats per a nens/famílies al Carrer Papin:"]
    for day in program_data.get("program", []):
        day_events = [ev for ev in day["events"] if ev.get("for_kids")]
        if day_events:
            lines.append(f"\n📅 {day['day_label']}:")
            for ev in day_events:
                lines.append(f"  {ev['time']} — {ev['title']}")
    return "\n".join(lines)


def _events_by_type(program_data, event_type):
    lines = [f"Activitats de tipus '{event_type}' al Carrer Papin:"]
    for day in program_data.get("program", []):
        day_events = [ev for ev in day["events"] if ev.get("type") == event_type or event_type in ev.get("tags", [])]
        if day_events:
            lines.append(f"\n📅 {day['day_label']}:")
            for ev in day_events:
                lines.append(f"  {ev['time']} — {ev['title']}")
    return "\n".join(lines)


def _streets_info(program_data):
    lines = ["Carrers participants a la Festa Major de Sants 2026:"]
    for street in program_data.get("other_streets", []):
        theme = street.get("theme", "")
        lines.append(f"  - {street['name']}: {theme}")
    return "\n".join(lines)


today = str(date.today())

BASE_SYSTEM_PROMPT = f"""Ets la PapinIA, la intel·ligència artificial del carrer Papin de la Festa Major de Sants 2026. Ets una IA divertida, simpàtica i amb ganes de festa!

Estàs al carrer Papin durant la Festa Major de Sants (Barcelona). El tema del guarnit d'enguany és l'Olimpíada Popular de Barcelona de 1936, una competició esportiva alternativa als Jocs Olímpics de Berlín organitzats pel règim nazi de Hitler.

L'Olimpíada Popular va ser organitzada pel Comitè Català pro Esport Popular, amb el suport del govern de la República Espanyola (250.000 pessetes), la Generalitat de Catalunya presidida per Lluís Companys (100.000 pessetes) i el Front Popular francès (600.000 pessetes). S'hi van inscriure uns 6.000 atletes de 20 a 23 delegacions nacionals i regionals — incloent equips d'Alsàcia, Galícia, Euskadi, Algèria, Palestina i exiliats alemanys i italians antifeixistes. Havia de celebrar-se del 19 al 26 de juliol de 1936 a l'Estadi de Montjuïc, combinant esport i folklore (la "setmana popular de l'esport i el folklore"). El 18 de juliol, Pablo Casals assajava la Novena Simfonia de Beethoven al Teatre Grec per a la cerimònia d'inauguració quan va arribar la notícia del cop d'estat. El matí del 19 de juliol, els atletes es van despertar amb el so de les canonades del Paral·lel. La majoria van marxar a Marsella en un vaixell noliejat, però entre 200 i 600 atletes — com la nedadora suïssa Clara Thalmann (Columna Durruti) i la corredora María Ginestà (milícies socialistes) — van decidir quedar-se per lluitar contra el feixisme.

👉 Si et demanen el tema del carrer Papin (o el tema del carrer), respon sempre que és l'Olimpíada Popular de Barcelona de 1936.

No t'inventis informació si no la tens. Si no saps alguna cosa, recomana preguntar a la gent de la comissió a la barra.
La festa comença el 22 i acaba el 30 d'agost de 2026. Es decoren molts carrers.
Avui és el dia {today}.

La Comissió del carrer Papin:
- Va renéixer el 2014 gràcies a un grup de veïnes que volien recuperar la tradició.
- L'ambient és inclusiu i obert a tothom.
- Instagram: @comissiopapin
- Punt de trobada: Orfeó de Sants (C. Miquel Àngel, 54)

Estil d'interacció:
- Respon amb frases curtes. Evita llargues explicacions (màxim 1-2 paràgrafs).
- Sigues festiva, simpàtica i propera.
- Considera que hi pot haver gent amb esperit festiu o nens curiosos. Tu sempre educada i responsable.
- Intenta mantenir el català com a llengua principal.
- El teu carrer favorit és el Carrer Papin!

Imatges disponibles:
- Quan les dades rellevants mencionen una fotografia amb [IMATGE:nomfitxer.jpg], pots incloure-la a la teva resposta posant exactament [IMATGE:nomfitxer.jpg] al text.
- Només inclou una imatge si és realment rellevant per la pregunta. No n'incloguis mai més d'una per resposta.
- Mai t'inventis noms de fitxers d'imatge.
"""


def _build_context_block(category, program_data):
    blocks = []

    if category in ("programa", "programatot"):
        blocks.append(_full_program_text(program_data))
        blocks.append(_streets_info(program_data))

        today_str = str(date.today())
        today_summary = _program_summary_for_date(program_data, today_str)
        if today_summary:
            blocks.append(f"\n🔔 Avui ({today_str}):{today_summary}")

        tomorrow = date.today()
        from datetime import timedelta
        tomorrow_str = str(tomorrow + timedelta(days=1))
        tomorrow_summary = _program_summary_for_date(program_data, tomorrow_str)
        if tomorrow_summary:
            blocks.append(f"\n📆 Demà ({tomorrow_str}):{tomorrow_summary}")

    elif category == "carrers":
        blocks.append(_streets_info(program_data))

    elif category == "nens" or category == "familiar":
        blocks.append(_kids_events(program_data))

    elif category == "concert" or category == "música":
        blocks.append(_events_by_type(program_data, "concert"))

    elif category == "olimpiada":
        pass  # RAG handles this in generate_response

    elif category == "guarnit":
        blocks.append("""El guarnit del carrer Papin 2026 recrea l'ambient de l'Olimpíada Popular de Barcelona de 1936.
[PLACEHOLDER: detalls del guarnit es completaran quan estiguin disponibles]
""")

    elif category == "participar":
        blocks.append("""Com participar a la Comissió de Festes del Carrer Papin:
- Parlar amb la gent de la Comissió a la barra del carrer Papin
- Seguir-nos a Instagram: @comissiopapin
- Venir a l'Orfeó de Sants (C. Miquel Àngel, 54)
- La comissió va renéixer el 2014 i ha crescut molt
- No cal cap compromís constant: qualsevol ajuda és benvinguda
- L'ambient és inclusiu i obert a tothom
""")

    return "\n\n".join(blocks)


CLASSIFIER_PROMPT = """Ets un classificador. Analitza la pregunta de l'usuari i respon NOMÉS amb una d'aquestes opcions (sense cometes ni text addicional):

- programatot: si la pregunta demana el programa d'activitats, horaris, o què hi ha avui/demà/quan
- carrers: si la pregunta és sobre altres carrers participants o les seves decoracions
- olimpiada: si la pregunta és sobre l'Olimpíada Popular de 1936, el tema del guarnit, o la història
- guarnit: si la pregunta demana detalls tècnics del guarnit, materials o construcció
- participar: si la pregunta és sobre com col·laborar o participar a la comissió
- estandard: per a qualsevol altra cosa (salutacions, preguntes generals, dubte)

⚠️ Si et demanen què hi ha "al carrer" sense dir quin, es refereixen al carrer Papin.
"""


def classify(user_input, conversation_history=None):
    client = _get_client()

    user_message = ""
    if conversation_history:
        past = [f"- {m['content']}" for m in conversation_history if m["role"] == "user"]
        if past:
            user_message = "Preguntes anteriors (context):\n" + "\n".join(past[:-1]) + "\n\n"
    user_message += f"Pregunta actual:\n{user_input}"

    messages = [
        {"role": "system", "content": CLASSIFIER_PROMPT},
        {"role": "user", "content": user_message},
    ]
    try:
        resp = client.chat.completions.create(
            model="openai/gpt-oss-20B",
            messages=messages,
            temperature=0.0,
        )
        cat = resp.choices[0].message.content.strip().lower().replace("'", "").replace('"', '')
        return cat
    except Exception:
        return "estandard"


def generate_response(user_input, conversation_history, program_data):
    client = _get_client()

    category = classify(user_input, conversation_history)

    context_block = _build_context_block(category, program_data)
    system_prompt = BASE_SYSTEM_PROMPT

    if category == "olimpiada":
        chunks = retrieve(user_input, top_k=3)
        rag_context = format_context(chunks)
        if rag_context:
            context_block = rag_context + ("\n\n" + context_block if context_block else "")

    if context_block:
        system_prompt += f"\n\n--- DADES RELLEVANTS ---\n{context_block}\n--- FI DADES ---"

    messages = [{"role": "system", "content": system_prompt}]

    for msg in conversation_history:
        if msg["role"] in ("user", "assistant"):
            messages.append({"role": msg["role"], "content": msg["content"]})

    messages.append({"role": "user", "content": user_input})

    try:
        resp = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages,
        )
        reply = resp.choices[0].message.content
        reply = re.sub(r"<think.*?>.*?</think>", "", reply, flags=re.DOTALL | re.IGNORECASE)
        return reply.strip()
    except Exception as e:
        return f"Hi ha hagut un problema, intenta-ho de nou més tard. ({e})"
