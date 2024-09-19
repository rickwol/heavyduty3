import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px 
import datetime, timedelta
from streamlit_extras.switch_page_button import switch_page
from Functions import *

st.set_page_config(page_title="Overview", page_icon="📈", initial_sidebar_state="collapsed")

#st.sidebar.header("Ritprofielen")

st.title("Heavy Duty Elektrificatie tool")
st.title("Overzicht")

st.text_area("Input",
                   "Aantal voertuigen: .."
                   "Gemiddeld aantal kilometers per dag:")

st.text_area("Voertuigen & Laadinfrastructuur",
                   "Aantal voertuigen: .."
                   "Gemiddeld aantal kilometers per dag:")

st.text_area("Netaansluiting",
                   "Het benodigde additionele vermogen is: .."
                   "Uw huidige netaansluiting is:"
                    "Dit is onvoldoende/voldoende")


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
<img src="https://i.ibb.co/b6QF7F1/design.png">
</div>
"""
st.markdown(footer,unsafe_allow_html=True)  