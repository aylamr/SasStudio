import requests
import pandas as pd


headers = {
    'Accept': 'application/json, text/plain, */*'
}

params = {
    'type': 'main',
    'page_size': '1000',
    'q': '',
}

response = requests.get('https://www.data.gouv.fr/api/2/datasets/53698f4ca3a729239d2036df/resources/', params=params, headers=headers)

vehicules, caracs, lieux, usagers = pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# Récupérer l'ensemble des données
for data in response.json()["data"]:
    if ("vehicules-2" in data["title"]):
        part = pd.read_csv(data["latest"], sep=";")
        if part.shape[1] == 1:
            part = pd.read_csv(data["latest"], sep=",", low_memory=False)
        vehicules = pd.concat([vehicules, part])
    elif ("lieux-" in data["title"]):
        part = pd.read_csv(data["latest"], sep=";")
        if part.shape[1] == 1:
            part = pd.read_csv(data["latest"], sep=",", low_memory=False)
        lieux = pd.concat([lieux, part])
    elif ("usagers-" in data["title"]):
        part = pd.read_csv(data["latest"], sep=";")
        if part.shape[1] == 1:
            part = pd.read_csv(data["latest"], sep=",")
        usagers = pd.concat([usagers, part])
    elif ("caracteristiques-" in data["title"]) | ("carcteristiques-" in data["title"]):
        try:
            part = pd.read_csv(data["latest"], sep=";", error_bad_lines=False)
        except UnicodeDecodeError as e:
            part = pd.read_csv(data["latest"], sep=",",encoding="ISO-8859-1")
            part["lat"] = part["lat"]/100000
            part["long"] = part["long"]/100000
        caracs = pd.concat([caracs, part])
    else:
        pass


# standardize dates
caracs.an = caracs.an.replace(17, 2017).replace(18, 2018)
caracs["date"] = caracs.jour.astype("str").str.zfill(2) + "-" + caracs.mois.astype("str").str.zfill(2) + "-" + caracs.an.astype("str")
caracs["date"] = pd.to_datetime(caracs["date"], infer_datetime_format=True)

# replace codes by categories
# https://static.data.gouv.fr/resources/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2021/20221104-163105/description-des-bases-de-donnees-annuelles-2021.pdf
code2cat = {
    "1":"Autoroute",
    "2":"Route nationale",
    "3":"Route Départementale",
    "4":"Voie Communales",
    "5":"Hors réseau public",
    "6":"Parc de stationnement ouvert à la circulation publique",
    "7":"Routes de métropole urbaine",
    "9":"autre"
}

code2plan = {
"-1" : "Non renseigné",
"1" : "Partie rectiligne",
"2" : "En courbe à gauche",
"3" : "En courbe à droite",
"4" : "En S"
}

code2surf = {
"-1" : "Non renseigné",
"1" : "Normale",
"2" : "Mouillée",
"3" : "Flaques",
"4" : "Inondée",
"5" : "Enneigée",
"6" : "Boue",
"7" : "Verglacée",
"8" : "Corps gras – huile",
"9" : "Autre"
}


code2infra = {
"-1" : "Non renseigné",
"0" : "Aucun",
"1" : "Souterrain - tunnel",
"2" : "Pont - autopont",
"3" : "Bretelle d’échangeur ou de raccordement",
"4" : "Voie ferrée",
"5" : "Carrefour aménagé",
"6" : "Zone piétonne",
"7" : "Zone de péage",
"8" : "Chantier",
"9" : "Autres "
}

code2situ = {
"-1" : "Non renseigné",
"0" : "Aucun",
"1" : "Sur chaussée",
"2" : "Sur bande d’arrêt d’urgence",
"3" : "Sur accotement",
"4" : "Sur trottoir",
"5" : "Sur piste cyclable",
"6" : "Sur autre voie spéciale",
"8" : "Autres"
}


lieux["categorie"] = lieux.apply(lambda x: code2cat[str(x["catr"])], axis=1)

# merge dataframes
df = caracs.merge(lieux, on="Num_Acc", how="left")

# select columns
df= df[["Num_Acc", "date", "lat", "long","categorie", "vma", "plan", "lartpc", "larrout", "surf", "infra", "situ", "dep"]].dropna()
df = df.fillna(-1)
df["plan"] = df["plan"].replace(0, -1)
df["surf"] = df["surf"].replace(0, -1)
df["plan"] = df.apply(lambda x: code2plan[str(int(x["plan"]))], axis=1)
df["surf"] = df.apply(lambda x: code2surf[str(int(x["surf"]))], axis=1)
df["infra"] = df.apply(lambda x: code2infra[str(int(x["infra"]))], axis=1)
df["situ"] = df.apply(lambda x: code2situ[str(int(x["situ"]))], axis=1)

# convert lat/long to float
df["lat"] = df["lat"].str.replace(",",".").astype("float")
df["long"] = df["long"].str.replace(",",".").astype("float")

df.rename(columns={'vma':'v_max', 'lartpc':'largeur_TPC', 'larrout':'largeur_chaussée', 'surf':'etat_surface','situ':'Situation_accident', 'infra':'Aménagement'}, inplace=True)
SAS.df2sd(df,'casuser.accidents_corporels_py')