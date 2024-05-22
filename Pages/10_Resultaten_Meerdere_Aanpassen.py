import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px 
import datetime, timedelta
from streamlit_extras.switch_page_button import switch_page
from Functions import *

st.set_page_config(page_title="Ritprofielen", page_icon="📈", initial_sidebar_state="collapsed")

#st.sidebar.header("Ritprofielen")

st.title("Heavy Duty Elektrificatie tool")

ritdata = st.session_state.ritdata2
st.write("Op deze pagina kunt u de technische specificaties naar uw wens aanpassen. Per voertuig staan reeds de berekende ideale waardes ingevuld.") 
#st.dataframe(ritdata)
#st.dataframe(ritdata)
col1, col2 = st.columns(2)

voertuig ='Grote bakwagen lvm > 18 ton'
#st.write(range(ritdata["VoertuigNr"].nunique()))
with col1:
    for x in range(ritdata["VoertuigNr"].nunique()):
        ritdata2 = ritdata[ritdata["VoertuigNr"] == x+1].reset_index(drop=True)
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
                exec(f'accuvoertuig_{x} = st.number_input("Accu capaciteit (kWh)", value= np.round(ritdata2["Accu"].max()).astype(int), key= keyaccu)')
                exec(f'laadvoertuig_{x} = st.number_input("Laadsnelheid (kW)", value= np.round(ritdata2["laadsnelheid"].max()).astype(int), key= keylaad)')
                exec(f'ritdata.loc[ritdata["VoertuigNr"] == x+1, "Verbruik"] = verbruikvoertuig_{x}')
                exec(f'ritdata.loc[ritdata["VoertuigNr"] == x+1, "Accu"] = accuvoertuig_{x}')
                exec(f'ritdata.loc[ritdata["VoertuigNr"] == x+1, "laadsnelheid"] = laadvoertuig_{x}')
                ritdata3, profiel, profielsum = RitDataMeerdereAanpassen(ritdata)
                ritdata4 = ritdata3[ritdata3["VoertuigNr"] == x+1].reset_index(drop=True)
                if ritdata4["Accu"].min() < 0:
                    st.write(":red[Met deze combinatie van specificaties kunt u uw ritten **niet** uitvoeren]")
                else:
                    st.write(":green[Met deze combinatie van specificaties kunt u uw ritten **wel** uitvoeren]")
        
with col2:
    for x in range(ritdata["VoertuigNr"].nunique()):
        ritdata2 = ritdata[ritdata["VoertuigNr"] == x+1].reset_index(drop=True)
        #exec(f'verbruikvoertuig_{x} = 0') 
        #print(ritdata2["VoertuigNr"].min())
        if ritdata2["VoertuigNr"].min() % 2 == 0:
            tekst = "Voor voertuig " + str(x+1)
            st.subheader(tekst)
            voertuig = ritdata2["Type voertuig"][0]
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
                exec(f'accuvoertuig_{x} = st.number_input("Accu capaciteit (kWh)", value= np.round(ritdata2["Accu"].max()).astype(int), key= keyaccu )')
                exec(f'laadvoertuig_{x}  = st.number_input("Laadsnelheid (kW)", value= np.round(ritdata2["laadsnelheid"].max()).astype(int), key= keylaad)')
                exec(f'ritdata.loc[ritdata["VoertuigNr"] == x+1, "Verbruik"] = verbruikvoertuig_{x}')
                exec(f'ritdata.loc[ritdata["VoertuigNr"] == x+1, "Accu"] = accuvoertuig_{x}')
                exec(f'ritdata.loc[ritdata["VoertuigNr"] == x+1, "laadsnelheid"] = laadvoertuig_{x}')
                ritdata3, profiel, profielsum = RitDataMeerdereAanpassen(ritdata)
                ritdata4 = ritdata3[ritdata3["VoertuigNr"] == x+1].reset_index(drop=True)
                if ritdata4["Accu"].min() < 0:
                    st.write(":red[Met deze combinatie van specificaties kunt u uw ritten **niet** uitvoeren]")
                else:
                    st.write(":green[Met deze combinatie van specificaties kunt u uw ritten **wel** uitvoeren]")
                #st.dataframe(ritdata[ritdata["VoertuigNr"] == x+1].loc["Accu"])
                
#st.write(accuvoertuig_1)             
#st.dataframe(ritdata)
ritdata3, profiel, profielsum = RitDataMeerdereAanpassen(ritdata)
st.session_state.ritdata3 = ritdata3
st.experimental_rerun()
st.session_state.profielsum = profielsum
st.experimental_rerun()

col3, col4 = st.columns(2)
with col3:
    if st.button("Vorige"):
        switch_page("ritprofiel_gemiddeld")
    
with col4:
    if st.button("Volgende"):
        switch_page("laadprofiel")  