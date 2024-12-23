import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px 
import datetime, timedelta
import requests
from datetime import date
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title="Netaansluiting", page_icon="📈", initial_sidebar_state="collapsed", layout="wide")

download = requests.get("https://data.partnersinenergie.nl/capaciteitskaart/data/congestie_pc6.csv")
#today = date.today()
#d1 = today.strftime("%Y%m%d")
#csvname = "export_"+ d1 +".csv"
csvname = "congestie_pc6.csv"
if download.status_code == 200:
    # Save the content of the response to a local CSV file
    with open(csvname, "wb") as f:
        f.write(download.content)
congestiedatabase = pd.read_csv(csvname, delimiter = ";", decimal=",")
#congestiedatabase = pd.read_csv("data2/netcongestie.csv")
#st.sidebar.header("Ritprofielen")

####Header
from streamlit_navigation_bar import st_navbar

styles = {
    "nav": {
        "background-color": "#fab529",
        "height": "4rem",
        "font-size": "40px",
        "justify-content": "left"
    }
}


st_navbar(
    pages=["Heavy Duty Elektrificatie Tool"],
    styles = styles
)
col5, col6, = st.columns([8, 1])

with col5: 

    st.write("Wat is uw huidige netaansluiting?")


    Netaansluiting=  st.selectbox(options = ["3X25A", "3X35A", "3X40A", "3X63A", "3X80A", "<175kVA", "< 500kVA", "> 500 kVA"], label = "Selecteer uit lijst")
    st.write("Wat is uw postcode waarop uw bedrijf is gevestigd?")

    if Netaansluiting == "3X25A":
        vermogen = 17.5
    elif Netaansluiting == "3X35A":
        vermogen = 22.5
    elif Netaansluiting == "3X40A":
        vermogen = 26
    elif Netaansluiting == "3X63A":
        vermogen = 35
    elif Netaansluiting == "3X80A":
        vermogen = 50
    elif Netaansluiting == "<175kVA":
        vermogen = 175
    else:
        vermogen = 500

    vermogen = vermogen + st.session_state.maxvermogen

    vermogencat = 17.5

    if vermogen < 17.5:
        vermogencat = "3X25A"
    elif vermogen < 22.5:
        vermogencat = "3X35A"
    elif vermogen < 26:
        vermogencat = "3X40A"
    elif vermogen < 35:
        vermogencat = "3X63A"
    elif vermogen < 50:
        vermogencat = "3X80A"
    elif vermogen < 175:
        vermogencat = "<175 kVA"
    elif vermogen < 500:
        vermogencat = "<500 kVA"
    else:
        vermogencat = ">500kVA"

    radio_markdown = '''
    Data komt uit de netcongestiekaart van netbeheer Nederland.
    Neem altijd contact op met uw netbeheerder om te zien wat er precies mogelijk is. 
    '''.strip()

    Postcode = st.text_input(label = "Postcode", placeholder= "1011AA", help=radio_markdown)

    Postcode = Postcode.replace(" ", "").upper()
    Congestie = congestiedatabase[congestiedatabase["postcode"] == Postcode]

    st.write("Op basis van uw ritprofiel en het verwachte aantal trucks moet u uw netaansluiting uitbreiden naar minimaal: " + vermogencat) 
    netcongestie = 0
    if (Postcode == "") :
        st.write("U heeft nog geen postcode ingevoerd of de postcode is onbekend") 

    else:
        try: 
            netcongestie = Congestie.iloc[0, 2]
            if Congestie.iloc[0, 2] == 0:
                st.write("Momenteel is er op uw locatie", Postcode, "geen sprake van netcongestie. Er is ook voor de komende termijn voldoende capaciteit beschikbaar")
            if Congestie.iloc[0, 2] == 1:
                 st.write("Momenteel is er op uw locatie", Postcode, "geen sprake van netcongestie. Maar aansluitingen zien wel beperkt. Neem contact op met uw netbeheerder voor details")
            if Congestie.iloc[0, 2] == 2:
                 st.write("Momenteel is er op uw locatie", Postcode, "sprake van netcongestie. Er wordt specifiek onderzoek gedaan naar de mogelijkheden")
            if Congestie.iloc[0, 2] == 3 or Congestie.iloc[0, 2] == 3:
                st.write("Momenteel is er op uw locatie", Postcode, "sprake van netcongestie. U wordt in de wachtrij geplaatst. Neem contact met u netbeheerder voor meer informatie")
                st.write("Met mitigerende maatregelen kunt u uw benodigde netaansluiting terugbrengen tot: 3X80A. Hierdoor hoeft u niet lang te wachten op uitbreiding van uw aansluiting.") 
        except:
            st.error("De postcode is onbekend, controleer nogmaals de invoer")
    ######Buttons voor switch vorige en huidige pagina########
    col3, col4 = st.columns(2)
    with col3:
        if st.button("Vorige"):
            switch_page("laadprofiel")
    with col4:
        if st.button("Volgende"):
            switch_page("overzicht")


####opslaan variabelen
    st.session_state.netaansluiting = Netaansluiting
    st.session_state.netaansluitingnieuw = vermogencat
    st.session_state.netcongestie = netcongestie
####################Pagina opmaak ######################        
with col6:
    st.image("https://i.ibb.co/x5ZPpyq/Progressbar6.png", width=100)    

#except:
 #   st.error("Er is iets misgegaan, probeer het later opnieuw")
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


####Sidebar niet zichtbaar
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