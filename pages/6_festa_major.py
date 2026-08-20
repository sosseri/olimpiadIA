import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Festa Major de Sants", page_icon="🎭", layout="centered", initial_sidebar_state="expanded")

from lib.decor import section_accent, nav_bar

nav_bar()

MAP_EMBED_URL = "https://www.google.com/maps/d/embed?mid=1Mm-g7z6ukfmLSi5zEH3uvXwQ2secCTER&ll=41.3766953765755%2C2.134091757378447&z=15"

st.markdown("""
<style>
    .festa-header {
        background: linear-gradient(135deg, #e65100 0%, #f57c00 50%, #ffa726 100%);
        border-radius: 16px; padding: 1.5rem; text-align: center; color: #fff;
        margin-bottom: 1.5rem; box-shadow: 0 2px 10px rgba(0,0,0,0.15);
    }
    .festa-header h1 { margin: 0; font-size: 1.5rem; }
    .festa-header p { margin: 0.3rem 0 0; font-size: 0.95rem; opacity: 0.9; }
    .fact-box {
        background: #fff3e0; border-left: 4px solid #e65100;
        padding: 1rem; border-radius: 0 8px 8px 0; margin: 0.8rem 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="festa-header">
    <h1>🎭 La Festa Major de Sants</h1>
    <p>Història, orígens i tradicions de la festa del barri</p>
</div>
""", unsafe_allow_html=True)

section_accent(0)
st.markdown("""
## Orígens

La **Festa Major de Sants** és una de les festes de barri més importants i emblemàtiques de Barcelona. Les seves arrels es remunten a mitjans del **segle XIX**, quan **Santa Maria de Sants** era encara un municipi independent, separat de Barcelona.

La festa se celebra al voltant del **24 d'agost**, festivitat de **Sant Bartomeu**, patró de l'antiga parròquia de Sants. Les primeres celebracions consistien en balls, cercaviles, actes religiosos i activitats populars.
""")

section_accent(1)
st.markdown("""
## Els carrers guarnits: l'ànima de la festa

El tret més característic de la Festa Major de Sants és la **decoració dels carrers** (els "guarnits"). Aquesta tradició va començar de manera organitzada el **1943**, quan els veïns van començar a competir per tenir el carrer més ben decorat.

Entre 1970 i 1984, la tradició va decaure significativament, però el **1985** es va reprendre amb força i des de llavors no ha parat de créixer.

Cada carrer o plaça participant:
- Tria un **tema** cada any (pot ser cultural, històric, reivindicatiu, fantàstic...)
- Forma una **comissió de festes** amb veïns i veïnes del carrer
- Treballa durant mesos (sovint des del març o abril) per construir les decoracions
- Utilitza principalment **materials reciclats i reutilitzats**
- Competeix al **concurs oficial de guarniment** i al **concurs popular de Sants 3 Ràdio**
""")

st.markdown("""
<div class="fact-box">
<strong>Sabies que...</strong> Les decoracions es fan íntegrament pels veïns i veïnes de cada carrer,
sense pressupostos grans ni professionals. La creativitat, el treball en equip i el reciclatge
són els ingredients principals!
</div>
""", unsafe_allow_html=True)

section_accent(2)
st.markdown("""
## La Festa Major Alternativa

Paral·lelament, al **Parc de l'Espanya Industrial**, l'assemblea del barri organitza la **Festa Major Alternativa**, amb tallers, concerts, xerrades i activitats de caràcter reivindicatiu i comunitari.
""")

section_accent(3)
st.markdown("""
## Carrers participants 2026

L'any 2026 participen **11 carrers i places** a la Festa Major de Sants, cadascun amb el seu propi tema de guarniment:

| Carrer / Plaça | Tema 2026 |
|---|---|
| **Carrer Papin** | L'Olimpíada Popular de Barcelona de 1936 |
| **Carrer d'Alcolea de Baix** | Disco Festival Sound — música, ball i festa de barri |
| **Carrer d'Alcolea de Dalt** | Circ Alcolea — espectacle i arts circenses |
| **Plaça de la Farga** | Artesania farguera i cultura del barri |
| **Carrer de Finlàndia** | 45è aniversari de la Comissió de Festes |
| **Carrer de Galileu** | Remember '70 '80 '90 — música i nostàlgia |
| **Carrer de Guadiana** | Comencem per les postres — dolços, salsa i festa galàctica |
| **Carrer de Sagunt** | Sagunt connectat — metro, música i comunitat |
| **Carrer de Valladolid** | Jules Verne — viatges, aventura i imaginació |
| **Carrer de Vallespir de Baix** | Versions i música en directe — cultura popular urbana |
| **Carrer de Vallespir de Dalt** | Nits de versions, rock i tradicions |

A més, els **Castellers de Sants** també organitzen activitats durant la festa.
""")

st.markdown("## Mapa dels carrers guarnits")
st.markdown(
    "Explora el mapa interactiu per trobar la ubicació exacta de tots els "
    "carrers participants i planificar la teva visita."
)
components.iframe(MAP_EMBED_URL, height=480)

section_accent(4)
st.markdown("""
## Dades pràctiques

- **Dates 2026:** Del 22 al 30 d'agost de 2026
- **Dia del patró:** 24 d'agost (Sant Bartomeu)
- **Barri:** Sants, districte de Sants-Montjuïc, Barcelona
- **Accés:** Metro L1 i L5 (Plaça de Sants), FGC (Plaça de Sants)
- **Programa oficial:** [Ajuntament de Barcelona](https://ajuntament.barcelona.cat/sants-montjuic/ca/festa-major-de-sants)
- **Guarniments 2026:** [Informació oficial dels guarniments](https://ajuntament.barcelona.cat/sants-montjuic/ca/noticies/els-guarniments-de-la-festa-major-de-sants-40324)
""")

section_accent(5)
st.markdown("""
## 📻 Sants 3 Ràdio, la ràdio de la festa

A partir del **22 d'agost**, **Sants 3 Ràdio** es converteix en la **ràdio de la Festa Major de Sants 2026**, que podràs escoltar al **103.2 FM**.

Trucant al número de la ràdio, **93 298 19 19**, pots votar:
- 🏆 El **millor guarnit** (millor carrer)
- 🎨 La **millor decoració de sostre**
""")

st.markdown("---")
st.caption("La Festa Major de Sants: on la comunitat, la creativitat i la festa es troben des de fa més d'un segle.")

section_accent(6)
st.markdown("""
## Activitats de la festa 2026

La Festa Major de Sants 2026 ofereix una programació molt diversa durant tota la setmana, amb cada carrer aportant la seva pròpia proposta temàtica:

### Cultura popular catalana
- **Castellers de Sants**: exhibicions de torres humanes i Diada Castellera (dissabte 29)
- **Correfoc**: infantil (Guspires de Sants i Diables de Castelldefels) i adult amb Diables de Sants (dissabte 29)
- **Gegants i capgrossos**, **sardanes**, **bastoneres** a la cercavila i actes unitaris

### Espectacles i concerts
- Concerts de tots els estils a cada carrer: rock, rumba, havaneres, versions, electrònica, salsa...
- Cinema a la fresca (Carrer Papin)
- Nit de monòlegs (Carrer Papin, dijous 27)
- Espectacles de carrer i pallassos

### Activitats familiars
- Jocs infantils, batalles ninja, gimcanes fotogràfiques
- Tallers creatius: graffiti, cianotipia, fang, serigrafia
- Fira del Benestar Animal (dijous 27, Vallespir de Dalt)
- Xocolatades i activitats per als més petits

### Gastronomia
- Sopars populars de germanor a cada carrer (botifarrada, paella, fideuà, arrossada...)
- Vermuts i tastos de productes locals
- Concursos de truites i de pastissos
- Barres de bar a cada carrer

### Actes unitaris
Alguns actes reuneixen tots els carrers participants:
- **Pregó de Festa Major** a càrrec de l'actriu Leticia Dolera (dissabte 22, Parc de l'Espanya Industrial)
- **Lliurament de premis del concurs de guarniment** (dilluns 24)
- **Lliurament dels Premis Populars** organitzat per Sants 3 Ràdio (dissabte 29, Carrer de Vallespir de Dalt)
- **Diada Castellera i Pilar caminant** dels Castellers de Sants (dissabte 29)
- **Correfoc** infantil i adult (dissabte 29)
- **Piromusical de cloenda** (diumenge 30, Parc de l'Espanya Industrial)
""")
