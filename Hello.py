import streamlit as st
from st_pages import Page, add_page_title, show_pages
from streamlit_extras.switch_page_button import switch_page


st.set_page_config(page_title=None, page_icon=None, initial_sidebar_state="collapsed", menu_items=None, layout="wide")

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




show_pages(
    [
        Page("Hello.py", "Heavy Duty Elektrificatie Tool", "🏠"),
        # Can use :<icon-name>: or the actual icon
        Page("Pages/01_Input_selectie.py", "Input"),
        #Page("Pages/01_Voertuig_selectie.py", "Voertuig"), 
        Page("Pages/02_InAppInput.py", "In App Input"), 
        #Page("Pages/02_Ritprofielen_Gemiddeld.py", "Ritprofieel Gemiddeld"),
        Page("Pages/03_Ritprofielen_Meerdere.py", "Ritprofiel Gemiddeld"),
        #Page("Pages/05_Laadprofiel_segment.py", "Ritprofiel Per Segment"),
        Page("Pages/06_Resultaten.py", "Voertuig keuze"),
        Page("Pages/09_ResultatenMeerdere.py", "Meerdere Voertuig keuze"),
        Page("Pages/10_Resultaten_Meerdere_Aanpassen.py", "Opties"), 
        Page("Pages/07_Laadprofiel.py", "Laadprofiel"),
        Page("Pages/08_Netaansluiting.py", "Netaansluiting"),
        Page("Pages/11_Overview.py", "Overzicht"),

       
    ]
)

with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)
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





from streamlit_extras.switch_page_button import switch_page
st.markdown(
    """De tool voor een geïntegreerd advies voor elektrische logistiek. Op basis van ritgegevens krijgt u een advies over de keuze voor elektrische trucks en de bijbehorende laadinfrastructuur.<br><br> Aan de hand van ritprofielen van uw voertuigen krijgt u specifieker advies over de benodigde accucapaciteit van het voertuig en de laadcapaciteit van de infrastructuur.<br><br>Voor de ritprofielen heeft u keuze u voorgeselecteerde ritprofielen, handmatige input in deze app of gebruik te maken van uw eigen ritgegevens middels een simpel format.<br><br>
Door een beperkt aantal stappen te volgen en een keuze te maken over uw laadstrategie krijgt u direct beter inzicht in de mogelijkheden voor elektrificatie van uw wagenpark. De applicatie neemt u hierin stap voor stap mee. Meer informatie kunt u krijgen door over de (i) tekentjes te gaan. Heeft u toch behoefte aan een volledige handleiding, dan is deze <a href="https://icthva-my.sharepoint.com/:b:/g/personal/r_wolbertus_hva_nl/EaeEWQSxE7RFhZXiOHgsQB8Be1mgDanahR6xu5GXhvQMEQ?e=XHYZqp">hier</a> te downloaden.<br><br> Dit project is gefinancierd met middelen uit het project Green Transport Delta Elektrificatie en in samenwerking tussen TNO en het Nationaal Kennisplatform Laadinfrastructuur (NKL) tot stand gekomen.

<a href="https://brainporteindhoven.com/nl/ondernemen-en-innoveren/markten/mobility/programmabureau-smart-green-mobility/green-transport-delta-elektrificatie"><img src="https://i.ibb.co/JHc4snw/GTDElogo-removebg-preview.png" alt="GTDElogo" border="0"></a>

""", 
    unsafe_allow_html=True
)

#st.page_link("pages/02_InAppInput.py", label = "Input")

if st.button("Start"):
    switch_page("input")

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
    
