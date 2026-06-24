import streamlit as st

st.set_page_config(page_title="Festa Major de Sants", page_icon="🎭", layout="centered")

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

st.markdown("""
## Orígens

La **Festa Major de Sants** és una de les festes de barri més importants i emblemàtiques de Barcelona. Les seves arrels es remunten a mitjans del **segle XIX**, quan **Santa Maria de Sants** era encara un municipi independent, separat de Barcelona.

La festa se celebra al voltant del **24 d'agost**, festivitat de **Sant Bartomeu**, patró de l'antiga parròquia de Sants. Les primeres celebracions consistien en balls, cercaviles, actes religiosos i activitats populars.
""")

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

st.markdown("""
## Activitats de la festa

La Festa Major de Sants ofereix una programació molt diversa durant tota la setmana:

### Cultura popular catalana
- **Castellers**: exhibicions de torres humanes
- **Correfocs**: cercaviles de foc amb diables i dracs
- **Gegants i capgrossos**: figures gegants que desfilen pels carrers
- **Sardanes**: balls tradicionals catalans
- **Bastoneres**: danses amb bastons

### Espectacles i concerts
- Concerts de tots els estils: rock, punk, ska, rumba, electrònica, havaneres...
- Cinema a la fresca
- Nits de monòlegs i humor
- Espectacles de carrer

### Activitats familiars
- Jocs infantils i tradicionals
- Tallers creatius
- Gimcanes i concursos
- Pintacares i activitats per als més petits

### Gastronomia
- Sopars populars (botifarrada, arrossada, paella...)
- Tastos de productes locals
- Vermuts i xocolatades
- Barres de bar a cada carrer

### Actes unitaris
Alguns actes reuneixen tots els carrers participants:
- **Pregó de Festa Major** al Parc de l'Espanya Industrial
- **Lliurament de premis** del concurs de guarniment
- **Diada Castellera**
- **Correfoc** (infantil i adult)
- **Piromusical de cloenda** per tancar la festa
""")

st.markdown("""
## La Festa Major Alternativa

Paral·lelament, al **Parc de l'Espanya Industrial**, l'assemblea del barri organitza la **Festa Major Alternativa**, amb tallers, concerts, xerrades i activitats de caràcter reivindicatiu i comunitari.
""")

st.markdown("""
## Carrers participants

Habitualment participen **11 carrers i places** a la Festa Major de Sants:

1. Carrer Papin
2. Carrer d'Alcolea de Baix
3. Carrer d'Alcolea de Dalt
4. Plaça de la Farga
5. Carrer de Finlàndia
6. Carrer de Galileu
7. Carrer de Guadiana
8. Carrer de Sagunt
9. Carrer de Valladolid
10. Carrer de Vallespir de Baix
11. Carrer de Vallespir de Dalt

A més, els **Castellers de Sants** també organitzen activitats durant la festa.
""")

st.markdown("""
## Dades pràctiques

- **Dates 2026:** Del 22 al 30 d'agost
- **Dia del patró:** 24 d'agost (Sant Bartomeu)
- **Barri:** Sants, districte de Sants-Montjuïc, Barcelona
- **Accés:** Metro L1 i L5 (Plaça de Sants), FGC (Plaça de Sants)
- **Programa oficial:** [Ajuntament de Barcelona](https://ajuntament.barcelona.cat/sants-montjuic/ca/festa-major-de-sants)
""")

st.markdown("---")
st.caption("La Festa Major de Sants: on la comunitat, la creativitat i la festa es troben des de fa més d'un segle.")
