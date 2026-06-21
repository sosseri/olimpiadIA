# PapinIA — Festa Major de Sants 2026

Chatbot interactiu per al **Carrer Papin** de la Festa Major de Sants 2026. Respon preguntes sobre el programa de la festa, la història de l'**Olimpíada Popular de Barcelona de 1936** i el guarnit del carrer, en català i amb veu.

## Estructura del projecte

```
├── app_main.py              # Pàgina d'inici (Streamlit)
├── pages/
│   ├── 1_xat.py             # Xat amb PapinIA
│   ├── 2_programa.py        # Programa d'activitats
│   ├── 3_olimpiada.py       # Història de l'Olimpíada Popular
│   ├── 4_arxiu.py           # Arxiu fotogràfic
│   └── 5_festa_major.py     # Info general de la Festa Major
├── lib/
│   ├── chatbot.py           # Lògica principal: classificació i generació de respostes
│   └── rag.py               # Recuperació de context per a preguntes sobre l'Olimpíada
├── data/
│   ├── programa.json        # Programa d'activitats de la festa
│   ├── olimpiada_chunks.json  # Base de coneixement sobre l'Olimpíada (RAG)
│   └── images_metadata.json   # Metadades de les imatges històriques
├── assets/
│   ├── images/              # Imatges històriques de l'Olimpíada Popular
│   └── festa/               # Fotos de la festa i el carrer Papin
└── .env                     # Clau API (no pujada al repositori)
```

## Instal·lació i execució local

### Prerequisits

- Python 3.10 o superior
- Clau d'API de [Groq](https://console.groq.com)

### Instal·lació

```bash
git clone <url-del-repositori>
cd OlimpiadaIA
pip install -r requirements.txt
```

### Configuració

Crea un fitxer `.env` a l'arrel del projecte:

```
GROQ_API_KEY=la_teva_clau_aqui
```

### Execució

```bash
streamlit run app_main.py
```

L'aplicació s'obre a [http://localhost:8501](http://localhost:8501).

## Desplegament a Render

1. Crea un nou servei web a [Render](https://render.com) apuntant al repositori.
2. A **Environment**, afegeix la variable `GROQ_API_KEY` amb la teva clau.
3. Com a **Start command**: `streamlit run app_main.py --server.port $PORT --server.address 0.0.0.0`

La primera interacció pot trigar fins a 1 minut si el servei ha estat inactiu (cold start del pla gratuït).

---

## Com modificar la informació dels prompts

El comportament del chatbot es controla des de `lib/chatbot.py`. Hi ha tres nivells:

### 1. Personalitat i context general (`BASE_SYSTEM_PROMPT`)

Modifica la variable `BASE_SYSTEM_PROMPT` per canviar:
- La personalitat del bot (to, estil, idioma)
- Les dates de la festa
- La informació de la comissió (Instagram, punt de trobada)
- El resum del tema de l'Olimpíada que el bot sempre té present

### 2. Context específic per categoria (`_build_context_block`)

Quan l'usuari pregunta sobre un tema concret, el bot rep un bloc de context addicional. Cada `elif category == "..."` correspon a un tema:

| Categoria | Quan s'activa | On editar |
|---|---|---|
| `programatot` / `programa` | Preguntes sobre el programa | `_full_program_text()` llegeix `data/programa.json` |
| `carrers` | Altres carrers de la festa | `_streets_info()` llegeix `data/programa.json` |
| `olimpiada` | Història de l'Olimpíada | **RAG** — veure secció següent |
| `guarnit` | El guarnit del carrer | Bloc de text directament a `_build_context_block` |
| `participar` | Com unir-se a la comissió | Bloc de text directament a `_build_context_block` |

Per exemple, per actualitzar la informació del guarnit:

```python
# lib/chatbot.py, dins de _build_context_block:
elif category == "guarnit":
    blocks.append("""El guarnit del carrer Papin 2026 recrea...
    [escriu aquí la descripció actualitzada]
    """)
```

### 3. Classificador (`CLASSIFIER_PROMPT`)

El `CLASSIFIER_PROMPT` defineix les categories possibles i quan s'aplica cada una. Si afegeixes una nova categoria (p. ex. `musica`), cal:

1. Afegir-la a la llista del `CLASSIFIER_PROMPT`
2. Afegir el bloc `elif category == "musica":` a `_build_context_block`

---

## Com afegir imatges noves

Les imatges es mostren a l'arxiu fotogràfic (`pages/4_arxiu.py`) i el chatbot pot referenciar-les en les respostes.

### Pas 1: Afegir el fitxer d'imatge

Copia la imatge a la carpeta corresponent:

- `assets/images/` — imatges històriques de l'Olimpíada Popular (les que pot citar el chatbot)
- `assets/festa/` — fotos de la festa i el carrer Papin (només apareixen a l'arxiu, el bot no les cita)

Usa noms descriptius en `snake_case`, per exemple: `atletes_seleccio_francesa_1936.jpg`

### Pas 2: Afegir les metadades a `data/images_metadata.json`

Afegeix una entrada al array JSON:

```json
{
  "file": "atletes_seleccio_francesa_1936.jpg",
  "caption": "Atletes de la selecció francesa abans de partir cap a Barcelona per a l'Olimpíada Popular",
  "caption_es": "Atletas de la selección francesa antes de partir hacia Barcelona para la Olimpiada Popular",
  "source_url": "https://url-original-de-la-imatge.jpg",
  "source_site": "nom-del-lloc.com",
  "year": "1936"
}
```

Camps obligatoris: `file`, `caption`, `source_url`, `source_site`.

### Pas 3: El chatbot la detecta automàticament

No cal fer res més. `lib/rag.py` llegeix `images_metadata.json` en arrencar i crea automàticament un chunk de context per a cada imatge, amb paraules clau extretes del nom del fitxer i de la llegenda. Quan un usuari faci una pregunta relacionada, el bot rebrà el context i podrà incloure `[IMATGE:nomfitxer.jpg]` a la resposta, que el xat renderitza com una imatge inline.

> **Nota**: si afegeixes una imatge però el bot no la menciona espontàniament, prova a fer la pregunta de forma més directa (p. ex. "tens fotos de...?"). El sistema recupera fins a 3 chunks per consulta; si hi ha molt contingut relacionat, la imatge pot quedar fora dels tres primers.

---

## Models utilitzats

| Rol | Model | Notes |
|---|---|---|
| Classificació | `openai/gpt-oss-20b` | Temperatura 0, ràpid i determinista |
| Generació de respostes | `openai/gpt-oss-120b` | Via Groq API |

Ambdós models s'accedeixen a través de l'API de [Groq](https://console.groq.com). Per canviar el model, modifica les constants `model=` a `lib/chatbot.py` (funcions `classify` i `generate_response`).

---

## Crèdits

Desenvolupat per la Comissió del Carrer Papin per a la Festa Major de Sants 2026.  
Contacte: [@comissiopapin](https://instagram.com/comissiopapin) · Orfeó de Sants, C. Miquel Àngel 54, Barcelona.
