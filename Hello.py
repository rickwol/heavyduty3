import streamlit as st
from st_pages import Page, add_page_title, show_pages

st.set_page_config(page_title=None, page_icon=None, layout="centered", initial_sidebar_state="collapsed", menu_items=None)



show_pages(
    [
        Page("Hello.py", "Home", "🏠"),
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



st.title("Welkom bij de Heavy Duty elektrificatie tool")
from streamlit_extras.switch_page_button import switch_page
st.markdown(
    """
    De tool voor een geïntegreerd advies voor elektrische logistiek. Op basis van ritgegevens krijgt u een advies over de keuze voor elektrische trucks en de bijbehorende laadinfrastructuur. 
    
    Aan de hand van ritprofielen van uw voertuigen krijgt u specifieker advies over de benodigde accucapaciteit van het voertuig en de laadcapaciteit van de infrastructuur. 
    
    Voor de ritprofielen heeft u keuze u voorgeselecteerde ritprofielen, handmatige input in deze app of gebruik te maken van uw eigen ritgegevens middels het format dat u ook aan het CBS moet aanleveren. 
    
    Door een beperkt aantal stappen te volgen en een keuze te maken over uw laadstrategie krijgt u direct beter inzicht in de mogelijkheden voor elektrificatie van uw wagenpark. 
"""
)

#st.page_link("pages/02_InAppInput.py", label = "Input")

st.link_button("Start", "https://heavyduty3-production.up.railway.app/Input")
    

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
    
