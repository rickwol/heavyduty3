import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px 
import datetime, timedelta
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title="Laadprofiel", page_icon="📈", initial_sidebar_state="collapsed")

#st.sidebar.header("Ritprofielen")

st.title("Heavy Duty Elektrificatie tool")


st.write("Vul hier het rittenpatroon in voor een dag met een maximaal aantal kilometers")


Aantaltrucks=  1

st.write("Op basis van uw eerdere input zou uw laadprofiel erg ongeveer zo uit komen te zien")

#df2 = pd.read_csv("profiel.csv", sep=";")
df2 = st.session_state.profielsum
date = "2023-01-01"


df2["Tijdstip"] = pd.to_datetime(df2["Tijdlijst"])
df2["Load(kW)"] = df2["laadsnelheid"]
fig = px.line(df2, x="Tijdstip", y="Load(kW)", title= "Laadprofiel")


st.plotly_chart(fig)
col3, col4 = st.columns(2)
with col3:
    if st.button("Vorige"):
        switch_page("opties")
with col4:
    if st.button("Volgende"):
        switch_page("netaansluiting")


if "maxvermogen" not in st.session_state:
    st.session_state.maxvermogen = df2["Load(kW)"].max()
