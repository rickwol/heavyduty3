import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px 
import datetime, timedelta
from streamlit_extras.switch_page_button import switch_page
from Functions2 import *

st.set_page_config(page_title="Ritprofielen", page_icon="📈", initial_sidebar_state="collapsed")
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

# if "df_value" not in st.session_state:
#     if "df_meerdere" not in st.session_state:
#         ritdata = st.session_state["df_segment"]
#     else:
#         ritdata = st.session_state["df_meerdere"]
#         else:
#             ritdata = st.session_state["df_value"]

ritdata = st.session_state["df_value"]

ritdata = RitDataEnkele(ritdata, st.session_state.voertuig)
                                    
rit1 =  ritdata["Aantal kilometers"].head(1)
if ritdata["Aantal kilometers"].shape[0]>1:
    andereritten = ritdata["KM"].tail(-1).max()#/0.8
else:
    andereritten = rit1
kilometers = float(np.maximum(rit1, andereritten)) ###Maximum van alle ritten

kilomterssom = ritdata["Aantal kilometers"].sum() ###Totaalkilometers

energieonderweg = int(kilometers/0.7 * st.session_state.voertuig)
energiedepot = int(kilomterssom/0.7 * st.session_state.voertuig)

oplaaddepot = int(np.round(ritdata["laadsnelheid"].tail(1)))

st.dataframe(ritdata)

st.write("Op basis van uw input zijn dit twee trucks in combinatie met laadpalen afhankelijk van de laadstrategie")

col1, col2, col3, = st.columns(3)

with col1:
    st.header("Alleen depot laden")
    st.image("https://media.istockphoto.com/id/1306857153/nl/foto/het-laadstation-van-elektrische-voertuigen-op-een-achtergrond-van-een-vrachtwagen.jpg?s=612x612&w=0&k=20&c=kF5jroBqGmPsn_6zup2ahw1R2W6xNb6dNibQqlf-KGM=")
    st.write("Accu:", str(np.round(energiedepot)), "kWh")
    st.write("Range:", str(np.round(kilomterssom)), "km")
    st.write("Oplaadcapaciteit: ", str(oplaaddepot), "kW")
with col2:
    st.header("Frequent laden")
    st.image("https://media.istockphoto.com/id/1306857153/nl/foto/het-laadstation-van-elektrische-voertuigen-op-een-achtergrond-van-een-vrachtwagen.jpg?s=612x612&w=0&k=20&c=kF5jroBqGmPsn_6zup2ahw1R2W6xNb6dNibQqlf-KGM=")
    st.write("Accu:", str(np.round(energieonderweg)), "kWh")
    st.write("Range:", str(np.round(kilometers)),"km")
    st.write("Oplaadcapaciteit: ", str(int(np.round(ritdata["laadsnelheid"].max()))), "kW")

radio_markdown = '''
Maak uw keuze uit twee laadstrategieën
1. Depot Laden: U laad uw voertuigen alleen na de laatste rit op de dag. In de tool wordt er vanuit gegaan dat de tijd voldoende is om de volgende weer volledig opgeladen te zijn. De range van de truck moet voldoende zijn om alle ritten op de dag te doen.
2. Frequent Laden: Bij deze strategie kiest u ervoor om ook op stops op het depot op te laden. Alleen stops van 20 minuten of langer worden meegenomen. 
'''.strip()

#st.sidebar.header("Ritprofielen")



###Keuze voertuig
truckinput = st.radio(
    'Kies hier uw laadstrategie',
    ('Depot laden                 ', 'Frequent laden'),horizontal = True, help=radio_markdown)


st.text("Gebruik deze input voor een verkenning van welke specifieke truck dit kan zijn in de ZETI tool:")
url = "https://globaldrivetozero.org/tools/zeti/"
st.write("Klik [hier](%s) voor de tool" % url)

#truckinput = st.selectbox("Welke optie kiest u?", ("Alleen depot laden",  "Frequent laden"))

st.write("Afhankelijk van uw laadstrategie nemen we uw voertuigspecificaties mee. Wilt uw toch iets anders invullen dan kan dit hieronder")
with st.expander("Zie specificaties"):
    accu = st.number_input('Accu (kWh)', value= energiedepot)
    accu = st.number_input('Oplaadvermogen (kW)', value= oplaaddepot)

    
    
if st.button("Volgende"):
    switch_page("laadprofiel")
