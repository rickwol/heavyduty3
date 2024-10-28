def RitDataMeerdere(ritdata, marge):
    
    import pandas as pd
    import numpy as np
    import datetime

    ritdata["Starttime"] = pd.to_datetime(ritdata["Starttijd"], format = '%H:%M')
    ritdata["Endtime"] = pd.to_datetime(ritdata["Eindtijd"], format = '%H:%M')
    ritdata["difftime"] = ((ritdata["Starttime"].shift(-1) - ritdata["Endtime"]).dt.total_seconds()/3600)-0.16
    ritdata["difftime"] = np.where(ritdata["difftime"] < 0, 12, ritdata["difftime"])
    ritdata["difftime"] = np.where(ritdata["difftime"].isna(), 12, ritdata["difftime"])
    #Indien difftime te klein - kan laden wordt Nee
    ritdata["Kan laden op einde rit"] = np.where((ritdata["difftime"]<0.5), "Nee", ritdata["Kan laden op einde rit"])
    ritdata["Kan laden op einde rit"] = np.where((ritdata["VoertuigNr"].shift(-1) != ritdata["VoertuigNr"]), "Ja", ritdata["Kan laden op einde rit"])
    
    ####Bepalen verbruik
    
#      if voertuig == 'Medium bakwagen lvm 12 - 18 ton':
#         tempverbruikvoertuig = 1.2
#     elif voertuig =='Grote bakwagen lvm > 18 ton': 
#         tempverbruikvoertuig = 1.1
#     elif voertuig =='Lichte trekker z/opl gvm < 40 ton':
#         tempverbruikvoertuig = 1
#     else:
#         tempverbruikvoertuig = 0.8

    ###initalisatie kolom
    ritdata["KMber"] = 0

    ###Nog te checken
    for z in range(len(ritdata["KM"])):
        if ritdata["Rit Nr"][z] == 1:
            ritdata["KMber"][z]  = ritdata["KM"][z]
        elif ritdata["Kan laden op einde rit"][z-1] == "Nee":
            ritdata["KMber"][z]  = ritdata["KMber"][z-1]  + ritdata["KM"][z]
        else:
            ritdata["KMber"][z]  = ritdata["KM"][z]

    rit1 =  ritdata["KM"].head(1)
    if ritdata["KM"].shape[0]>1:
        andereritten = ritdata["KM"].tail(-1).max()/0.8
    else:
        andereritten = rit1



    ritdata["Starttime"] = pd.to_datetime(ritdata["Starttijd"], format = '%H:%M')
    ritdata["Endtime"] = pd.to_datetime(ritdata["Eindtijd"], format = '%H:%M')

    maxi = len(ritdata["Starttime"]) - 1
    mini = ritdata["Endtime"].max() + datetime.timedelta(hours=8)

    ritdata["Verbruik"] = np.where(ritdata["Type voertuig"]== 'Medium bakwagen lvm 12 - 18 ton', 1.2, 0.8)
    ritdata["Verbruik"] = np.where(ritdata["Type voertuig"]== 'Grote bakwagen lvm > 18 ton', 1.1,ritdata["Verbruik"])
    ritdata["Verbruik"] = np.where(ritdata["Type voertuig"]== 'Lichte trekker z/opl gvm < 40 ton', 1,ritdata["Verbruik"])
    

    ritdata["difftime"] = ((ritdata["Starttime"].shift(-1) - ritdata["Endtime"]).dt.total_seconds()/3600)-0.16
    ritdata["difftime"] = np.where(ritdata["difftime"] < -0.16, ((mini - ritdata["Endtime"]).dt.total_seconds()/3600)-0.16 ,ritdata["difftime"] )
    ritdata["difftime"].fillna(((mini - ritdata["Endtime"]).dt.total_seconds()/3600)-0.16, inplace = True)
    ###klopt deze?
    ritdata["Rittijd"] = ((ritdata["Endtime"]-ritdata["Starttime"]).dt.total_seconds()/3600)
    if "Energieextra" not in ritdata.columns: 
        ritdata["verbruikextra"] = np.where(ritdata.Functionaliteit == "Lift Vuilnis" , 0.2 * ritdata["Lifts per uur (indien van toepassing)"],0)
        ritdata["verbruikextra"] = np.where(ritdata.Functionaliteit == "Lift Anders" , 0.2 * ritdata["Lifts per uur (indien van toepassing)"],ritdata["verbruikextra"])
        ritdata["verbruikextra"] = np.where(ritdata.Functionaliteit == "Koeling" , 6,ritdata["verbruikextra"])
        ritdata["Energieextra"] = ritdata["verbruikextra"] * ritdata["Rittijd"]
    
    ritdata["Aantalritten"] = (ritdata.
              groupby(['VoertuigNr'])["Rit Nr"].transform('max'))
    ritdata["laadsnelheid"] =  (ritdata["KMber"] * (1-(marge/100)) * ritdata["Verbruik"]/  ritdata["difftime"]) 
    ritdata["laadsnelheid"] = np.where((ritdata["Aantalritten"] == ritdata["Rit Nr"]), (ritdata["KMber"] * ritdata["Verbruik"]/  ritdata["difftime"]) , ritdata["laadsnelheid"])
    ritdata["laadsnelheid"] = np.where((ritdata["Kan laden op einde rit"] == "Nee"), 0, ritdata["laadsnelheid"])
    
    #ritdata["laadsnelheid"].fillna((ritdata["KM"].sum()* 1.2)/12, inplace=True)###1.2 voertuig verbruik 



    ritdata["Starttime"] = ritdata["Starttime"].dt.floor('5min') 
    ritdata["Endtime"] = ritdata["Endtime"].dt.ceil('5min')
    ritdata["Tijdlijst"] = 0

    for z in range(len(ritdata["Starttime"])-1):
        if (ritdata["Endtime"][z] < ritdata["Starttime"][z+1]):
            ritdata["Tijdlijst"][z] =list(pd.date_range(ritdata["Endtime"][z], ritdata["Starttime"][z+1] ,freq='5T'))
        else:
            ritdata["Tijdlijst"][z] =list(pd.date_range(ritdata["Endtime"][z], mini ,freq='5T'))
    


    # ####Ritdata check accu
    ritdata["Accu"] = 0 #in te stellen op basis van berekening of invulveld

    ritdata["EnergieVerbruik"] = -(ritdata["KM"] * ritdata["Verbruik"] + ritdata["Energieextra"])

    ritdata["Energieopladen"] = np.where(ritdata["laadsnelheid"] > 0, ritdata["difftime"] * ritdata["laadsnelheid"], 0)
    ritdata["Accu"] = ritdata.groupby(["VoertuigNr"])["KMber"].transform('max')
    ritdata["Accu"] = ritdata["Accu"] + ritdata["verbruikextra"].max()
    ritdata["Accu"] = np.where(ritdata["Rit Nr"] == 1, (ritdata["Accu"]/(1-(marge/100))) * ritdata["Verbruik"], 0)
    
    ###Update profiel laatste rit
    mini = ritdata["Endtime"].max() + datetime.timedelta(hours= ritdata["Energieopladen"][maxi]/ritdata["laadsnelheid"].max())
    ritdata["Tijdlijst"][maxi] = ritdata["Tijdlijst"][maxi] =list(pd.date_range(ritdata["Endtime"][maxi], mini ,freq='5T'))

    #ritdata["Accu"] = ritdata["Accu"].shift(-1) + ritdata["EnergieVerbruik"] + ritdata["Energieopladen"]

    
    
    ritdata["VoertuigNr"] = pd.to_numeric(ritdata["VoertuigNr"])
    ritdata["Rit Nr"] = pd.to_numeric(ritdata["Rit Nr"])
    ritdata = ritdata.sort_values(["VoertuigNr", "Rit Nr"])

    for x in range(len(ritdata.Accu)):
        if ritdata["Rit Nr"][x] == 1:
            ritdata["Accu"][x] = ritdata["Accu"][x] + ritdata["EnergieVerbruik"][x]
        else:
            ritdata["Accu"][x] = ritdata["Accu"][x-1] + ritdata["EnergieVerbruik"][x] + ritdata["Energieopladen"][x]

    ritdata["Accu"] = np.where(ritdata["Accu"] >ritdata.KMber.max()/(1-(marge/100))*ritdata["Verbruik"], (1-(marge/100))*ritdata["Verbruik"], ritdata["Accu"])
    
    ritdata["laadsnelheid"] = np.where(ritdata["Rit Nr"] == ritdata["Aantalritten"], (ritdata['Energieopladen']/8), ritdata["laadsnelheid"]) 
    
    profiel = pd.DataFrame(ritdata.explode(["Tijdlijst"]).reset_index())
    profielsum = pd.DataFrame(profiel.groupby(["Tijdlijst"]).laadsnelheid.sum()).reset_index()
    
    return ritdata, profiel, profielsum

###Tweede functie - aanpassingen
def RitDataMeerdereAanpassen(ritdata, verbruiklift, verbruikkoeling):
    
    import pandas as pd
    import numpy as np
    import datetime

    ritdata["laadsnelheid"] = np.where((ritdata["Kan laden op einde rit"] == "Nee"), 0, ritdata["laadsnelheid"])
    
    
    # ####Ritdata check accu
    #ritdata["Accu"] = 0 #in te stellen op basis van berekening of invulveld

    ###Energievebruik extra updaten
    ritdata["verbruikextra"] = np.where(ritdata.Functionaliteit == "Lift Vuilnis" , verbruiklift * ritdata["Lifts per uur (indien van toepassing)"],0)
    ritdata["verbruikextra"] = np.where(ritdata.Functionaliteit == "Lift Anders" , verbruiklift * ritdata["Lifts per uur (indien van toepassing)"],ritdata["verbruikextra"])
    ritdata["verbruikextra"] = np.where(ritdata.Functionaliteit == "Koeling" , verbruikkoeling,ritdata["verbruikextra"])
    ritdata["Energieextra"] = ritdata["verbruikextra"] * ritdata["Rittijd"]
    
    
    ritdata["EnergieVerbruik"] = -(ritdata["KM"] * ritdata["Verbruik"]+ritdata["Energieextra"])

    ritdata["Energieopladen"] = np.where(ritdata["laadsnelheid"] > 0, ritdata["difftime"] * ritdata["laadsnelheid"], 0)
    ritdata["Accu"] = ritdata.groupby(["VoertuigNr"])["Accu"].transform('max')
    ritdata["Accumax"] = ritdata.groupby(["VoertuigNr"])["Accu"].transform('max')
    ritdata["Accu"] = np.where(ritdata["Rit Nr"] == 1, ritdata["Accu"], 0)

    #ritdata["Accu"] = ritdata["Accu"].shift(-1) + ritdata["EnergieVerbruik"] + ritdata["Energieopladen"]

    
    
    ritdata["VoertuigNr"] = pd.to_numeric(ritdata["VoertuigNr"])
    ritdata["Rit Nr"] = pd.to_numeric(ritdata["Rit Nr"])
    ritdata = ritdata.sort_values(["VoertuigNr", "Rit Nr"])

    for x in range(len(ritdata.Accu)):
        if ritdata["Rit Nr"][x] == 1:
            ritdata["Accu"][x] = ritdata["Accu"][x] + ritdata["EnergieVerbruik"][x]
        else:
            ritdata["Accu"][x] = ritdata["Accu"][x-1] + ritdata["EnergieVerbruik"][x] + ritdata["Energieopladen"][x]
            if ritdata["Accu"][x] > ritdata['Accumax'][x]:
                ritdata["Energieopladen"][x] =  ritdata['Accumax'][x] - ritdata["Accu"][x-1] + ritdata["EnergieVerbruik"][x]
            ritdata["Accu"] = np.where(ritdata["Accu"] > ritdata['Accumax'],ritdata['Accumax'], ritdata["Accu"])
    
    ritdata["laadsnelheid"] = np.where(ritdata["Rit Nr"] == ritdata["Aantalritten"], (ritdata['Energieopladen']/8), ritdata["laadsnelheid"])
    
    profiel = pd.DataFrame(ritdata.explode(["Tijdlijst"]).reset_index())
    profielsum = pd.DataFrame(profiel.groupby(["Tijdlijst"]).laadsnelheid.sum()).reset_index()
    
    return ritdata, profiel, profielsum


def profielsummaken(ritdata):
    
    import pandas as pd
    import numpy as np
    import datetime
    import streamlit as st
    
    ritdata["Starttime"] = pd.to_datetime(ritdata["Starttijd"], format = '%H:%M')
    ritdata["Endtime"] = pd.to_datetime(ritdata["Eindtijd"], format = '%H:%M')
    
    maxi = len(ritdata["Starttime"]) - 1
    mini = ritdata["Starttime"].min() + datetime.timedelta(days=1)
    ritdata["Tijdlijst"] = 0
    for z in range(len(ritdata["Starttime"])-1):
        if (ritdata["Endtime"][z] < ritdata["Starttime"][z+1]):
            ritdata["Tijdlijst"][z] =list(pd.date_range(ritdata["Endtime"][z], ritdata["Starttime"][z+1] ,freq='5T'))
        else:
            ritdata["Tijdlijst"][z] =list(pd.date_range(ritdata["Endtime"][z], mini ,freq='5T'))

    ritdata["Tijdlijst"][maxi] =list(pd.date_range(ritdata["Endtime"][maxi], mini ,freq='5T'))
    
    profiel = pd.DataFrame(ritdata.explode(["Tijdlijst"]).reset_index())
    profielsum = pd.DataFrame(profiel.groupby(["Tijdlijst"]).laadsnelheid.sum()).reset_index()
    
    return  profielsum
    