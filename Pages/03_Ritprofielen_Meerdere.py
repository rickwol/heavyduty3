import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px 
import datetime, timedelta
#from mitosheet.streamlit.v1 import spreadsheet
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title="Ritprofielen meerdere voertuigen", page_icon="📈", initial_sidebar_state="collapsed", layout="wide")

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

col3, col4, = st.columns([8, 1])

with col3:

    st.markdown("""Download de excel file om de ritprofielen voor meerdere voertuigen in te vullen. In het huidige formulier staat reeds een voorbeeld ingevuld. Voor een verdere instructie zie de losse <a href="https://filebrowser-production-98b8.up.railway.app/api/public/dl/cYXEu_yl">handleiding</a> of instructies in het tweede tabblad<br><br>
    Indien het formulier goed is ingevuld krijgt een visuele weergave van het rittenpatroon.

    """, unsafe_allow_html=True)
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

    if DataFrame is not None:      
        edited_df2 = DataFrame2
        edited_df2["Starttijd"] = "1970-01-01 " + edited_df2["Starttijd"]
        edited_df2["Eindtijd"] = "1970-01-01 " + edited_df2["Eindtijd"]
        edited_df2 = edited_df2[["VoertuigNr", "Starttijd", "Eindtijd"]]
        heightfig = edited_df2["VoertuigNr"].max()*150
        edited_df2["VoertuigNr"]=edited_df2["VoertuigNr"].astype(str)
        fig = px.timeline(edited_df2, x_start ="Starttijd", x_end ="Eindtijd", y= "VoertuigNr", color= "VoertuigNr", height=heightfig)
        fig.update_xaxes(tickformat="%H:%M:%S")
        fig.update_yaxes(visible=False)
        fig.update_traces(
        hovertemplate=None,
       hoverinfo='skip'
    )
        st.write("Een visuele weergave van uw rittenpatroon over de dag")
        st.plotly_chart(fig)        

####opmaak van pagina    
with col4:
    st.image("https://i.ibb.co/Z1DQj9D/Progressbar2.png", width=100)
    
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

