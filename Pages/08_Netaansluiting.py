import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px 
import datetime, timedelta
import requests
from datetime import date

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

download = requests.get("https://capaciteitskaart.netbeheernederland.nl/dashboard/download")
today = date.today()
d1 = today.strftime("%Y%m%d")
csvname = "export_"+ d1 +".csv"
if download.status_code == 200:
    # Save the content of the response to a local CSV file
    with open(csvname, "wb") as f:
        f.write(download.content)
congestiedatabase = pd.read_csv(csvname)
#congestiedatabase = pd.read_csv("data2/netcongestie.csv")
#st.sidebar.header("Ritprofielen")

st.title("Heavy Duty Elektrificatie tool")


st.write("Wat is uw huidige netaansluiting?")


Netaansluiting=  st.selectbox(options = ["3X25A", "3X35A", "3X40A", "3X63A", "3X80A", "<175MVA", "< 500MVA"], label = "Selecteer uit lijst")
st.write("Wat is uw postcode waarop uw bedrijf is gevestigd?")

radio_markdown = '''
Data komt uit de netcongestiekaart van netbeheer Nederland.
Neem altijd contact op met uw netbeheerder om te zien wat er precies mogelijk is. 
'''.strip()

Postcode = st.text_input(label = "Postcode", placeholder= "1011AA", help=radio_markdown)

Postcode = Postcode.replace(" ", "").upper()
Congestie = congestiedatabase[congestiedatabase["postcode"] == Postcode]

st.write("Op basis van uw ritprofiel en het verwachte aantal trucks moet u uw netaansluiting uitbreiden naar minimaal: <175MVA") 

if (Postcode == "") :
    st.write("U heeft nog geen postcode ingevoerd of de postcode is onbekend") 
else:
     if Congestie.iloc[0, 2] == 0:
        st.write("Momenteel is er op uw locatie", Postcode, "geen sprake van netcongestie. Er is ook voor de komende termijn voldoende capaciteit beschikbaar")
     if Congestie.iloc[0, 2] == 1:
         st.write("Momenteel is er op uw locatie", Postcode, "geen sprake van netcongestie. Maar aansluitingen zien wel beperkt. Neem contact op met uw netbeheerder voor details")
     if Congestie.iloc[0, 2] == 2 or Congestie.iloc[0, 2] == 3:
         st.write("Momenteel is er op uw locatie", Postcode, "sprake van netcongestie. Naar verwachting kunt u deze netaansluting pas in 2026 verkrijgen")
         st.write("Met mitigerende maatregelen kunt u uw benodigde netaansluiting terugbrengen tot: 3X80A. Hierdoor hoeft u niet lang te wachten op uitbreiding van uw aansluiting.") 


         

