import json
import os
import re
from datetime import date

import groq
from dotenv import load_dotenv

from lib.rag import format_context, retrieve_with_image

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


def _get_street(program_data, key):
    return program_data.get("streets", {}).get(key, {})


def _street_days_sorted(street_data):
    return sorted(street_data.get("days", {}).items())


def _program_summary_for_date(program_data, target_date_str):
    lines = []
    papin = _get_street(program_data, "papin")
    day_data = papin.get("days", {}).get(target_date_str)
    if day_data:
        lines.append(f"\n📅 {day_data['day_label']} — Carrer Papin:")
        for ev in day_data["events"]:
            lines.append(f"  {ev['time']} — {ev['title']}: {ev.get('description', '')}")
    unitari = _get_street(program_data, "unitari")
    u_day = unitari.get("days", {}).get(target_date_str)
    if u_day:
        lines.append(f"\n📅 {u_day['day_label']} — Actes Unitaris:")
        for ev in u_day["events"]:
            lines.append(f"  {ev['time']} — {ev['title']}")
    return "\n".join(lines) if lines else None


def _full_program_text(program_data):
    lines = ["Programa complet del Carrer Papin:"]
    papin = _get_street(program_data, "papin")
    for dk, day_data in _street_days_sorted(papin):
        lines.append(f"\n📅 {day_data['day_label']}:")
        for ev in day_data["events"]:
            lines.append(f"  {ev['time']} — {ev['title']}")
            if ev.get("description"):
                lines.append(f"         {ev['description']}")
    unitari = _get_street(program_data, "unitari")
    if unitari:
        lines.append("\n\nActes Unitaris:")
        for dk, day_data in _street_days_sorted(unitari):
            lines.append(f"\n📅 {day_data['day_label']}:")
            for ev in day_data["events"]:
                lines.append(f"  {ev['time']} — {ev['title']}")
    return "\n".join(lines)


def _street_program_text(program_data, street_key):
    street = _get_street(program_data, street_key)
    if not street:
        return ""
    lines = [_street_header(street), ""]
    for dk, day_data in _street_days_sorted(street):
        lines.append(f"📅 {day_data['day_label']}:")
        for ev in day_data["events"]:
            lines.append(f"  {ev['time']} — {ev['title']}")
            if ev.get("description"):
                lines.append(f"         {ev['description']}")
        lines.append("")
    return "\n".join(lines)


def _all_streets_summary(program_data):
    """All streets with theme + decoration — no program events."""
    lines = ["Carrers participants a la Festa Major de Sants 2026:\n"]
    for key, street in program_data.get("streets", {}).items():
        if key == "unitari":
            continue
        lines.append(_street_header(street))
        lines.append("")
    return "\n".join(lines)


def _kids_events(program_data):
    lines = ["Activitats per a nens/famílies al Carrer Papin:"]
    papin = _get_street(program_data, "papin")
    for dk, day_data in _street_days_sorted(papin):
        day_events = [ev for ev in day_data["events"] if ev.get("for_kids")]
        if day_events:
            lines.append(f"\n📅 {day_data['day_label']}:")
            for ev in day_events:
                lines.append(f"  {ev['time']} — {ev['title']}")
    return "\n".join(lines)


def _events_by_type(program_data, event_type):
    lines = [f"Activitats de tipus '{event_type}' al Carrer Papin:"]
    papin = _get_street(program_data, "papin")
    for dk, day_data in _street_days_sorted(papin):
        day_events = [
            ev
            for ev in day_data["events"]
            if ev.get("type") == event_type or event_type in ev.get("tags", [])
        ]
        if day_events:
            lines.append(f"\n📅 {day_data['day_label']}:")
            for ev in day_events:
                lines.append(f"  {ev['time']} — {ev['title']}")
    return "\n".join(lines)


def _streets_info(program_data):
    return _all_streets_summary(program_data)


today = str(date.today())

BASE_SYSTEM_PROMPT = f"""Ets la PapinIA, la intel·ligència artificial del carrer Papin de la Festa Major de Sants 2026. Ets una IA divertida, simpàtica i amb ganes de festa!

Estàs al carrer Papin durant la Festa Major de Sants (Barcelona). El tema del guarnit d'enguany és l'Olimpíada Popular de Barcelona de 1936, una competició esportiva alternativa als Jocs Olímpics de Berlín organitzats pel règim nazi de Hitler.

L'Olimpíada Popular va ser organitzada pel Comitè Català pro Esport Popular, amb el suport del govern de la República Espanyola (250.000 pessetes), la Generalitat de Catalunya presidida per Lluís Companys (100.000 pessetes) i el Front Popular francès (600.000 pessetes). S'hi van inscriure uns 6.000 atletes de 20 a 23 delegacions nacionals i regionals — incloent equips d'Alsàcia, Galícia, Euskadi, Algèria, Palestina i exiliats alemanys i italians antifeixistes. Havia de celebrar-se del 19 al 26 de juliol de 1936 a l'Estadi de Montjuïc, combinant esport i folklore (la "setmana popular de l'esport i el folklore"). El 18 de juliol, Pablo Casals assajava la Novena Simfonia de Beethoven al Teatre Grec per a la cerimònia d'inauguració quan va arribar la notícia del cop d'estat. El matí del 19 de juliol, els atletes es van despertar amb el so de les canonades del Paral·lel. La majoria van marxar a Marsella en un vaixell noliejat, però entre 200 i 600 atletes — com la nedadora suïssa Clara Thalmann (Columna Durruti) i la corredora María Ginestà (milícies socialistes) — van decidir quedar-se per lluitar contra el feixisme.

👉 Si et demanen el tema del carrer Papin (o el tema del carrer), respon sempre que és l'Olimpíada Popular de Barcelona de 1936.

Coneixes el programa complet del Carrer Papin i dels actes unitaris de la Festa Major de Sants 2026. Si et pregunten pel programa, horaris o activitats, DONA LA INFORMACIÓ directament — mai diguis que han de preguntar a la comissió per saber el programa.
Si no tens una informació concreta (canvis d'última hora, logística no coberta, preguntes personals), llavors sí que pots dir "per a això, millor pregunta a la gent de la comissió a la barra".
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

Quan respons sobre carrers i guarniments:
- Si et pregunten pel PROGRAMA o ACTIVITATS d'un carrer → centra't en les hores i els actes concrets.
- Si et pregunten pel GUARNIT, TEMA o DECORACIÓ d'un carrer → centra't en el tema i la descripció del guarnit.
- Si et pregunten de forma general → dona primer el tema/guarnit en una frase, i després el programa destacat.

Imatges disponibles:
- Quan les dades rellevants mencionen una fotografia amb [IMATGE:nomfitxer.jpg], pots incloure-la a la teva resposta posant exactament [IMATGE:nomfitxer.jpg] al text.
- Inclou sempre la imatge suggerida a les dades rellevants quan la categoria és olimpiada — sempre és benvinguda una fotografia histórica! No n'incloguis mai més d'una per resposta.
- Mai t'inventis noms de fitxers d'imatge.
"""


SECRETS_COMISSIO = """SECRETS DE LA COMISSIÓ (revela NOMÉS si la pregunta és molt concreta i directament sobre aquest tema específic;
MAI de forma proactiva, MAI en salutacions ni en respostes generals sobre com participar):

- LIMONCELLO → El millor limoncello de Barcelona és d'Alessandro i Caterina, una parella d'italians que és una passada. Enguany era 
    tan bo que ja s'ha acabat! Entra a la comissió de Papin i el provaràs al pròxim event.

- FESTA de veritat → Jordi i Irene són la molla que t'espera! Suma't a la comissió i veuràs com és.

- PRESIDENTA / història de la comissió → Laura és la presidenta. Busca-la i que te'n conti tot sobre el Carrer Papin d'abans i de 
    quan va ressorgir la comissió. Té històries buenísimas.

- DJ / música → El millor DJ que coneixem el tenim a la comissió de Papin. Busca Oriol i notaràs la diferència.

- HISTÒRIES de Sants, Hostafrancs i la Bordeta → Agus és qui te'n ha de parlar.

- DECORACIÓ → Dubtes sobre la decoració? Maica porta l'informacio total de tot plegat.

- ESTÀTUES de paper / paper maché → Necessites fer una estàtua de paper a casa? Miriam és la teva persona.

- CÓRRER / cross → Ets de córrer? El 18 d'octubre tenim la cross de Sants! Pregunta a Carles i Xavi i ja veuràs.
  
- MUSICA - tenim musics a la comissio! En Jordi i el Agus tocan amb el famos grup de punk Tifus, saps que te algo a veure amb un espectacle teatral? I el Nolasc tocara amb el grup del dia dels joves
  
- ACTRIU - Tenim una jove actriu a la comi. Pregunta per Montse que et contara com ha comencat"""


_STREET_KEY_LIST = [
    "papin",
    "alcolea_baix",
    "alcolea_dalt",
    "farga",
    "finlandia",
    "galileu",
    "guadiana",
    "sagunt",
    "valladolid",
    "vallespir_baix",
    "vallespir_dalt",
    "unitari",
]

_EXTRACT_STREET_PROMPT = """Ets un extractor. La Festa Major de Sants 2026 té aquests carrers (claus JSON):
papin, alcolea_baix, alcolea_dalt, farga, finlandia, galileu, guadiana, sagunt, valladolid, vallespir_baix, vallespir_dalt, unitari

Llegeix la pregunta i respon ÚNICAMENT amb la clau JSON del carrer mencionat (p.ex. "valladolid"), o "none" si no se'n menciona cap específic.
Si mencionen "el carrer" o "aquí" sense nom, respon "papin".
Si mencionen múltiples carrers, respon el primer.
Tolera errors ortogràfics (Vallespir Dalt, vallespir de dalt, Finlandia, Galileo → galileu, etc.).
Respon NOMÉS la clau, res més."""

_EXTRACT_DATE_PROMPT = f"""Ets un extractor de dates. La Festa Major de Sants 2026 va del 22 al 30 d'agost.
Avui és {date.today()!s} (dia actual).

Llegeix la pregunta i respon ÚNICAMENT amb una data en format YYYY-MM-DD si s'hi menciona un dia concret, o "none" si no.
Exemples:
- "dijous" → 2026-08-27  (dijous de la festa = 27 agost)
- "divendres" → 2026-08-28
- "dissabte" → pots preguntar-te si és el 22 o el 29; si no hi ha número, "none"
- "avui" → {date.today()!s}
- "demà" → {date.today() + __import__("datetime").timedelta(days=1)!s}
- "sant bartomeu" → 2026-08-24
- "dia jove" → 2026-08-26
- "dilluns 24" → 2026-08-24
- "divendres 28" → 2026-08-28
Respon NOMÉS la data o "none", res més."""

_EXTRACT_FOCUS_PROMPT = """Ets un extractor. Llegeix la pregunta i respon ÚNICAMENT amb una d'aquestes opcions:

- events: la pregunta demana activitats, horaris, concerts, programa, que hi ha, quan és, a quina hora...
- theme: la pregunta demana el tema, la decoració, el guarnit, com és el carrer, de que va...
- both: la pregunta és general o demana les dues coses alhora

Exemples:
- "Que hi ha dijous?" → events
- "A quina hora és el concert?" → events
- "Quin és el tema de Valladolid?" → theme
- "Com és la decoració de Finlàndia?" → theme
- "Parla'm del carrer Sagunt" → both
- "Quins carrers participen?" → both
- "Que hi ha i com és el guarnit de Galileu?" → both

Respon NOMÉS "events", "theme" o "both", res més."""


def _extract_street_date_focus(user_input, conversation_history):
    """
    Run 3 LLM calls in parallel to extract:
      - street key (or None)
      - date string YYYY-MM-DD (or None)
      - focus: "events" | "theme" | "both"
    """
    from concurrent.futures import ThreadPoolExecutor

    client = _get_client()

    context = ""
    if conversation_history:
        recent = [
            m["content"] for m in conversation_history[-4:] if m["role"] == "user"
        ]
        if recent:
            context = "Context recent: " + " | ".join(recent) + "\n"
    full_text = context + "Pregunta: " + user_input

    def call(system_prompt):
        try:
            resp = client.chat.completions.create(
                model="openai/gpt-oss-20B",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": full_text},
                ],
                temperature=0.0,
            )
            return (
                resp.choices[0]
                .message.content.strip()
                .lower()
                .replace('"', "")
                .replace("'", "")
            )
        except Exception:
            return None

    with ThreadPoolExecutor(max_workers=3) as ex:
        f_street = ex.submit(call, _EXTRACT_STREET_PROMPT)
        f_date = ex.submit(call, _EXTRACT_DATE_PROMPT)
        f_focus = ex.submit(call, _EXTRACT_FOCUS_PROMPT)
        street_raw = f_street.result()
        date_raw = f_date.result()
        focus_raw = f_focus.result()

    street_key = street_raw if street_raw in _STREET_KEY_LIST else None

    date_str = None
    if date_raw and date_raw != "none":
        if re.match(r"^\d{4}-\d{2}-\d{2}$", date_raw):
            date_str = date_raw

    focus = focus_raw if focus_raw in ("events", "theme", "both") else "both"

    return street_key, date_str, focus


# Keep old name as alias so nothing else breaks
def _extract_street_and_date(user_input, conversation_history):
    street_key, date_str, _ = _extract_street_date_focus(
        user_input, conversation_history
    )
    return street_key, date_str


def _street_header(street_data):
    """One-line header with theme and decoration for a street."""
    name = street_data.get("name", "")
    theme = street_data.get("theme", "")
    deco = street_data.get("decoration_description", "")
    lines = [f"🏘️ {name}"]
    if theme:
        lines.append(f"  Tema del guarnit: {theme}")
    if deco:
        lines.append(f"  Decoració: {deco}")
    return "\n".join(lines)


def _single_day_text(street_data, date_str):
    """Render one day of a street as text, with street header."""
    day = street_data.get("days", {}).get(date_str)
    if not day:
        return None
    lines = [_street_header(street_data), f"📅 {day['day_label']}:"]
    for ev in day["events"]:
        lines.append(f"  {ev['time']} — {ev['title']}")
        if ev.get("description"):
            lines.append(f"         {ev['description']}")
    return "\n".join(lines)


CLASSIFIER_PROMPT = """Ets un classificador per a la Festa Major de Sants (Barcelona). Analitza la pregunta i respon NOMÉS amb una d'aquestes opcions (sense cometes ni text addicional):

- programa: preguntes sobre activitats, horaris, concerts, programa, decoració, tema, guarnit, carrers participants, durada de la festa o qualsevol cosa relacionada amb la Festa Major de Sants 2026
- olimpiada: preguntes sobre l'Olimpíada Popular de 1936, atletes antifeixistes, la Guerra Civil, Pablo Casals, Clara Thalmann, María Ginestà, els Jocs de Berlín, Hitler, la República, o qualsevol tema històric d'aquella època
- guarnit: preguntes sobre com s'ha CONSTRUÏT físicament el guarnit de Papin (materials concrets, tècniques, brics, tul, fusta, paper maché, com s'ha fet)
- participar: preguntes sobre com unir-se, col·laborar o participar a la comissió de festes del carrer Papin
- estandard: salutacions, preguntes totalment fora de tema (aparcar, restaurants, transport...) o xat general

Carrers de la festa (tots van sota "programa"): Papin, Valladolid, Sagunt, Guadiana, Finlàndia, Galileu, Alcolea de Baix, Alcolea de Dalt, Plaça de la Farga, Vallespir de Baix, Vallespir de Dalt.

Exemples:
- "Que hi ha avui?" → programa
- "Concerts a Valladolid?" → programa
- "Quins carrers participen?" → programa
- "Fins quan dura la festa?" → programa
- "Tema de Finlàndia?" → programa
- "Qui era Clara Thalmann?" → olimpiada
- "Que va passar el 19 de juliol del 36?" → olimpiada
- "Amb quins materials s'ha fet el sostre?" → guarnit
- "Com puc ajudar a la comissió?" → participar
- "Teniu limoncello?" → participar
- "Qui és la presidenta?" → participar
- "Hi ha algun DJ a la comissió?" → participar
- "Qui em pot explicar la història de Sants?" → participar
- "Hola!" → estandard
- "On puc aparcar?" → estandard
"""


def classify(user_input, conversation_history=None):
    client = _get_client()

    user_message = ""
    if conversation_history:
        past = [
            f"- {m['content']}" for m in conversation_history if m["role"] == "user"
        ]
        if past:
            user_message = (
                "Preguntes anteriors (context):\n" + "\n".join(past[:-1]) + "\n\n"
            )
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
        cat = (
            resp.choices[0]
            .message.content.strip()
            .lower()
            .replace("'", "")
            .replace('"', "")
        )
        return cat
    except Exception:
        return "estandard"


def _build_program_context(user_input, conversation_history, program_data):
    """
    Smart context builder for program queries.
    Uses two LLM calls to extract street and date, then injects only the relevant JSON slice.
    Falls back to broader context when neither is detected.
    """
    from datetime import timedelta

    street_key, date_str, focus = _extract_street_date_focus(
        user_input, conversation_history
    )

    blocks = []
    today_str = str(date.today())
    tomorrow_str = str(date.today() + timedelta(days=1))

    if street_key and date_str:
        # One street, one day
        street = _get_street(program_data, street_key)
        if focus == "theme":
            # Only decoration — no events needed
            blocks.append(_street_header(street))
        elif focus == "events":
            # Only events — minimal header for context
            day_text = _single_day_text(street, date_str)
            if day_text:
                blocks.append(day_text)
            else:
                blocks.append(
                    f"{street.get('name', street_key)}: no hi ha activitats el {date_str}."
                )
            unitari = _get_street(program_data, "unitari")
            u_day = unitari.get("days", {}).get(date_str)
            if u_day:
                u_lines = [f"Actes unitaris el {u_day['day_label']}:"]
                for ev in u_day["events"]:
                    u_lines.append(f"  {ev['time']} — {ev['title']}")
                blocks.append("\n".join(u_lines))
        else:  # both
            day_text = _single_day_text(street, date_str)
            if day_text:
                blocks.append(day_text)
            else:
                blocks.append(
                    f"{_street_header(street)}\n"
                    f"No hi ha activitats registrades per a {street.get('name', street_key)} el {date_str}."
                )
            unitari = _get_street(program_data, "unitari")
            u_day = unitari.get("days", {}).get(date_str)
            if u_day:
                u_lines = [f"Actes unitaris el {u_day['day_label']}:"]
                for ev in u_day["events"]:
                    u_lines.append(f"  {ev['time']} — {ev['title']}")
                blocks.append("\n".join(u_lines))

    elif street_key and not date_str:
        # One street, no date
        street = _get_street(program_data, street_key)
        if focus == "theme":
            blocks.append(_street_header(street))
        elif focus == "events":
            # Header-less: just days and events
            lines = []
            for dk, day_data in _street_days_sorted(street):
                lines.append(f"📅 {day_data['day_label']}:")
                for ev in day_data["events"]:
                    lines.append(f"  {ev['time']} — {ev['title']}")
            blocks.append("\n".join(lines))
        else:  # both
            blocks.append(_street_program_text(program_data, street_key))

    elif date_str and not street_key:
        # One day, all streets
        if focus == "theme":
            # Only themes — no events
            blocks.append(f"Carrers i guarniments per al {date_str}:\n")
            for key, street in program_data.get("streets", {}).items():
                if key == "unitari":
                    continue
                blocks.append(_street_header(street))
        elif focus == "events":
            # Only events per street that day
            for key, street in program_data.get("streets", {}).items():
                if key == "unitari":
                    continue
                day_text = _single_day_text(street, date_str)
                if day_text:
                    blocks.append(day_text)
            unitari = _get_street(program_data, "unitari")
            u_day = unitari.get("days", {}).get(date_str)
            if u_day:
                u_lines = ["Actes unitaris:"]
                for ev in u_day["events"]:
                    u_lines.append(f"  {ev['time']} — {ev['title']}")
                blocks.append("\n".join(u_lines))
        else:  # both
            blocks.append(f"Programa i guarniments per al {date_str}:\n")
            for key, street in program_data.get("streets", {}).items():
                if key == "unitari":
                    continue
                day_text = _single_day_text(street, date_str)
                if day_text:
                    blocks.append(day_text)
                else:
                    blocks.append(
                        _street_header(street) + "\n  (sense activitats aquest dia)"
                    )
            unitari = _get_street(program_data, "unitari")
            u_day = unitari.get("days", {}).get(date_str)
            if u_day:
                u_lines = ["Actes unitaris:"]
                for ev in u_day["events"]:
                    u_lines.append(f"  {ev['time']} — {ev['title']}")
                blocks.append("\n".join(u_lines))

    else:
        # No street, no date
        if focus == "theme":
            blocks.append(_all_streets_summary(program_data))
        elif focus == "events":
            blocks.append(_full_program_text(program_data))
            today_summary = _program_summary_for_date(program_data, today_str)
            if today_summary:
                blocks.append(f"🔔 Avui ({today_str}):{today_summary}")
            tomorrow_summary = _program_summary_for_date(program_data, tomorrow_str)
            if tomorrow_summary:
                blocks.append(f"📆 Demà ({tomorrow_str}):{tomorrow_summary}")
        else:  # both
            blocks.append(_full_program_text(program_data))
            blocks.append(_all_streets_summary(program_data))
            today_summary = _program_summary_for_date(program_data, today_str)
            if today_summary:
                blocks.append(f"🔔 Avui ({today_str}):{today_summary}")
            tomorrow_summary = _program_summary_for_date(program_data, tomorrow_str)
            if tomorrow_summary:
                blocks.append(f"📆 Demà ({tomorrow_str}):{tomorrow_summary}")

    return "\n\n".join(b for b in blocks if b)


def generate_response(user_input, conversation_history, program_data):
    client = _get_client()

    category = classify(user_input, conversation_history)

    system_prompt = BASE_SYSTEM_PROMPT
    context_block = ""

    if category == "programa":
        context_block = _build_program_context(
            user_input, conversation_history, program_data
        )

    elif category == "olimpiada":
        chunks = retrieve_with_image(user_input, top_k=3)
        context_block = format_context(chunks)

    elif category == "guarnit":
        context_block = """El guarnit del Carrer Papin 2026 recrea l'Olimpíada Popular de Barcelona de 1936.
Dimensions: 24 m de llargada × 8 m d'amplada (192 m²).

Zones del guarnit:
- La portalada: cartell oficial de l'Olimpíada Popular, un avió amb publicitat i una guita (figura de cultura popular).
- La paret lateral: grades de l'estadi amb públic de l'època, esportistes de països i regions participants, banderoles dels esports.
- El sostre: simula el cel de l'estadi amb coloms blancs (com en les inauguracions olímpiques) i confeti gegant amb els colors de l'Olimpíada.
- La contraportalada: l'inici de la guerra — un mur mig derruït amb el cartell de la inauguració enganxat, bombes i coloms blancs morts.

Materials (tot reciclat):
- Cartró (capses, cartró ploma, tub de cartró trobat al carrer): coloms, confeti, plafons de la barra, grades, avió, coll de la guita.
- 660 tetrabricks: el mur i els trossos de mur derruït.
- Teles pintades i 9 llençols vells: cel blau, cos de la guita, banderoles amb logos d'esports.
- Llistons i fullola de fusta: ales de l'avió, estructura del cartell, figures i lletres, base de la guita.
- Malla de galliner: cos de la guita.
- Paper maixé: cap de la guita, coloms, avió, marcs dels plafons, grades.
- Pintura ecològica.

La Olimpiada Popular de Barcelona de 1936 no llegó a celebrarse a causa del estallido del golpe de Estado y el inicio de la Guerra Civil el 18 de julio de 1936. Por este motivo, no hubo ceremonia inaugural oficial ni suelta de palomas blancas (coloms blancs).
Contexto de la Olimpiada Popular
Fecha prevista: Del 19 al 26 de julio de 1936.
Motivo de la cancelación: El alzamiento militar frustró el evento horas antes de su comienzo en el Estadio de Montjuïc.
Participantes esperados: Cerca de 6.000 atletas de 22 naciones y unos 20.000 visitantes totales en Barcelona. En la parte delantera de la calle reproducimos el evento como habría sido (como gente en el estadio y els coloms de la inauguracion de inicio olimpiadas), en la parte trasera representamos el estallido del golpe de Estado y el inicio de la guerra civil."""

    elif category == "participar":
        context_block = """Com participar a la Comissió de Festes del Carrer Papin:
- Parlar amb la gent de la Comissió a la barra del carrer Papin
- Seguir-nos a Instagram: @comissiopapin
- Venir a l'Orfeó de Sants (C. Miquel Àngel, 54)
- La comissió va renéixer el 2014 i ha crescut molt
- No cal cap compromís constant: qualsevol ajuda és benvinguda
- L'ambient és inclusiu i obert a tothom
""" + SECRETS_COMISSIO

    elif category == "estandard":
        context_block = """CONTEXT GENERAL (per a salutacions i xat fora de tema):

Festa Major de Sants 2026:

- Del 22 al 30 d'agost de 2026, al barri de Sants (Barcelona). Lema: "Per molts Sants, sempre".

- Onze carrers i espais es guarneixen. El teu carrer és el Carrer Papin, amb el tema de l'Olimpíada Popular de 1936.

- Carrers participants: Papin, Alcolea de Baix, Alcolea de Dalt, Plaça de la Farga, Finlàndia, Galileu, Guadiana, Sagunt, Valladolid,
  Vallespir de Baix i Vallespir de Dalt.

Olimpíada Popular (molt resumit):

- Competició esportiva antifeixista prevista a Barcelona del 19 al 26 de juliol de 1936, alternativa als Jocs de Berlín de Hitler. No
  es va arribar a celebrar per l'esclat de la Guerra Civil.

Sobre què pots preguntar-me:

- El programa i els horaris de la festa i dels carrers.

- La decoració i el guarnit dels carrers.

- La història de l'Olimpíada Popular de 1936.

- Com participar a la comissió del Carrer Papin.

Comportament:

- Sigues sempre educada, propera i festiva.

- No caiguis en provocacions, insults ni vulgaritats: reconduïx amb simpatia cap a la festa.

- Si et pregunten coses totalment fora de tema (aparcament, restaurants, transport...), respon amablement que ets la IA del Carrer
  Papin i redirigeix cap al que sí que saps.

""" + SECRETS_COMISSIO

    elif category in ("nens", "familiar"):
        context_block = _kids_events(program_data)

    if context_block:
        system_prompt += (
            f"\n\n--- DADES RELLEVANTS ---\n{context_block}\n--- FI DADES ---"
        )

    is_first_message = not any(m["role"] == "user" for m in conversation_history)
    if is_first_message:
        system_prompt += """

--- PRIMER MISSATGE ---
És el primer missatge d'aquesta persona. Al final de la teva resposta, afegeix una línia breu i festiva que els convidi a explorar, per exemple:
"Pots preguntar-me sobre el programa, la decoració del carrer, la història de l'Olimpíada Popular... o el que vulguis! 🎉"
Adapta-ho al context de la seva pregunta, però sempre de forma curta i acollidora.
--- FI PRIMER MISSATGE ---"""

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
        reply = re.sub(
            r"<think.*?>.*?</think>", "", reply, flags=re.DOTALL | re.IGNORECASE
        )
        reply = reply.strip()

        if category == "olimpiada":
            image_files = []
            try:
                image_files = [
                    c.get("image_file")
                    for c in retrieve_with_image(user_input, top_k=3)
                    if c.get("is_image") and c.get("image_file")
                ]
            except Exception:
                image_files = []

            if image_files and not re.search(
                r"\[(?:IMATGE|IMAGE|IMAGEN):[^\]]+\]", reply, flags=re.IGNORECASE
            ):
                reply = reply.rstrip() + f"\n[IMATGE:{image_files[0]}]"

        return reply
    except Exception as e:
        return f"Hi ha hagut un problema, intenta-ho de nou més tard. ({e})"
