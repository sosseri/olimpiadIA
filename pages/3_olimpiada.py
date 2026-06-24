import streamlit as st

st.set_page_config(page_title="L'Olimpíada Popular de Barcelona 1936", page_icon="🏟️", layout="centered")

st.markdown("""
<style>
    .olimp-header {
        background: linear-gradient(135deg, #4a148c 0%, #880e4f 50%, #b71c1c 100%);
        border-radius: 16px; padding: 1.5rem; text-align: center; color: #fff;
        margin-bottom: 1.5rem; box-shadow: 0 2px 10px rgba(0,0,0,0.15);
    }
    .olimp-header h1 { margin: 0; font-size: 1.5rem; }
    .olimp-header p { margin: 0.3rem 0 0; font-size: 0.95rem; opacity: 0.9; }
    .timeline-item {
        border-left: 3px solid #880e4f; padding: 0.8rem 1rem; margin: 0.5rem 0;
        background: #fce4ec; border-radius: 0 8px 8px 0;
    }
    .timeline-date { font-weight: 700; color: #880e4f; }
    .quote-box {
        background: #f3e5f5; border-left: 4px solid #4a148c;
        padding: 1rem; border-radius: 0 8px 8px 0; margin: 1rem 0;
        font-style: italic;
    }
    .source-note {
        font-size: 0.8rem; color: #888; margin-top: 0.3rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="olimp-header">
    <h1>🏟️ L'Olimpíada Popular de Barcelona de 1936</h1>
    <p>L'esport contra el feixisme — El tema del Carrer Papin 2026</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
## L'alternativa antifeixista als Jocs de Hitler

L'any 1936, el règim nazi d'Adolf Hitler va organitzar els **Jocs Olímpics de Berlín** com una enorme operació de propaganda. Volia mostrar al món la suposada superioritat de la "raça ària". El Comitè Olímpic Internacional (COI) va mantenir Berlín com a seu malgrat les protestes internacionals.

Davant d'aquesta instrumentalització de l'esport, van sorgir **moviments de boicot** arreu del món. Organitzacions obreres, partits d'esquerres i esportistes van demanar que no es participés als Jocs de Berlín. La resposta va prendre forma a Barcelona.
""")

st.markdown("""
## L'Olimpíada Popular: l'esport del poble

Com a alternativa, el **Comitè Català pro Esport Popular** — amb el suport del govern de la **República Espanyola**, la **Generalitat de Catalunya** presidida per **Lluís Companys** i el govern del **Front Popular francès** — va organitzar una competició esportiva oberta i antifeixista. Era "l'acte més important del moviment internacional contra la instrumentalització dels Jocs de Berlín pel règim nazi."

**Dades clau:**
- **Seu:** Estadi de Montjuïc, Barcelona
- **Dates previstes:** 19–26 de juliol de 1936
- **Atletes inscrits:** ~6.000 de 20 a 23 delegacions
- **Finançament:** 250.000 pessetes (República), 100.000 (Generalitat), 600.000 (França)
- **Formats:** Nacional, regional i local — permetia equips d'Alsàcia, Galícia, Euskadi, Algèria, Palestina i exiliats alemanys i italians antifeixistes
- **Caràcter:** Esport + folklore ("setmana popular de l'esport i el folklore")
""")

st.markdown("""
<div class="quote-box">
"L'Olimpíada Popular volia recuperar el veritable esperit olímpic, la pau i la solidaritat entre les nacions."
<div class="source-note">Arxiu Nacional de Catalunya / patrimoni.gencat.cat</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
## Un projecte que anava més enllà de l'esport

L'Olimpíada incloïa un **programa cultural ampli**: concerts, exposicions d'art, representacions teatrals i conferències. Uns 3.000 participants addicionals estaven previstos en activitats folklòriques, incloent-hi la **Patum de Berga**. Es va posar especial èmfasi en la **participació femenina**, en un moment en què les dones tenien dificultats per accedir a l'esport en igualtat de condicions.

Les delegacions incloïen França, Regne Unit, Estats Units, Bèlgica, Holanda, Suïssa, Noruega, Suècia, Dinamarca, Txecoslovàquia, Canadà, Algèria i Palestina. Destacaven especialment les delegacions d'**exiliats alemanys i italians antifeixistes**, que no podien competir sota les seves banderes nacionals.
""")

st.markdown("## Cronologia")

events = [
    ("1931", "Olimpíada Obrera a Viena: precedent directe de l'Olimpíada Popular, amb esportistes d'esquerres de tot Europa."),
    ("1933–1935", "Hitler arriba al poder. El COI confirma Berlín com a seu olímpica malgrat les protestes internacionals."),
    ("Primavera 1936", "Es constitueix el Comitè Català pro Esport Popular a Barcelona. Lluís Companys en serà president honorari. Comencen les inscripcions massives."),
    ("Juliol 1936", "Atletes de 20 a 23 delegacions arriben a Barcelona. A la ciutat hi ha uns 20.000 visitants. L'ambient és d'entusiasme i esperança."),
    ("18 de juliol de 1936", "Pablo Casals assaja la Novena Simfonia de Beethoven al Teatre Grec de Montjuïc per a la cerimònia d'inauguració. Aquella nit arriba la notícia: cop d'estat militar."),
    ("19 de juliol de 1936", "El dia de la inauguració prevista. Els atletes es desperten amb el so de les canonades del barri del Paral·lel. L'Olimpíada Popular no es celebra."),
    ("19–21 de juliol 1936", "La majoria d'atletes marxen a Marsella en un vaixell noliejat. Però entre 200 i 600 atletes decideixen quedar-se i s'uneixen a les milícies antifeixistes. Entre ells, Clara Thalmann (nedadora suïssa, Columna Durruti) i María Ginestà (corredora, milícies socialistes)."),
    ("1 d'agost de 1936", "S'inauguren els Jocs Olímpics de Berlín. Jesse Owens guanya 4 medalles d'or, contradient la propaganda ària de Hitler."),
    ("1936–1939", "Guerra Civil Espanyola. Molts dels atletes que van quedar-se lluitaran a les Brigades Internacionals. La República cau el 1939."),
]

for ev_date, ev_desc in events:
    st.markdown(f"""
    <div class="timeline-item">
        <div class="timeline-date">{ev_date}</div>
        <div>{ev_desc}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
## La Guerra Civil i la fi d'un somni

El cop d'estat del 17–18 de juliol de 1936 no només va destruir l'Olimpíada Popular, sinó que va iniciar una guerra de tres anys. La República, defensada per obrers, sindicalistes i voluntaris internacionals de les Brigades Internacionals, va caure el 1939 davant les forces de Franco, recolzades per l'Alemanya nazi i la Itàlia feixista.

L'esperit de solidaritat que havia motivat l'Olimpíada Popular es va transformar en lluita armada. **Entre 200 i 600 atletes** van renunciar a tornar a casa i van agafar les armes — un dels capítols més emotius de la solidaritat internacional antifeixista del segle XX.
""")

st.markdown("""
<div class="quote-box">
"Mentre assajàvem l'himne immortal de la fraternitat, escoltàvem el tro dels canons a la llunyania."
<div class="source-note">Pablo Casals, 18 de juliol de 1936 — vscw.ca / wanderer.es</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
## Llegat

L'Olimpíada Popular de Barcelona de 1936 és recordada com el **gest de protesta esportiva internacional més important contra el nazisme**. El seu llegat viu en la memòria dels atletes que van fer la tria més difícil, en l'ideal d'un esport obert a tothom sense distinció de raça, nació o classe, i en la convicció que la cultura i l'esport poden ser eines de resistència contra la barbàrie.

El Carrer Papin li dedica el guarnit de 2026 — 90 anys després.
""")

st.markdown("---")

st.markdown("""
## Per saber-ne més

**Fonts documentals:**
- [Arxiu Patrimonial de la Generalitat de Catalunya](https://patrimoni.gencat.cat/es/catalunyapaisdarxius/recurso-digital/recurso/document/programa-de-lolimpiada-popular-de-barcelona/) — Programa oficial de l'Olimpíada Popular (AHCB)
- [Betevé — Va Passar Aquí](https://beteve.cat/va-passar-aqui/olimpiada-popular-cadci-1936/) — L'Olimpíada Popular i el CADCI
- [Nou Barris per la República](https://noubarrisperlarepublica.org/cas/herramientas-republicanas/cultura-cas/la-olimpiada-popular-del-36/) — La Olimpiada Popular del 36
- [VSCW.ca — Volunteers for the Spanish Civil War](https://vscw.ca/es/node/783) — Atletes que van quedar-se a lluitar
- [Wanderer.es](https://www.wanderer.es/barcelona-la-olimpiada-popular-que-quiso-derrotar-a-hitler/) — Barcelona, la Olimpiada Popular que quiso derrotar a Hitler
- [Wikipedia — Olimpiada Popular](https://es.wikipedia.org/wiki/Olimpiada_Popular)

**Llibres:**
- *L'Olimpíada Popular de Barcelona* — Xavier Pujadas i Carles Santacana (estudi acadèmic de referència)
- *Homenatge a Catalunya* — George Orwell (testimoni de primera mà de la Guerra Civil)

**Pel·lícules:**
- *Tierra y Libertad* (1995, Ken Loach) — voluntari britànic a la Guerra Civil
- *Libertarias* (1996, Vicente Aranda) — dones anarquistes durant la guerra
""")

st.markdown("---")
st.caption("El carrer Papin dedica el guarnit de 2026 a la memòria de l'Olimpíada Popular i de totes les persones que van lluitar contra el feixisme.")
