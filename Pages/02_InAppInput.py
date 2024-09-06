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
    .reportview-container .main .block-container{{f"max-width: 1000px;"
    }}

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
        tempverbruikvoertuig = 0.8
    elif voertuig =='Grote bakwagen lvm > 18 ton': 
        tempverbruikvoertuig = 1
    elif voertuig =='Lichte trekker z/opl gvm < 40 ton':
        tempverbruikvoertuig = 1.1
    else:
        tempverbruikvoertuig = 1.2
    
    
    verbruikvoertuig = st.number_input('Energieverbruik voertuig kWh/km', value= tempverbruikvoertuig)
    st.write(optiesvoertuig)
    if optiesvoertuig == "Koeling":
        verbruikopties  = st.number_input('Energieverbruik koeling kWh/uur', value=6)
    elif optiesvoertuig == "Geen":
        st.text("Geen additioneel verbruik")    
        verbruikopties = 0
    else: 
        verbruikopties = st.number_input('Energieverbruik opties kWh/lift', value=0.5)
        Aantallifts = st.number_input('Aantal lifts per uur', value=10)
        

###Store inputs in session state
if "voertuig" not in st.session_state:
    st.session_state.voertuig = 1/verbruikvoertuig
    st.rerun()
if "opties" not in st.session_state:
    st.session_state.opties = verbruikopties
    st.rerun()
if "typevoertuig" not in st.session_state:
    st.session_state.typevoertuig = voertuig
    st.rerun()
    
#Aantalritten =  st.number_input('Hoeveel ritten op 1 dag?', step = 1, min_value= 5) -3
radio_markdown = '''
Er wordt een marge aangehouden om onvoorziene situaties mee te kunnen nemen (Standaard 10%) en om de veroudering van de batterij over de tijd mee te nemen (10%). Kleinere marges worden niet geadviseerd.
'''.strip()

###Store arge in session state
if "marge" not in st.session_state:
    st.session_state.marge = 20
    st.rerun()


marge2 = st.number_input("Hoeveel marge wilt u aanhouden voor u batterij capaciteit in procenten? De standaard waarde is 20%. Klik op het vraagteken voor meer informatie over de marge", value = st.session_state.marge, help=radio_markdown)

###Update session state op basis van input
if marge2 != st.session_state.marge:
    st.session_state.marge = marge2
    
    

###Standaard Dataframe
df = pd.DataFrame(
    [
           {"Nummer rit": 1,"Starttijd Rit": "8:00", 'Eindtijd Rit' : "9:45", "Aantal kilometers": 10, "Kan laden op einde rit" : True, "Locatie einde rit: (Depot of Anders)" : "Depot"},
        {"Nummer rit": 2,"Starttijd Rit": "10:00", 'Eindtijd Rit' : "10:45", "Aantal kilometers": 75, "Kan laden op einde rit" : False, "Locatie einde rit: (Depot of Anders)" : "Depot"},
        {"Nummer rit": 3,"Starttijd Rit": "12:00", 'Eindtijd Rit' : "13:45", "Aantal kilometers": 175, "Kan laden op einde rit" : True, "Locatie einde rit: (Depot of Anders)" : "Depot"},
         {"Nummer rit": 4,"Starttijd Rit": "15:00", 'Eindtijd Rit' : "16:00", "Aantal kilometers": 35, "Kan laden op einde rit" : True, "Locatie einde rit: (Depot of Anders)" : "Depot"},
        {"Nummer rit": 5,"Starttijd Rit": "16:10", 'Eindtijd Rit' : "17:00", "Aantal kilometers": 40, "Kan laden op einde rit" : True, "Locatie einde rit: (Depot of Anders)" : "Depot"},
     
      
   ]
)  


###Bepaal aantal ritten
#if(Aantalritten > 0):
 #   for z in range(Aantalritten):
  #      df = df.append({"Nummer rit": z+4,"Starttijd Rit": "8:00", 'Eindtijd Rit' : "9:45", "Aantal kilometers": 10, "Kan laden op einde #rit" : True, "Locatie einde rit: (Depot of Anders)" : "Depot"}, ignore_index=True)

###Store dataframe in session state
if "df_value" not in st.session_state:
    st.session_state.df_value = df
    st.rerun()




        
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
    st.rerun()

col1, col2, = st.columns(2)

with col1:
    if st.button("Vorige"):
        switch_page("input")
    
with col2:
    if st.button("Volgende"):
        switch_page("voertuig keuze")