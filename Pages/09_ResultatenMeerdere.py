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

# if "df_value" not in st.session_state:
#     if "df_meerdere" not in st.session_state:
#         ritdata = st.session_state["df_segment"]
#     else:
#         ritdata = st.session_state["df_meerdere"]
#         else:
#             ritdata = st.session_state["df_value"]

ritdata = st.session_state["df_value"]

radio_markdown = '''
Er wordt een marge aangehouden om onvoorziene situaties mee te kunnen nemen (Standaard 10%) en om de veroudering van de batterij over de tijd mee te nemen (10%). Veel kleinere marges worden niet geadviseerd.
'''.strip()
marge = st.number_input("Hoeveel marge wilt u aanhouden voor u batterij capaciteit in procenten? De standaard waarde is 20%", value = 20, help=radio_markdown)

ritdata, profiel, profielsum = RitDataMeerdere(ritdata, marge)

profielsum.laadsnelheid.max()

st.write("Op basis van uw input zijn dit twee mogelijke laadstrategieën met configuraties van uw trucks")
radio_markdown = '''
Maak uw keuze uit twee laadstrategieën
1. Depot Laden: U laad uw voertuigen alleen na de laatste rit op de dag. In de tool wordt er vanuit gegaan dat de tijd voldoende is om de volgende weer volledig opgeladen te zijn. De range van de truck moet voldoende zijn om alle ritten op de dag te doen.
2. Frequent Laden: Bij deze strategie kiest u ervoor om ook op stops op het depot op te laden. Alleen stops van 20 minuten of langer worden meegenomen. 
'''.strip()

#st.sidebar.header("Ritprofielen")



###Keuze voertuig



st.text("Gebruik deze input voor een verkenning van welke specifieke truck dit kan zijn in de ZETI tool:")
url = "https://globaldrivetozero.org/tools/zeti/"
st.write("Klik [hier](%s) voor de tool" % url)

col1, col2, = st.columns(2)



with col1:
    st.header("Alleen depot laden")
    st.image("https://media.istockphoto.com/id/1306857153/nl/foto/het-laadstation-van-elektrische-voertuigen-op-een-achtergrond-van-een-vrachtwagen.jpg?s=612x612&w=0&k=20&c=kF5jroBqGmPsn_6zup2ahw1R2W6xNb6dNibQqlf-KGM=")
    for x in range(ritdata["VoertuigNr"].nunique()):
        ritdata2 = ritdata[ritdata["VoertuigNr"]==x+1].reset_index(drop=True)
        ###Verbruik vaststellen
        verbruik = ritdata2["Verbruik"][0]

        rit1 =  ritdata2["KM"].head(1)
        if ritdata2["KM"].shape[0]>1:
            andereritten = ritdata2["KM"].tail(-1).max()#/0.8
        else:
            andereritten = rit1
        kilometers = float(np.maximum(rit1, andereritten)) ###Maximum van alle ritten
        kilomterssom = ritdata2["KM"].sum() ###Totaalkilometers
        energieonderweg = int(kilometers/(1-(marge/100)) * verbruik)
        energiedepot = int(kilomterssom/(1-(marge/100)) * verbruik)
        oplaaddepot = int(energiedepot/8)
        tekst = "Voor voertuig " + str(x+1)
        st.subheader(tekst)
        st.write("Accu:", str(np.round(energiedepot)), "kWh")
        st.write("Range:", str(np.round(kilomterssom)), "km")
        st.write("Oplaadcapaciteit: ", str(oplaaddepot), "kW")
        

with col2:
    st.header("Frequent laden")
    st.image("https://media.istockphoto.com/id/1306857153/nl/foto/het-laadstation-van-elektrische-voertuigen-op-een-achtergrond-van-een-vrachtwagen.jpg?s=612x612&w=0&k=20&c=kF5jroBqGmPsn_6zup2ahw1R2W6xNb6dNibQqlf-KGM=")
    for x in range(ritdata["VoertuigNr"].nunique()):
        ritdata2 = ritdata[ritdata["VoertuigNr"]==x+1].reset_index(drop=True)
        ###Verbruik vaststellen
        verbruik = ritdata2["Verbruik"][0]
        
        rit1 =  ritdata2["KM"].head(1)
        if ritdata2["KM"].shape[0]>1:
            andereritten = ritdata2["KM"].tail(-1).max()#/0.8
        else:
            andereritten = rit1
        kilometers = ritdata2.KMber.max() ###Maximum van alle ritten
        kilomterssom = ritdata["KM"].sum() ###Totaalkilometers
        energieonderweg = int(kilometers/(1-(marge/100)) * verbruik)
        energiedepot = int(kilomterssom/(1-(marge/100)) * verbruik)
        oplaaddepot = int(np.round(ritdata2["laadsnelheid"].tail(1)))
        tekst = "Voor voertuig " + str(x+1)
        st.subheader(tekst)
        st.write("Accu:", str(np.round(ritdata2["Accu"].max())), "kWh")
        st.write("Range:", str(np.round(ritdata2["Accu"].max()/ritdata2["Verbruik"].max())),"km")
        st.write("Oplaadcapaciteit: ", str(int(np.round(ritdata2["laadsnelheid"].max()))), "kW")

truckinput = st.radio(
    'Kies hier uw laadstrategie',
    ('Depot laden                 ', 'Frequent laden'),horizontal = True, help=radio_markdown)

col3, col4, = st.columns(2)

with col3:
    if st.button("Vorige"):
        switch_page("ritprofiel_gemiddeld")
    
with col4:
    if st.button("Volgende"):
        switch_page("opties")  
    

        
if truckinput == 'Frequent laden':
  profielsum = profielsum
else:
    oplaaddepotsum = 0
    for x in range(ritdata["VoertuigNr"].nunique()):
        ritdata2 = ritdata[ritdata["VoertuigNr"]==x+1]
        rit1 =  ritdata2["KM"].head(1)
        if ritdata2["KM"].shape[0]>1:
            andereritten = ritdata2["KM"].tail(-1).max()#/0.8
        else:
            andereritten = rit1
        kilometers = float(np.maximum(rit1, andereritten)) ###Maximum van alle ritten
        kilomterssom = ritdata2["KM"].sum() ###Totaalkilometers
        energieonderweg = int(kilometers/(1-(marge/100)) * verbruik)
        energiedepot = int(kilomterssom/(1-(marge/100)) * verbruik)
        oplaaddepot = int(energiedepot/8)
        oplaaddepotsum = oplaaddepotsum + oplaaddepot
        
    profielsum  = pd.DataFrame.from_dict({"Tijdlijst" : [0]})
    profielsum["Tijdlijst"][0]  = list(pd.date_range("1900-01-01 0:00", "1900-01-02 05:05" ,freq='5T'))
    profielsum = pd.DataFrame(profielsum.explode(["Tijdlijst"]).reset_index())
    timemax = str(ritdata["Starttime"].max())
    profielsum["laadsnelheid"] = np.where(profielsum["Tijdlijst"] > timemax, oplaaddepotsum, 0)
    profielsum["laadsnelheid"] = np.where(profielsum["Tijdlijst"] > "1900-01-02 05:00", 0, profielsum["laadsnelheid"] )
    
    


st.session_state.marge= marge    
st.session_state.ritdata2 = ritdata
st.session_state.profielsum = profielsum
st.session_state.laadkeuze = truckinput