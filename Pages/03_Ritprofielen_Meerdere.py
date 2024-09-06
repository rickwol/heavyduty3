import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px 
import datetime, timedelta
#from mitosheet.streamlit.v1 import spreadsheet
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title="Ritprofielen meerdere voertuigen", page_icon="📈", initial_sidebar_state="collapsed")

#st.sidebar.header("Ritprofielen")

st.title("Heavy Duty Elektrificatie tool")

st.write("Download de excel file om de ritprofielen voor meerdere voertuigen in te vullen. In het huidige formulier staat reeds een voorbeeld ingevuld. Voor een verdere instructie zie de losse handleiding of instructies in het tweede tabblad")
with open("Pages/Invulformulier.xlsx", "rb") as file:
    st.download_button(label = "Download", data=file, file_name="Invulformulier.xlsx")

st.write("Indien je het formulier hebt ingevuld kun je hier uploaden")

DataFrame = st.file_uploader(label = "Upload")
if DataFrame is not None:
    DataFrame2 = pd.read_excel(DataFrame, converters={'Starttijd': str,'eindtijd': str} )
    st.session_state.df_value = DataFrame2

col1, col2, = st.columns(2)

with col1:
    if st.button("Vorige"):
        switch_page("input")
    
with col2:
    if st.button("Volgende"):
        switch_page("meerdere voertuig keuze")    

    


