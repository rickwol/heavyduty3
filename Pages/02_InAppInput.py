import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px 
import datetime, timedelta
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title="Inappinvoer", page_icon="📈", initial_sidebar_state="collapsed")

st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)
#st.sidebar.header("Ritprofielen")

st.title("Heavy Duty Elektrificatie tool")


st.write("Vul hier het rittenpatroon in voor een gemiddelde dag")


st.write("Kies hier het type voertuig dat u wilt elektrificeren")

###overlay
radio_markdown = '''
De keuze voor uw voertuig en opties is belangrijk om het verbruik te bepalen.
Er wordt standaardwaardes voor specifieke voertuigen meegegeven.
Deze kunt u ook nog aanpassen
'''.strip()

###Keuze voertuig
voertuig = st.selectbox(
    '',
    ('Medium bakwagen lvm 12 - 18 ton', 'Grote bakwagen lvm > 18 ton', 'Lichte trekker z/opl gvm < 40 ton', "Zware trekker z/opl gvm > 40 ton"), help=radio_markdown)


optiesvoertuig =  st.selectbox("Welke andere energievebruikers heeft uw voertuig?",
                                        ("Geen", "Koeling", "Lift: Vuilnis", "Lift Anders"),
                               help=radio_markdown)
                                         

st.write("De keuzes voor uw voertuig en opties hangen samen met het energieverbruik")
st.write("Wilt u deze inzien en aanpassen, dan kan dit hieronder")
with st.expander("Zie specificaties"):
    st.write(voertuig)
    if voertuig == 'Medium bakwagen lvm 12 - 18 ton':
        tempverbruikvoertuig = 1.2
    elif voertuig =='Grote bakwagen lvm > 18 ton': 
        tempverbruikvoertuig = 1.1
    elif voertuig =='Lichte trekker z/opl gvm < 40 ton':
        tempverbruikvoertuig = 1
    else:
        tempverbruikvoertuig = 0.8
    
    
    verbruikvoertuig = st.number_input('Energieverbruik voertuig kWh/km', value= tempverbruikvoertuig)
    st.write(optiesvoertuig)
    if optiesvoertuig == "Koeling":
        verbruikopties  = st.number_input('Energieverbruik opties kWh/uur', value=0.8)
    elif optiesvoertuig == "Geen":
        verbruikopties  = st.number_input('Energieverbruik opties kWh/uur', value=0)       
    else: 
        verbruikopties = st.number_input('Energieverbruik opties kWh/keer', value=0.05)

###Store inputs in session state
if "voertuig" not in st.session_state:
    st.session_state.voertuig = verbruikvoertuig
if "opties" not in st.session_state:
    st.session_state.opties = verbruikopties

Aantalritten =  st.number_input('Hoeveel ritten op 1 dag?', step = 1, min_value= 3) -1

###Standaard Dataframe
df = pd.DataFrame(
    [
           {"Nummer rit": 1,"Starttijd Rit": "8:00", 'Eindtijd Rit' : "9:45", "Aantal kilometers": 10, "Kan laden op einde rit" : True, "Locatie einde rit: (Depot of Anders)" : "Depot"},
        {"Nummer rit": 2,"Starttijd Rit": "10:00", 'Eindtijd Rit' : "10:45", "Aantal kilometers": 75, "Kan laden op einde rit" : False, "Locatie einde rit: (Depot of Anders)" : "Depot"},
        {"Nummer rit": 3,"Starttijd Rit": "12:00", 'Eindtijd Rit' : "13:45", "Aantal kilometers": 175, "Kan laden op einde rit" : True, "Locatie einde rit: (Depot of Anders)" : "Depot"}
     
      
   ]
)  


###Bepaal aantal ritten
if(Aantalritten > 0):
    for z in range(Aantalritten):
        df = df.append({"Nummer rit": z+2,"Starttijd Rit": "8:00", 'Eindtijd Rit' : "9:45", "Aantal kilometers": 10, "Kan laden op einde rit" : True, "Locatie einde rit: (Depot of Anders)" : "Depot"}, ignore_index=True)

###Store dataframe in session state
if "df_value" not in st.session_state:
    st.session_state.df_value = df




        
###update df functie
def update(edited_df):
    for row_1, row_2, row_3, row_4, row_5, row_6 in zip(
        edited_df["Nummer rit"], edited_df["Starttijd Rit"], edited_df['Eindtijd Rit'], edited_df["Aantal kilometers"], edited_df["Kan laden op einde rit"], edited_df["Locatie einde rit: (Depot of Anders)"] 
    ):
        st.write(
            ""
        )
        
###Edit ritten
if df.equals(st.session_state["df_value"]): 
    edited_df = st.data_editor(df,key="editor",  num_rows="dynamic")
    
else:
    edited_df = st.data_editor(st.session_state["df_value"],key="editor",  num_rows="dynamic")

###Controleer of df zelfde als edited_Df ander supdate session state

                                                       

if edited_df is not None and not edited_df.equals(st.session_state["df_value"]):
    # This will only run if
    # 1. Some widget has been changed (including the dataframe editor), triggering a
    # script rerun, and
    # 2. The new dataframe value is different from the old value
    update(edited_df)
    st.session_state["df_value"] = edited_df

col1, col2, = st.columns(2)

with col1:
    if st.button("Vorige"):
        switch_page("input")
    
with col2:
    if st.button("Volgende"):
        switch_page("voertuig keuze")