def RitDataEnkele(ritdata, voertuig):
    
    import pandas as pd
    import numpy as np
    import datetime
    import streamlit as st
    
    ritdata["KM"] = ritdata["Aantal kilometers"]

    for z in range(len(ritdata["Aantal kilometers"])):
        if ritdata["Kan laden op einde rit"][z] != True:
            ritdata["KM"][z+1] = ritdata["KM"][z+1]+ ritdata["KM"][z]


    rit1 =  ritdata["Aantal kilometers"].head(1)
    if ritdata["Aantal kilometers"].shape[0]>1:
        andereritten = ritdata["KM"].tail(-1).max()#/0.8
    else:
        andereritten = rit1



    ritdata["Starttime"] = pd.to_datetime('2023-01-01 ' + ritdata["Starttijd Rit"])
    ritdata["Endtime"] = pd.to_datetime('2023-01-01 ' + ritdata["Eindtijd Rit"])
    ritdata["difftime"] = ((ritdata["Starttime"].shift(-1) - ritdata["Endtime"]).dt.total_seconds()/3600)-0.16
    ritdata["laadsnelheid"] =  ((ritdata["KM"] * voertuig)/  ritdata["difftime"])
    ritdata["laadsnelheid"].fillna((ritdata["Aantal kilometers"].sum()* voertuig)/12, inplace=True)

    return ritdata
