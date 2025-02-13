###IMPORTS###
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim


def recup_tableau_aeroports(url, name_csv):
    '''Fonction qui permet de récupérer les données sur un site pour les stocker dans un csv.'''
    #On renseigne l'url du site voulu
    response = requests.get(url)
    #On utilise BeautifulSoup pour screapper des données en présisant html
    soup = bs(response.text, 'html.parser')
    #Sur le site, on veut récupérer toutes les données d'un tableau donc on cherche toutes les 'table', on le trouve en faisant F12 sur le site
    table_aero = soup.find_all('table')
    #On créer la dataframe et il n'y a pas a faire plus puisque c'est deja un tableau sur le site.
    df=pd.read_html(str(table_aero))
    #On présise que l'on veut récupérer que le premier tableau parce qu'il y en plusieurs sir le site et qu'on a besoin que du premier
    df=pd.DataFrame(df[0])
    #Permet de verifier s'il y a un espace, valeur différente si on utilise anaconda ou python (problème trouvé en faisant différents test et voici notre solution)
    if df.columns[5] == "Total passengers":
        #On renomme donc la tête de la colonne avec le nom voulu
        df.rename(columns={'Total passengers':'Totalpassengers'}, inplace= True)
    #Ici, on rajoute deux colonnes a notre dataframe pour prévoir le fait qu'on va rajouter la latitude et la longitude plus tard
    df["latitude"] = ""
    df["longitude"] = ""
    #On transforme la dataframe en CSV que l'on stock avec le chemin d'accès fournit en paramètre
    df.to_csv(name_csv, index=False)
    #On retourne la dataframe pour pouvoir l'utiliser dans une autre fonction afin de rajouter les coordonnées gps
    return df

def recupCoo(url,name_csv):
    '''Cette fonction scrappe les données d'une page web pour les stocker dans un CSV.
La page contient beaucoup d'informations concernant des milliers d'aéroports mondiaux avec les coordonnées gps'''
    #Comme précédemment
    response = requests.get(url)
    soup = bs(response.content, 'html.parser')
    l = []
    #On créer une liste qui a deux dimensions avec autant de ligne que d'aéroport et de colonne que d'information sur chaque aéroports
    #On va ensuite la transformer en dataframe.
    #Il y a donc 7698 aéroports différents et 13 information par aéroports
    for i in range(7698):
        l.append([0] * 13)
    i = 0
    j = 0
    temp = []
    #Cette boucle supprimme les virgules placées au mauvais endroit comme par exmple dans un nombre d'aéroport
    #On arrive a les repérer parce qu'elles ont un espace après
    for list in soup:
        list = list.replace(', ',' ')
        list = list.replace('t,','t')
        temp.append(str(list).split(","))
    temp = temp[0]
    del temp[0]
    #Cette boucle permet de remplir le tableau l correctemment, en passant bien a la ligne d'après quand les 13 informations de chaque aéroports on été ajouté 
    #Elle évite les décallages et retire les guillemets présents sur toutes les informations sauf les nombres
    for t in temp:
        if j == 13:
            i+=1
            j=0
            l[i][j] = t.replace('"','')
        else :
            l[i][j] = t.replace('"','')
        j+=1
    #On créer la dataframe à l'aide de la liste l
    df=pd.DataFrame(l)
    #On renomme les nom des colonnes pour pouvoir se repérer
    df.columns = ["NameAirport","City","Country","CodeIATA","LocationInfo","Latitude","Longitude","Number","Other","Letter","Loc","Airport","OurAirports"]
    #On transforme la dataframe en CSV que l'on stock avec le chemin d'accès fournit en paramètre
    df.to_csv(name_csv, index=False)
    #On retourne la dataframe pour pouvoir l'utiliser dans une autre fonction afin de rajouter les coordonnées aux premier CSV
    return df

def recup_tableau_aeroports_europe(url,name_csv):
    '''Cette fonction récupère des données sur les aéroports en Europe sur un site web'''
    #Repose sur le même principe que la première fonction
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    table_aero_europe = soup.find_all('table')
    
    df=pd.read_html(str(table_aero_europe))
    df=pd.DataFrame(df[0])
    #Permet de supprimer des lignes inutiles 
    df=df.drop([1,2,0,7])
    #On renomme une colonne qui avait des caractère en trop 
    df.rename(columns={'2019\xa0(r)':'2019'}, inplace= True)
    
    listplay = ['2015','2016','2017','2018','2019','2020']
    t = []
    t2 = []
    #Cette boucle permet de supprimer tous les caractères non voulus qui nous empéchaient de passer les valeur en entier
    for pays in listplay:
        t = np.array(df[pays])
        for i in range(len(t)):
            t2.append(t[i].replace('\xa0',''))
        df[pays] = t2
        df[pays].apply(int)
        t2 = []
        t = []
    #On transforme la dataframe en CSV que l'on stock avec le chemin d'accès fournit en paramètre
    df.to_csv(name_csv, index=False)

def fusion_pays_coordonnees(dfAirport,dfCoord,tabl_csv2):
    '''Cette fonction permet de rajouter la latitude et la longitude sur la premiere dataframe'''
    #On récupère les nom des aéroports dans une liste pour rechercher leur coordonnées dans une 
    country = np.array(dfAirport['Airport'])
    #Permet d'utiliser l'API GoogleMaps pour récuperer la latitude et la longitude à partir d'une adresse
    loc = Nominatim(user_agent="GetLoc")
    i=0
    for c in country:
        #Pour chque aéroport on regarde s'il trouve bien les coordonnées dans la seconde dataframe
        temp = dfCoord.loc[dfCoord['NameAirport']==c].index.values
        #S'il n'a rien trouver, alors on utilise l'API de GoogleMaps mais cela prend plus de temps de calcul
        if len(temp) == 0:
            getLoc = loc.geocode(c)
            dfAirport.loc[i, 'latitude'] = getLoc.latitude
            dfAirport.loc[i, 'longitude'] = getLoc.longitude
        #S'il a trouver une correlation, alors on a juste a récupérer les valeurs
        else:
            dfAirport.loc[i, 'latitude'] = dfCoord.loc[temp[0],"Latitude"]
            dfAirport.loc[i, 'longitude'] = dfCoord.loc[temp[0],"Longitude"]
        #On transforme la dataframe en CSV que l'on stock avec le chemin d'accès fournit en paramètre
        dfAirport.to_csv(tabl_csv2, index=False)
        i+=1


#Liens web utilisés et chemins d'accès des CSVs
url_aeroport = 'https://en.wikipedia.org/wiki/List_of_busiest_airports_by_passenger_traffic'
urlCoord = 'https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat'
url_aeroport_europe = 'https://www.insee.fr/fr/statistiques/2016152#tableau-figure1'
tab_aero = "./tab/tables_aero.csv"
tab_coord = "./tab/tables_coord.csv"
tab_aero_europe = "./tab/tables_aero_europe.csv"

#Création des dataframes et des CSVs avec les données des aéroports
print('#########################################\nCréation des dataframes et des CSVs avec les données des aéroports\n#########################################')
dfAeroMonde = recup_tableau_aeroports(url_aeroport,tab_aero)
dfCoordonnees = recupCoo(urlCoord,tab_coord)
recup_tableau_aeroports_europe(url_aeroport_europe,tab_aero_europe)
fusion_pays_coordonnees(dfAeroMonde,dfCoordonnees,tab_aero)
