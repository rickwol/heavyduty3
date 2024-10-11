import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px 
import datetime, timedelta
from streamlit_extras.switch_page_button import switch_page
from Functions2 import *
from Functions import *

st.set_page_config(page_title="Ritprofielen", page_icon="📈", initial_sidebar_state="collapsed", layout="wide")

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


# if "df_value" not in st.session_state:
#     if "df_meerdere" not in st.session_state:
#         ritdata = st.session_state["df_segment"]
#     else:
#         ritdata = st.session_state["df_meerdere"]
#         else:
#             ritdata = st.session_state["df_value"]
###Ophalen variabelen uit session state
ritdataenkel = st.session_state["df_value"].copy(deep=True)
marge = st.session_state.marge
 
ritdata = RitDataEnkele(ritdataenkel, st.session_state.voertuig, st.session_state.opties)                           
rit1 =  ritdata["Aantal kilometers"].head(1)

if ritdata["Aantal kilometers"].shape[0]>1:
    andereritten = ritdata["KM"].tail(-1).max()#/0.8
else:
    andereritten = rit1
kilometers = float(np.maximum(rit1, andereritten)) ###Maximum van alle ritten

kilomterssom = ritdata["Aantal kilometers"].sum() ###Totaalkilometers

energieonderweg = int(kilometers/(1-(marge/100)) * st.session_state.voertuig) + ritdata["Energieextra"].sum()
energiedepot = int(kilomterssom/(1-(marge/100)) * st.session_state.voertuig) + ritdata["Energieextra"].sum()

oplaaddepot = int(np.round(ritdata["laadsnelheid"].tail(1)))



st.write("Op basis van uw input zijn dit twee trucks in combinatie met laadpalen afhankelijk van de laadstrategie")

col1, col2, col3, = st.columns(3)

with col1:
    st.header("Alleen 's nachts op depot laden")
    st.image("https://media.istockphoto.com/id/1306857153/nl/foto/het-laadstation-van-elektrische-voertuigen-op-een-achtergrond-van-een-vrachtwagen.jpg?s=612x612&w=0&k=20&c=kF5jroBqGmPsn_6zup2ahw1R2W6xNb6dNibQqlf-KGM=")
    st.write("Accu:", str(np.round(energiedepot)), "kWh")
    st.write("Range:", str(np.round(kilomterssom)), "km")
    st.write("Laadvermogen: ", str(oplaaddepot), "kW")
with col2:
    st.header("'s nachts + tussentijds laden")
    st.image("https://media.istockphoto.com/id/1306857153/nl/foto/het-laadstation-van-elektrische-voertuigen-op-een-achtergrond-van-een-vrachtwagen.jpg?s=612x612&w=0&k=20&c=kF5jroBqGmPsn_6zup2ahw1R2W6xNb6dNibQqlf-KGM=")
    st.write("Accu:", str(np.round(energieonderweg)), "kWh")
    st.write("Range:", str(np.round(kilometers)),"km")
    st.write("Laadvermogen: ", str(int(np.round(ritdata["laadsnelheid"].max()))), "kW")

radio_markdown = '''
Maak uw keuze uit twee laadstrategieën
1. 's nachts Depot Laden: U laad uw voertuigen alleen na de laatste rit op de dag. In de tool wordt er vanuit gegaan dat de tijd voldoende is om de volgende weer volledig opgeladen te zijn. De range van de truck moet voldoende zijn om alle ritten op de dag te doen.
2. 's nachts + tussentijds laden: Bij deze strategie kiest u ervoor om ook op stops op het depot op te laden. Alleen stops van 20 minuten of langer worden meegenomen. 
'''.strip()

#st.sidebar.header("Ritprofielen")



###Keuze voertuig
truckinput = st.radio(
    'Kies hier uw laadstrategie',
    ('Depot laden                 ', "'s nachts + tussentijds laden"),horizontal = True, help=radio_markdown)


st.text("Gebruik deze input voor een verkenning van welke specifieke truck dit kan zijn in de ZETI tool:")
url = "https://globaldrivetozero.org/tools/zeti/"
st.write("Klik [hier](%s) voor de tool" % url)

#truckinput = st.selectbox("Welke optie kiest u?", ("Alleen depot laden",  "Frequent laden"))
if truckinput == "'s nachts + tussentijds laden":
    accu = energieonderweg
else:
    accu = energiedepot
    ritdata["Kan laden op einde rit"] = np.where(ritdata["Nummer rit"] < ritdata["Nummer rit"].max(), "Nee", "Ja") 
if truckinput == "'s nachts + tussentijds laden":
    snelheid = np.round(ritdata["laadsnelheid"].max()).astype(int)
else: 
    snelheid = oplaaddepot

    
###Aanpassen dataframe
ritdataenkel1 = ritdataenkel
ritdataenkel1["Starttijd"] = ritdataenkel1["Starttijd Rit"]
ritdataenkel1["Eindtijd"] = ritdataenkel1["Eindtijd Rit"]
ritdataenkel1["VoertuigNr"] = 1
ritdataenkel1["Type voertuig"] =  st.session_state.typevoertuig
ritdataenkel1["KM"] = ritdataenkel1["Aantal kilometers"]
ritdataenkel1["Rit Nr"] = ritdataenkel1["Nummer rit"] 


#st.dataframe(ritdataenkel1)

#profielsum = profielsummaken(ritdataenkel1) 

ritdata7, profiel, profielsum = RitDataMeerdere(ritdata, st.session_state.voertuig)


st.write("Afhankelijk van uw laadstrategie nemen we uw voertuigspecificaties mee. Wilt uw toch iets anders invullen dan kan dit hieronder")
#try: 

for x in range(ritdata7["VoertuigNr"].nunique()):
        ritdata2 = ritdata7[ritdata["VoertuigNr"] == x+1].reset_index(drop=True)
        margemax = ritdata2["Accu"].max()*(marge/100)
        exec(f'verbruikvoertuig_{x} = 0') 
        #print(ritdata2["VoertuigNr"].min())
        if ritdata2["VoertuigNr"].min() % 2 != 0:
            voertuig = st.session_state.typevoertuig
            tekst = "Voor gekozen voertuig" 
            st.subheader(tekst)
            st.write(voertuig)
            with st.expander("Zie specificaties"):
                #voertuig = ritdata2["Type voertuig"].min()
                #st.write(voertuig)
                if voertuig == 'Medium bakwagen lvm 12 - 18 ton':
                    exec(f'tempverbruikvoertuig_{x} = 1.2')
                elif voertuig =='Grote bakwagen lvm > 18 ton': 
                    exec(f'tempverbruikvoertuig_{x} = 1.1')
                elif voertuig =='Lichte trekker z/opl gvm < 40 ton':
                    exec(f'tempverbruikvoertuig_{x} = 1')
                else:
                    exec(f'tempverbruikvoertuig_{x} = 0.8')
                key = f"verbruik_input_{x}"
                keyaccu = f"accu_input_{x}"
                keylaad = f"laad_input_{x}"
                exec(f'verbruikvoertuig_{x} = st.number_input("Energieverbruik voertuig kWh/km", value= 1/st.session_state.voertuig, key= key)')
                exec(f'accuvoertuig_{x} = st.number_input("Accu capaciteit (kWh)", value= accu, key= keyaccu)')
                exec(f'laadvoertuig_{x} = st.number_input("Laadsnelheid (kW)", value= snelheid, key= keylaad)')
                exec(f'ritdata.loc[ritdata["VoertuigNr"] == x+1, "Verbruik"] = verbruikvoertuig_{x}')
                exec(f'ritdata.loc[ritdata["VoertuigNr"] == x+1, "Accu"] = accuvoertuig_{x}')
                exec(f'ritdata.loc[ritdata["VoertuigNr"] == x+1, "laadsnelheid"] = laadvoertuig_{x}')
                ritdata3, profiel, profielsum = RitDataMeerdereAanpassen(ritdata)
                ritdata4 = ritdata3[ritdata3["VoertuigNr"] == x+1].reset_index(drop=True)
                margemax = ritdata4.KMber.max()*ritdata4["Verbruik"].max()*(marge/100)
                if (ritdata4["Accu"]+ritdata4["EnergieVerbruik"].shift(-1)).min() < 0:
                    st.write(":red[Met deze combinatie van specificaties kunt u uw ritten **niet** uitvoeren]")
                elif (ritdata4["Accu"]+ritdata4["EnergieVerbruik"].shift(-1)).min() < margemax:
                    st.write(":orange[Met deze combinatie van specificaties kunt u uw ritten uitvoeren maar heeft u minder veiligheidsmarge dan gewenst]")             
                else:
                    st.write(":green[Met deze combinatie van specificaties kunt u uw ritten **wel** uitvoeren]")
                #st.write(margemax)
                #st.write( (ritdata4["Accu"]+ritdata4["EnergieVerbruik"].shift(-1)).min())    
#except:
      #st.error('Er is een fout opgetreden, probeer het nogmaals met een andere invoer', icon="🚨")  
#st.dataframe(profielsum)
####Opslaan resultaten in geheugen

st.session_state.profielsum = profielsum
st.session_state.ritdata3 = ritdata7
st.session_state.ritdata2 = ritdata7


######Buttons voor switch vorige en huidige pagina########

col3, col4 = st.columns(2)    
    
with col3:
    if st.button("Vorige"):
        switch_page("in_app_input")
    
with col4:
    if st.button("Volgende"):
        switch_page("laadprofiel")  

####################Pagina opmaak ######################           
        
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
