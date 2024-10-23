import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px 
import datetime, timedelta
from streamlit_extras.switch_page_button import switch_page
from Functions import *
import smtplib
from email.mime.text import MIMEText

st.set_page_config(page_title="Overview", page_icon="📈", initial_sidebar_state="collapsed", layout="wide")

#st.sidebar.header("Ritprofielen")
ritdata = st.session_state.ritdata3
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

with col5: 
    st.title("Overzicht")

#     for x in range(ritdata["VoertuigNr"].nunique()):
#         tekst = "Voor voertuig " + str(x+1)
#         st.write(tekst)
#         ritdata2 = ritdata[ritdata["VoertuigNr"] == x+1].reset_index(drop=True)
#         types = ritdata2["Type voertuig"][0] + '\n' + "Kilometers per dag: " + ritdata2["KM"].sum().astype("str")
#         st.text_area("Input",
#                        types)
#         #ritten = "Aantal ritten: " + str(len(ritdata2["KM"])) +"\n" + "Maximale lengte rit: " + ritdata2["KM"].max().astype("str")
#         #st.text_area("Ritgegeves",
#                        #ritten)
#         edited_df2 = ritdata
#         edited_df2["Rit"] = "Rit"
#         edited_df2["Starttijd Rit"] = "1970-01-01 " + edited_df2["Starttijd Rit"]
#         edited_df2["Eindtijd Rit"] = "1970-01-01 " + edited_df2["Eindtijd Rit"]
#         edited_df2 = edited_df2[["Rit", "Starttijd Rit", "Eindtijd Rit"]]
#         fig = px.timeline(edited_df2, x_start ="Starttijd Rit", x_end ="Eindtijd Rit", y= "Rit", height=200)
#         fig.update_xaxes(tickformat="%H:%M:%S")
#         st.plotly_chart(fig)
#         st.text_area("Voertuigen & Laadinfrastructuur",
#                        "Omvang van accucapaciteit: .."
#                        "Laadsnelheden:")

#         st.text_area("Netaansluiting",
#                        "Het benodigde additionele vermogen is: .."
#                        "Uw huidige netaansluiting is:"
#                         "Dit is onvoldoende/voldoende")


    def generate_pdf():
        """Generate an example pdf file and save it to example.pdf"""
        from fpdf import FPDF

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Welcome to Streamlit!", ln=1, align="C")
        pdf.output("example.pdf")


    if st.button("Generate PDF"):
        generate_pdf()
        st.success("Generated example.pdf!")

        with open("example.pdf", "rb") as f:
            st.download_button("Download pdf", f, "example.pdf")

    email_receiver = st.text_input('To')
    subject = "Heavy Duty Charging Tool Resultaten"
    body = "Beste, Bedankt voor het gebruik van de Heavy Duty Charging Tool Resultaten. In de bijlage vindt u uw resultaten. "
    if st.button("Stuur email"):
        email_sender = 'r.wolbertus@gmail.com'
    

# Hide the password input
        #password = st.text_input('Password', type="password", disabled=True)  


        try:
            
            msg = MIMEText(body)
            msg['From'] = "r.wolbertus@gmail.com"
            msg['To'] = email_receiver
            msg['Subject'] = subject
#             with open("example.pdf", "rb") as f:
#                 pdfd = f
#             msg.add_attachment(pdfd)
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login("r.wolbertus@gmail.com", "uiqa sieb pyxv gmeq")
            server.sendmail(email_sender, email_receiver, msg.as_string())
            server.quit()
            st.success('Email sent successfully! 🚀')
        except Exception as e:
            st.error("Failed to send email")
with col6:
    st.image("https://i.ibb.co/mJYqJB6/Progressbar7.png", width=40)
    
        
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