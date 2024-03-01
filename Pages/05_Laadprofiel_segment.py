import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px 
import datetime, timedelta
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title="Segmentkeuze", page_icon="📈", initial_sidebar_state="collapsed")

#st.sidebar.header("Ritprofielen")

st.title("Heavy Duty Elektrificatie tool")


radio_markdown = '''
Voor uw segment wordt een typisch ritprofiel getoond aangepast aan uw jaar kilometrage. 
Staat uw segment er niet tussen, kies dan voor de optie om handmatig een rittenpatroon in te vullen.
'''.strip()

optiesvoertuig =  st.selectbox("In welk segment bent u actief?",
                                        ("Afval", "Bouw", "Facilitair", "Horeca", "Post en pakket", "Retail food", "Retail non-food", "Installatie"),
                               help=radio_markdown)
Kilometrage =  st.number_input('Wat is het gemiddelde jaarkilometrage van uw truck?', step = 500, min_value= 5000)

####if statements voor keuze ritprofiel segment

#df_segment = ....
#st.session_state.df_segment = df_segment

if st.button("Volgende"):
    switch_page("voertuig keuze")



