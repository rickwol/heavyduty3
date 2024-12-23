import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px 
import datetime, timedelta
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title="Laadprofiel", page_icon="📈", initial_sidebar_state="collapsed", layout="wide")

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


    Aantaltrucks=  1

    st.write("Op basis van uw eerdere input zou uw laadprofiel erg ongeveer zo uit komen te zien")

    #df2 = pd.read_csv("profiel.csv", sep=";")
    df2 = st.session_state.profielsum.copy(deep=True)
    date = "2023-01-01"
    maxdate = df2["Tijdlijst"].max()
    df3 = pd.DataFrame(pd.date_range("1900-01-01 0:00:00",maxdate, freq='5T'))
    df3.rename(columns={df3.columns[0]: 'Tijdlijst'}, inplace=True)
    df2["Tijdlijst"] = pd.to_datetime(df2["Tijdlijst"])
    df4 =df2.merge(df3, on="Tijdlijst", how="outer")
    df4.laadsnelheid.fillna(0, inplace=True)
    df4["Tijdstip"] = pd.to_datetime(df4["Tijdlijst"])
    df4["Load(kW)"] = df4["laadsnelheid"]
    df4.drop_duplicates(subset=['Tijdstip'], inplace=True)
    df4.sort_values(by=['Tijdstip'], inplace=True)
    df4["Load(kW)"] = np.where(df4["Load(kW)"] < 0, df4["Load(kW)"]*-1, df4["Load(kW)"])

    fig = px.line(df4, x="Tijdstip", y="Load(kW)", title= "Laadprofiel")
    fig.update_xaxes(tickformat="%H:%M:%S")
    fig.update_layout(yaxis_title="Vermogen (kW)")

    


    st.plotly_chart(fig)
    col3, col4 = st.columns(2)
    with col3:
        if st.button("Vorige"):
            if st.session_state.invoer == 'In app invoer (1 voertuig maximaal)':
                switch_page("voertuig keuze")
            else:
                switch_page("opties")
    with col4:
        if st.button("Volgende"):
            switch_page("netaansluiting")


    if "maxvermogen" not in st.session_state:
        st.session_state.maxvermogen = df4["Load(kW)"].max()

    if "laadprofiel" not in st.session_state:
        st.session_state.laadprofiel = fig
with col6:
    st.image("https://i.ibb.co/Cw6Xxkd/Progressbar5.png", width=100)  

    
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