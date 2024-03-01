
def RitDataMeerdere(ritdata, voertuig):
    
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
    mini = ritdata["Starttime"].min() + datetime.timedelta(days=1)

    ritdata["Verbruik"] = 1.2 ###1.2 voertuig verbruik

    ritdata["difftime"] = ((ritdata["Starttime"].shift(-1) - ritdata["Endtime"]).dt.total_seconds()/3600)-0.16
    ritdata["difftime"] = np.where(ritdata["difftime"] < -0.16, ((mini - ritdata["Endtime"]).dt.total_seconds()/3600)-0.16 ,ritdata["difftime"] )
    ritdata["difftime"].fillna(((mini - ritdata["Endtime"]).dt.total_seconds()/3600)-0.16, inplace = True)
    ###klopt deze?
    ritdata["Aantalritten"] = (ritdata.
              groupby(['VoertuigNr'])["Rit Nr"].transform('max'))
    ritdata["laadsnelheid"] =  (ritdata["KMber"] * 0.8 * ritdata["Verbruik"]/  ritdata["difftime"]) 
    ritdata["laadsnelheid"] = np.where((ritdata["Aantalritten"] == ritdata["Rit Nr"]), (ritdata["KMber"] * ritdata["Verbruik"]/  ritdata["difftime"]) , ritdata["laadsnelheid"])
    ritdata["laadsnelheid"] = np.where((ritdata["Kan laden op einde rit"] == "Nee"), 0, ritdata["laadsnelheid"])
    ritdata
    #ritdata["laadsnelheid"].fillna((ritdata["KM"].sum()* 1.2)/12, inplace=True)###1.2 voertuig verbruik 



    ritdata["Starttime"] = ritdata["Starttime"].dt.floor('5min') 
    ritdata["Endtime"] = ritdata["Endtime"].dt.ceil('5min')
    ritdata["Tijdlijst"] = 0

    for z in range(len(ritdata["Starttime"])-1):
        if (ritdata["Endtime"][z] < ritdata["Starttime"][z+1]):
            ritdata["Tijdlijst"][z] =list(pd.date_range(ritdata["Endtime"][z], ritdata["Starttime"][z+1] ,freq='5T'))
        else:
            ritdata["Tijdlijst"][z] =list(pd.date_range(ritdata["Endtime"][z], mini ,freq='5T'))

    ritdata["Tijdlijst"][maxi] = ritdata["Tijdlijst"][maxi] =list(pd.date_range(ritdata["Endtime"][maxi], mini ,freq='5T'))


    # ####Ritdata check accu
    ritdata["Accu"] = 0 #in te stellen op basis van berekening of invulveld

    ritdata["EnergieVerbruik"] = -(ritdata["KM"] * ritdata["Verbruik"])

    ritdata["Energieopladen"] = np.where(ritdata["laadsnelheid"] > 0, ritdata["difftime"] * ritdata["laadsnelheid"], 0)
    ritdata["Accu"] = np.where(ritdata["Rit Nr"] == 1, 300, ritdata["Accu"])

    #ritdata["Accu"] = ritdata["Accu"].shift(-1) + ritdata["EnergieVerbruik"] + ritdata["Energieopladen"]

    profiel = pd.DataFrame(ritdata.explode(["Tijdlijst"]).reset_index())
    
    for z in range(len(ritdata["Accu"])):
        if ritdata["Rit Nr"][z] == 1:
            ritdata["Accu"][z]  = ritdata["Accu"][z] + ritdata["EnergieVerbruik"][z] + ritdata["Energieopladen"][z]
        else:
            ritdata["Accu"][z]  = ritdata["Accu"][z-1]  + ritdata["EnergieVerbruik"][z] + ritdata["Energieopladen"][z]

    ritdata["Accu"] = np.where(ritdata["Accu"] >300, 300, ritdata["Accu"])

    profielsum = pd.DataFrame(profiel.groupby(["Tijdlijst"]).laadsnelheid.sum()).reset_index()
    
    return ritdata, profiel, profielsum

###Tweede functie
