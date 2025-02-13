###IMPORTS###
import graph as gr
import pandas as pd

###Chemins d'accès aux CSVs
tab_aero = "./tab/tables_aero.csv"
tab_aero_europe = "./tab/tables_aero_europe.csv"
tab_coord = "./tab/tables_coord.csv"

###Création des Dataframes via les CSVs
print('#########################################\nGénération des dataframes')
dfEurope = pd.read_csv(tab_aero_europe)
dfMondeCoord = pd.read_csv(tab_aero)
dfCoord = pd.read_csv(tab_coord)

###créer l'Objet graph avec toutes les informations nécessaires(les 3 dataframes)
print('#########################################\nGénération du dashboard')
graph = gr.graph(dfMondeCoord,dfEurope,dfCoord)
graph.worldGen()

