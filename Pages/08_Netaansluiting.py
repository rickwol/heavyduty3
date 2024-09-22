import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px 
import datetime, timedelta
import requests
from datetime import date


download = requests.get("https://data.partnersinenergie.nl/capaciteitskaart/data/congestie_pc6.csv")
#today = date.today()
#d1 = today.strftime("%Y%m%d")
#csvname = "export_"+ d1 +".csv"
csvname = "congestie_pc6.csv"
if download.status_code == 200:
    # Save the content of the response to a local CSV file
    with open(csvname, "wb") as f:
        f.write(download.content)
congestiedatabase = pd.read_csv(csvname, delimiter = ";", decimal="," )
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
     if Congestie.iloc[0, 2] == 2:
         st.write("Momenteel is er op uw locatie", Postcode, "sprake van netcongestie. Er wordt specifiek onderzoek gedaan naar de mogelijkheden")
     if Congestie.iloc[0, 2] == 3 or Congestie.iloc[0, 2] == 3:
         st.write("Momenteel is er op uw locatie", Postcode, "sprake van netcongestie. U wordt in de wachtrij geplaatst. Neem contact met u netbeheerder voor meer informatie")
         st.write("Met mitigerende maatregelen kunt u uw benodigde netaansluiting terugbrengen tot: 3X80A. Hierdoor hoeft u niet lang te wachten op uitbreiding van uw aansluiting.") 


col3, col4 = st.columns(2)
with col3:
    if st.button("Vorige"):
        switch_page("laadprofiel")
with col4:
    if st.button("Volgende"):
        switch_page("overzicht")

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
<img src="https://i.ibb.co/sRP3VPm/design.png">
</div>
"""
st.markdown(footer,unsafe_allow_html=True)  
