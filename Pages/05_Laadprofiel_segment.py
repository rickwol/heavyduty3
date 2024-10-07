import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px 
import datetime, timedelta
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title="Segmentkeuze", page_icon="📈", initial_sidebar_state="collapsed")

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


