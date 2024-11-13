import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px 
import datetime, timedelta
from streamlit_extras.switch_page_button import switch_page
from Functions import *
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.nonmultipart import MIMENonMultipart
import email.encoders
from email.message import EmailMessage
import base64

st.set_page_config(page_title="Overview", page_icon="📈", initial_sidebar_state="collapsed", layout="wide")

#st.sidebar.header("Ritprofielen")
ritdata = st.session_state.ritdata3
if "VoertuigNr" not in ritdata.columns:
    ritdata["VoertuigNr"] = 1
    
ritdata["Accumax"] = ritdata["Accu"].max()/(1-(st.session_state.marge/100)) + ritdata["Energieextra"].sum()
profielsum = st.session_state.profielsum 

####Header
from streamlit_navigation_bar import st_navbar

styles = {
    "nav": {
        "background-color": "#fab529",
        "height": "3.825rem",
        "font-size": "30px",
    }
}

st_navbar(
    pages=["Heavy Duty Elektrificatie Tool"],
    styles = styles
)
col5, col6, = st.columns([8, 1])


#try: 
with col5: 
    st.title("Overzicht")

    col7, col8, col9 = st.columns([2, 2, 2])

    with col7: 
        for x in range(ritdata["VoertuigNr"].nunique()):
            exec(f'tekst1_{x} = "Voor voertuig " + str(x+1)')
            exec(f'st.subheader(tekst1_{x})')
            ritdata2 = ritdata[ritdata["VoertuigNr"] == x+1].reset_index(drop=True)
            exec(f'tekst2_{x} = ritdata2["Type voertuig"][0]')# + "\n Kilometers per dag: " + ritdata2["KM"].sum().astype("str")
            exec(f'st.write(tekst2_{x})')
            exec(f'tekst3_{x} = "Afstand per dag: " + ritdata2["KM"].sum().astype("str") + " KM"')
            exec(f'st.write(tekst3_{x})')
            exec(f'tekst4_{x} = "Maximale afstand zonder oplaadmogelijkheid: " + str(ritdata2["KMber"].max()) + " KM"')
            exec(f'st.write(tekst4_{x})')

    with col8:
        for x in range(ritdata["VoertuigNr"].nunique()):
            exec(f'tekst5_{x} = "" ')
            exec(f'st.subheader(tekst5_{x})')
            exec(f'st.subheader(tekst5_{x})')
            ritdata2 = ritdata[ritdata["VoertuigNr"] == x+1].reset_index(drop=True)
            exec(f'tekst6_{x} = "Accu: " + str(np.round(ritdata2["Accumax"][0])) + "kWh"')# + "\n Kilometers per dag: " + ritdata2["KM"].sum().astype("str")
            exec(f'st.write(tekst6_{x})')
            exec(f'tekst7_{x} = "Laadvermogen: " + str(np.round(ritdata2["laadsnelheid"].max())) + "kW"')
            exec(f'st.write(tekst7_{x})')
            exec(f'tekst8_{x} = "Verbruik per kilometer: " + str(ritdata2["Verbruik"].max()) + "kWh/km"')
            exec(f'st.write(tekst8_{x})')

    with col9:
        st.subheader("Voor uw gehele operatie")
        tekst9 = "Maximaal benodigd vermogen laden voertuigen: " + str(np.round(profielsum.laadsnelheid.max())) + " kW"
        st.write(tekst9)
        tekst10 = "Uw huidige netaansluiting: " + st.session_state.netaansluiting 
        st.write(tekst10)
        tekst11= "Uw benodigde netaansluiting: " + st.session_state.netaansluitingnieuw
        st.write(tekst11)
        tekstnetaansluiting = "Er is"
        tekstnetaansluiting = tekstnetaansluiting + str(np.where(st.session_state.netcongestie < 2, " ", " geen "))
        tekstnetaansluiting = tekstnetaansluiting + "sprake van netcongestie bij u in de buurt. "
        tekstnetaansluiting = tekstnetaansluiting + str(np.where(st.session_state.netcongestie < 2, "Neem contact op met uw netbeheerder", " "))
        st.write(tekstnetaansluiting)

    def generate_pdf():
        """Generate an example pdf file and save it to example.pdf"""
        from fpdf import FPDF
        class FPDF(FPDF):
            def footer(self):
                 if self.page_no() != 1:
                    pdf.image("https://i.ibb.co/K9nnLCx/design.png", h=20, w=200)

        pdf = FPDF()
        pdf.add_font("Open Sans", style="", fname="open-sans.regular.ttf", uni=True)
        pdf.add_font("Open Sans", style="B", fname="open-sans.bold.ttf", uni=True)
        pdf.set_font('Open Sans', '', 6)
        pdf.add_page()
        pdf.image("https://i.ibb.co/d52VC0r/Voorpagina-Resultaten.png", w=200)
        pdf.cell(200, 35, txt="", ln=1, align="L")
        pdf.set_font('Open Sans', style="B",size=12)
        pdf.cell(200, 10, txt="Resultaten Heavy Duty Charging Tool", ln=1, align="L")
        pdf.set_font('Open Sans', style="", size=8)
        pdf.multi_cell(200, 10, txt="Bedankt voor het gebruik van de Heavy Duty Charging Tool. In dit bestand vind u de resultaten van de tool in een gemakkelijk overzicht. Per ingevoerd voertuig krijgt u de specificaties waarmee u verder op zoekt kunt gaan naar de optimale afstemming tussen uw voertuig en de laadinfrastructuur.", align="L")
        pdf.cell(200, 10, txt="", ln=1, align="L")
        with pdf.text_columns(text_align="J", ncols=2, gutter=5) as cols: 
            for x in range(ritdata["VoertuigNr"].nunique()):
#                 pdf.set_font('Open Sans', style="B", size=8)
#                 exec(f'cols.cell(200, 10, txt=tekst1_{x} , ln=1, align="L")')
#                 pdf.set_font('Open Sans', style="", size=8)
#                 exec(f'cols.cell(200, 10, txt=tekst2_{x} , ln=1, align="L")')
#                 exec(f'pdf.cell(200, 10, txt=tekst3_{x} , ln=1, align="L")')
#                 exec(f'pdf.cell(200, 10, txt=tekst4_{x} , ln=1, align="L")')
#                 exec(f'pdf.cell(200, 10, txt=tekst5_{x} , ln=2, align="L")')
#                 exec(f'pdf.cell(200, 10, txt=tekst6_{x} , ln=1, align="L")')
#                 exec(f'pdf.cell(200, 10, txt=tekst7_{x} , ln=1, align="L")')
#                 exec(f'pdf.cell(200, 10, txt=tekst7_{x} , ln=1, align="L")')
#                 exec(f'pdf.cell(200, 10, txt=tekst8_{x} , ln=2, align="L")')
                pdf.set_font('Open Sans', style="B", size=10)
                exec(f'cols.write(text=tekst1_{x})')
                cols.write(text= "\n")
                pdf.set_font('Open Sans', style="", size=10)
                exec(f'cols.write( text=tekst2_{x})')
                cols.write(text= "\n")
                cols.write(text= "\n")
                exec(f'cols.write( text=tekst3_{x})')
                cols.write(text= "\n")
                cols.write(text= "\n")
                exec(f'cols.write( text=tekst4_{x})')
                cols.write(text= "\n")
                cols.write(text= "\n")
                exec(f'cols.write( text=tekst5_{x})')
                cols.write(text= "\n")
                cols.write(text= "\n")
                pdf.set_font('Open Sans', style="B", size=7)
                cols.write(text= "Gekozen specificaties")
                cols.write(text= "\n")
                cols.write(text= "\n")
                pdf.set_font('Open Sans', style="", size=10)
                exec(f'cols.write( text=tekst6_{x})')
                cols.write(text= "\n")
                cols.write(text= "\n")
                exec(f'cols.write( text=tekst7_{x})')
                cols.write(text= "\n")
                cols.write(text= "\n")
                exec(f'cols.write( text=tekst8_{x})')
                cols.write(text= "\n")
                cols.write(text= "\n")
                exec(f'cols.write( text=tekst5_{x})')
                cols.write(text= "\n")
                cols.write(text= "\n")
        if ritdata["VoertuigNr"].nunique()> 2: 
            pdf.add_page()            
        pdf.set_font('Open Sans', style="B", size=8)
        exec(f'pdf.cell(200, 10, txt="Benodigd voor uw gehele operatie" , ln=1, align="L")')
        pdf.set_font('Open Sans', style="", size=8)
        exec(f'pdf.cell(200, 10, txt=tekst9 , ln=1, align="L")')
        exec(f'pdf.cell(200, 10, txt=tekst10 , ln=1, align="L")')
        exec(f'pdf.cell(200, 10, txt=tekst11 , ln=1, align="L")')
        exec(f'pdf.cell(200, 10, txt=tekstnetaansluiting , ln=1, align="L")')


        pdf.output("ResultatenHeavyDuty.pdf")


    if st.button("Generate PDF"):
        generate_pdf()
        st.success("Uw PDF is klaar om te downloaden!")

        with open("ResultatenHeavyDuty.pdf", "rb") as f:
            st.download_button("Download pdf", f, "ResultatenHeavyDuty.pdf")


    email_receiver = st.text_input('To')
    subject = "Heavy Duty Charging Tool Resultaten"
    body = "Beste, Bedankt voor het gebruik van de Heavy Duty Charging Tool Resultaten. In de bijlage vindt u uw resultaten. /n Met vriendelijke groet het team van de Heavy Duty Charging Tool"
    if st.button("Stuur email"):
        email_sender = 'noreply@etruckplanner.nl'

        try: 
# Hide the password input
        #password = st.text_input('Password', type="password", disabled=True)  
            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = email_sender
            msg['To'] = email_receiver
            msg.set_content(body)
            file = "ResultatenHeavyDuty.pdf"
            with open(file,'rb') as f:
                file_data = f.read()
                file_name = f.name
                msg.add_attachment(file_data, maintype='application', subtype = 'pdf', filename=file_name)
            with smtplib.SMTP_SSL('smtp.strato.com', 465) as smtp:
                smtp.login("noreply@etruckplanner.nl",  "fLM68AWxq$jeuM+")
                smtp.send_message(msg)
                st.success('Email is verzonden! 🚀')
        except Exception as e:
             st.error("Failed to send email")
# except:
#     st.error("Er is iets mis gegaan, probeert u het opnieuw")


with col6:
    st.image("https://i.ibb.co/mJYqJB6/Progressbar7.png", width=100)

#except:
 #   st.error("Er ging iets mis. Probeert u het later nog eens")
        
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
