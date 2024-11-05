import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px 
import datetime, timedelta
from streamlit_extras.switch_page_button import switch_page
from Functions import *

st.set_page_config(page_title="Ritprofielen", page_icon="📈", initial_sidebar_state="collapsed", layout="wide")

#st.sidebar.header("Ritprofielen")

####Header
from streamlit_navigation_bar import st_navbar

styles = {
    "nav": {
        "background-color": "#fab529",
        "height": "3.825rem",
        "font-size": "30px",
    }
}

st_navbar(
    pages=["Heavy Duty Elektrificatie Tool"],
    styles = styles
)

col5, col6, = st.columns([8, 1])

with col5: 
    ritdata = st.session_state.ritdata2
    st.write("Op deze pagina kunt u de technische specificaties naar uw wens aanpassen. Per voertuig staan reeds de berekende ideale waardes ingevuld.") 

    marge = st.session_state.marge

    verbruikkoeling = st.number_input("Energieverbruik koeling kWh/uur", value= 0.6 , key= "koeling")
    verbruiklift = st.number_input("Energieverbruik opties kWh/lift", value= 0.2, key= "lift")
    
    if st.session_state.laadkeuze != "'s nachts + tussentijds laden":
        ritdata = st.session_state["df_value"]
        ritdata["Kan laden op einde rit"] = "Nee"
        ritdata["Kan laden op einde rit"] = np.where((ritdata["VoertuigNr"].shift(-1) != ritdata["VoertuigNr"]), "Ja", ritdata["Kan laden op einde rit"])
        verbruik= st.session_state.marge
        ritdata, profiel, profielsum = RitDataMeerdere(ritdata, verbruik)
        
    col1, col2 = st.columns(2)

    voertuig ='Grote bakwagen lvm > 18 ton'
    #st.write(range(ritdata["VoertuigNr"].nunique()))
    with col1:
        for x in range(ritdata["VoertuigNr"].nunique()):
            ritdata2 = ritdata[ritdata["VoertuigNr"] == x+1].reset_index(drop=True)
            margemax = ritdata2["Accu"][0]-ritdata2["EnergieVerbruik"][0]+ritdata2["Energieextra"].sum()
            exec(f'verbruikvoertuig_{x} = 0') 
            #print(ritdata2["VoertuigNr"].min())
            if ritdata2["VoertuigNr"].min() % 2 != 0:
                voertuig = ritdata2["Type voertuig"][0]
                tekst = "Voor voertuig " + str(x+1)
                st.subheader(tekst)
                st.write(voertuig)
                with st.expander("Zie specificaties"):
                    #voertuig = ritdata2["Type voertuig"].min()
                    #st.write(voertuig)
                    if voertuig == 'Medium bakwagen lvm 12 - 18 ton':
                        exec(f'tempverbruikvoertuig_{x} = 1.2')
                    elif voertuig =='Grote bakwagen lvm > 18 ton': 
                        exec(f'tempverbruikvoertuig_{x} = 1.1')
                    elif voertuig =='Lichte trekker z/opl gvm < 40 ton':
                        exec(f'tempverbruikvoertuig_{x} = 1')
                    else:
                        exec(f'tempverbruikvoertuig_{x} = 0.8')
                    key = f"verbruik_input_{x}"
                    keyaccu = f"accu_input_{x}"
                    keylaad = f"laad_input_{x}" 
                    exec(f'verbruikvoertuig_{x} = st.number_input("Energieverbruik voertuig kWh/km", value= tempverbruikvoertuig_{x}, key= key)')
                    exec(f'accuvoertuig_{x} = st.number_input("Accu capaciteit (kWh)", value= np.round(margemax).astype(int), key= keyaccu)')
                    exec(f'laadvoertuig_{x} = st.number_input("Laadvermogen (kW)", value= np.round(ritdata2["laadsnelheid"].max()).astype(int), key= keylaad)')
                    ritdata6 = ritdata.copy()
                    exec(f'ritdata6.loc[ritdata["VoertuigNr"] == x+1, "Verbruik"] = verbruikvoertuig_{x}')
                    exec(f'ritdata6.loc[ritdata["VoertuigNr"] == x+1, "Accu"] = accuvoertuig_{x}')
                    exec(f'ritdata6.loc[ritdata["VoertuigNr"] == x+1, "laadsnelheid"] = laadvoertuig_{x}')
                    ritdata3, profiel, profielsum = RitDataMeerdereAanpassen(ritdata6, verbruiklift, verbruikkoeling)
                    ritdata4 = ritdata3[ritdata3["VoertuigNr"] == x+1].reset_index(drop=True)
                    margemax = ritdata4.KMber.max()*ritdata4["Verbruik"].max()*(marge/100)
                    if (ritdata4["Accu"]+ritdata4["EnergieVerbruik"].shift(-1)).min() < 0:
                        st.write(":red[Met deze combinatie van specificaties kunt u uw ritten **niet** uitvoeren]")
                    elif (ritdata4["Accu"]+ritdata4["EnergieVerbruik"].shift(-1)).min() < margemax:
                        st.write(":orange[Met deze combinatie van specificaties kunt u uw ritten uitvoeren maar heeft u minder veiligheidsmarge dan gewenst]")             
                    else:
                        st.write(":green[Met deze combinatie van specificaties kunt u uw ritten **wel** uitvoeren]")
                    if st.button("Bereken", key="button"+str(x)):
                        st.rerun()
                    #st.dataframe(ritdata4)
                    #st.write(margemax)
                    #st.write( (ritdata4["Accu"]+ritdata4["EnergieVerbruik"].shift(-1)).min())

    with col2:
        for x in range(ritdata["VoertuigNr"].nunique()):
            ritdata2 = ritdata[ritdata["VoertuigNr"] == x+1].reset_index(drop=True)
            margemax = ritdata2["Accu"][0]-ritdata2["EnergieVerbruik"][0]+ritdata2["Energieextra"].sum()
            exec(f'verbruikvoertuig_{x} = 0') 
            #print(ritdata2["VoertuigNr"].min())
            if ritdata2["VoertuigNr"].min() % 2 == 0:
                voertuig = ritdata2["Type voertuig"][0]
                tekst = "Voor voertuig " + str(x+1)
                st.subheader(tekst)
                st.write(voertuig)
                with st.expander("Zie specificaties"):
                    #voertuig = ritdata2["Type voertuig"].min()
                    #st.write(voertuig)
                    if voertuig == 'Medium bakwagen lvm 12 - 18 ton':
                        exec(f'tempverbruikvoertuig_{x} = 1.2')
                    elif voertuig =='Grote bakwagen lvm > 18 ton': 
                        exec(f'tempverbruikvoertuig_{x} = 1.1')
                    elif voertuig =='Lichte trekker z/opl gvm < 40 ton':
                        exec(f'tempverbruikvoertuig_{x} = 1')
                    else:
                        exec(f'tempverbruikvoertuig_{x} = 0.8')
                    key = f"verbruik_input_{x}"
                    keyaccu = f"accu_input_{x}"
                    keylaad = f"laad_input_{x}" 
                    exec(f'verbruikvoertuig_{x} = st.number_input("Energieverbruik voertuig kWh/km", value= tempverbruikvoertuig_{x}, key= key)')
                    exec(f'accuvoertuig_{x} = st.number_input("Accu capaciteit (kWh)", value= np.round(margemax).astype(int), key= keyaccu)')
                    exec(f'laadvoertuig_{x} = st.number_input("Laadvermogen (kW)", value= np.round(ritdata2["laadsnelheid"].max()).astype(int), key= keylaad)')
                    ritdata6 = ritdata.copy()
                    exec(f'ritdata6.loc[ritdata["VoertuigNr"] == x+1, "Verbruik"] = verbruikvoertuig_{x}')
                    exec(f'ritdata6.loc[ritdata["VoertuigNr"] == x+1, "Accu"] = accuvoertuig_{x}')
                    exec(f'ritdata6.loc[ritdata["VoertuigNr"] == x+1, "laadsnelheid"] = laadvoertuig_{x}')
                    ritdata3, profiel, profielsum = RitDataMeerdereAanpassen(ritdata6, verbruiklift, verbruikkoeling)
                    ritdata4 = ritdata3[ritdata3["VoertuigNr"] == x+1].reset_index(drop=True)
                    margemax = ritdata4.KMber.max()*ritdata4["Verbruik"].max()*(marge/100)
                    if (ritdata4["Accu"]+ritdata4["EnergieVerbruik"].shift(-1)).min() < 0:
                        st.write(":red[Met deze combinatie van specificaties kunt u uw ritten **niet** uitvoeren]")
                    elif (ritdata4["Accu"]+ritdata4["EnergieVerbruik"].shift(-1)).min() < margemax:
                        st.write(":orange[Met deze combinatie van specificaties kunt u uw ritten uitvoeren maar heeft u minder veiligheidsmarge dan gewenst]")             
                    else:
                        st.write(":green[Met deze combinatie van specificaties kunt u uw ritten **wel** uitvoeren]")
                    if st.button("Bereken", key="button"+str(x)):
                        st.rerun()
                    #st.dataframe(ritdata[ritdata["VoertuigNr"] == x+1].loc["Accu"])

    #st.write(accuvoertuig_1)             
    ritdata3, profiel, profielsum = RitDataMeerdereAanpassen(ritdata6, 0.2, 0.6)
    st.session_state.ritdata3 = ritdata3
    st.session_state.profielsum = profielsum


    col3, col4 = st.columns(2)
    with col3:
        if st.button("Vorige"):
            switch_page("meerdere voertuig keuze")

    with col4:
        if st.button("Volgende"):
            switch_page("laadprofiel")  
        
with col6:
    st.image("https://i.ibb.co/7QS71b5/Progressbar4.png", width=100)
    

###design footer
footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: black;
text-align: center;
}
</style>
<div class="footer">
<a href= "https://www.tno.nl"><img src="https://i.ibb.co/McjKv1z/TNOlogo.png", width="70" height="60"></a>
<a href= "https://www.nklnederland.nl"><img src="https://i.ibb.co/rfgPP7T/Logo-NKL-2022.png", width="70" height="60"></a>
<img src="https://i.ibb.co/K9nnLCx/design.png">
</div>
"""
st.markdown(footer,unsafe_allow_html=True)  


