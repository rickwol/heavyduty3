import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px 
import datetime, timedelta
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title="Voertuigen", page_icon="📈", initial_sidebar_state="collapsed")

####Header
from streamlit_navigation_bar import st_navbar


styles = {
    "nav": {
        "background-color": "#fab529",
        "height": "4rem",
        "font-size": "35px",
        "justify-content": "left"
    }
}

st_navbar(
    pages=["Heavy Duty Elektrificatie Tool"],
    styles = styles
)

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
###Set tooltips
radio_markdown = '''
1. In app invoer: U vult ritgegevens voor 1 voertuig voor 1 dag in. U kunt kiezen voor welk type voertuig 
2. Format invoer: U gebruikt een vastgesteld format, waarbij u voor meerdere voertuigen data in kan voeren
'''.strip()

#st.sidebar.header("Ritprofielen")




###Keuze voertuig
inputkeuze = st.radio(
    'Kies hier de input die u wilt gebruiken',
    ('In app invoer (1 voertuig maximaal)', 'Format Invoer (Meerdere voertuigen)'),help=radio_markdown)

if inputkeuze not in st.session_state:
    st.session_state.invoer = inputkeuze



if st.button("Volgende"):
    if inputkeuze == 'Standaard profielen':
        switch_page("ritprofiel per segment")
    elif inputkeuze == 'In app invoer (1 voertuig maximaal)':
        switch_page("in app input")
    else:
        switch_page("ritprofiel gemiddeld")

        
        
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
