###IMPORTS###
import dash
from dash import dcc
from dash import html
from dash.dependencies import Output,Input
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import numpy as np


class graph:
    def __init__(self, df,dfeurope,dfcoord):
        self.df = df
        self.dfeurope = dfeurope
        self.dfcoord = dfcoord
    
    def worldGen(self):
        '''Cette fonction prend en parametre les trois dataframes et génère un Dashboard. En effet, on créer 5 graphiques différents et ensuite on paramètre la page avec de l'HTML.
        On précise les titres et sous-titres, les paragraphes, les fonts de couleurs avec l'emplacement des graphiques. 
        En définitif, elle s'occupe de tout ce qui est visuel.'''
        #Creation du Dashboard
        app = dash.Dash(__name__)
        #Permet de définir des couleurs pour les utiliser plus tard. Ca évite de copier coller le code couleur a chaque fois
        colors = {
            'background': '#111111',
            'title': '#66A6E5',
            'text': '#5A80A5'
        }

        # Initialisation de toutes les figures pour avoir des tailles et des types différents
        figCarteEntiere = make_subplots(
            rows=1, 
            cols=1
            )
        figMonde = make_subplots(
            rows=1, 
            cols=1,
            shared_xaxes=True,
            shared_yaxes=True,
            #On renseigne le type du graph que l'on va utiliser, ici un scattergeo
            specs=[[{"type": "scattergeo"}]]
            )

        figBar = make_subplots(
            rows=1, 
            cols=1,
            shared_xaxes=True,
            shared_yaxes=True,
            specs=[[{"type": "bar"}]])

        figPie = make_subplots(
            rows=1, 
            cols=1,
            shared_xaxes=True,
            shared_yaxes=True,
            specs=[[{"type":"pie"}]])

        figCovid = make_subplots(
            rows=1, 
            cols=1,
            shared_xaxes=True,
            shared_yaxes=True,
            specs=[[{"type":"scatter"}]])

        # Ici, l'objectif était de réaliser une carte très réaliste et qui peut être comparée a celles qu'on retrouve dans nos
        # applications. On a donc utilisé mapbox qui nous permet de réaliser ce qu'on voulait
        # On renseigne le liens qui correspond au style de notre carte. On a choisi quelque chose ressemblant a GoogleMaps satellite
        
        # Notre figure est décomposée en deux parties, les données et l'aspect graphique.
        # Pour les données, on fait un scattermapbox
        data =[go.Scattermapbox(
                lat=self.dfcoord["Latitude"], 
                lon=self.dfcoord["Longitude"],
                customdata = self.dfcoord["NameAirport"],
                mode="markers",
                text=self.dfcoord["NameAirport"],
                #Permet de préciser ce qu'on veut qu'il soit affiché quand on passe la souris sur un point
                hoverinfo="text",
                #Permet changer l'aspect des points, ici, ils seront jaune, petit et opaque
                marker=dict(
                    size= 13,
                    color = 'gold',
                    opacity = .8,
                ),
            )]
        # Pour l'aspect graphique, on fait un Layout
        layout = go.Layout(
            autosize=True,
            #Ici, on doit renseigner notre token personnel, qui est discponnible dans notre compte. Il permet d'afficher la carte gratuitement 50 000 fois
            mapbox= dict(accesstoken="pk.eyJ1IjoibWF4aW1lMTEyOCIsImEiOiJjbDlxODRqYmUwMzViM3VxbG9zaGwwczM1In0.gC10xZKulinIQ1c3pz1ezA",
            
            bearing=10,
            pitch=60,
            #Choix du zoom de départ
            zoom=11,
            #Coordonnées de départ 
            center= dict(
                lat=46.227638,
                lon=2.213749
                ),
            # On renseigne le liens qui correspond au style de notre carte. On a choisi quelque chose ressemblant a GoogleMaps satellite
            style="mapbox://styles/mapbox/satellite-streets-v11"
            ),
            #On choisi la hauteur de la carte
            height=900,
            #On met l'arrière plan en noir
            template="plotly_dark")

        #On définit notre première figure 
        figCarteEntiere = dict(data=data,layout=layout)

        #BAR
        #on définit les abscisses et les ordonnées de notre graphique en récupérant tout une colonne de la Dataframe pour avoir une liste
        x = np.array(self.df['Location'])
        y = np.array(self.df['Totalpassengers'])
        #On renseigne tous les paramètres
        figBar.add_trace(
            go.Bar(
                name='Aéroports avec le plus de visiteurs', 
                x=x, 
                y=y,
                text=y),
            row=1, 
            col=1
            ).update_traces(
                texttemplate='%{text:.2s}', #permet le nombre d'habitant au dessus des bâtons 
                textposition='outside'
                ).update_layout(height=800,template="plotly_dark")#On choisi la taille de la figure et la couleur des bords
        
        #Courbe
        figCovid.add_trace(
            #parametrage du graphique
            go.Scatter(
                x=self.dfeurope['Ligne aérienne'], 
                y=self.dfeurope['2015'].apply(int)),#On passe toutes la valeures de la colonne en entier 
            row=1,
            col=1
            ).update_layout(height=300,yaxis_range=[0,160000],template="plotly_dark")

        #Camembert
        #Initialisation ses paramètres pour ensuite tracer notre camembert
        xCam = []
        yCam = []
        for i in range(len(self.df)):
            #On rajoute des pays au fur et a musure dans une liste pour pouvoir additionner le nombre de voyageur par la suite
            if self.df.loc[i,"Country"] not in yCam:
                yCam.append(self.df.loc[i,"Country"])
                xCam.append(self.df.loc[i,"Totalpassengers"])
            else:
                val = yCam.index(self.df.loc[i,"Country"])
                xCam[val] += self.df.loc[i,"Totalpassengers"] 
        #Renseignement des paramètres de la figure
        figPie.add_trace(
            go.Pie(
                values = xCam, 
                labels=yCam,
                textinfo='label+percent',
                hole=.4),#Taille du trou au milieu du camembert
            row=1, 
            col=1
            ).update_layout(height=700,template="plotly_dark")

        #Carte du monde
        #Renseignement des paramètres de la figure
        figMonde.add_trace(go.Scattergeo(
            lat=self.df["latitude"],
            lon=self.df["longitude"],
            text=self.df["Location"] + ' : ' + self.df["Totalpassengers"].apply(str) + ' Visiteurs en 2021.',
            mode="markers",
            #Permet d'avoir une information qui apparait quand on passe la souris sur un point
            hoverinfo="text+lat+lon",
            showlegend=False,
            #parametrage des points
            marker=dict(
                color=self.df["Totalpassengers"], 
                size=self.df["Totalpassengers"]/1500000, 
                opacity=0.8)
            ),
            row=1, 
            col=1
            ).update_layout(height=800,template="plotly_dark")

        #permet d'ajouter des caractéristique sur la carte du monde, par exemple afficher les fleuves et les frontieres 
        figMonde.update_geos(
            projection_type="orthographic",
            landcolor="white",#Couleur des pays
            oceancolor="#006994",#couleur des océans
            coastlinewidth = 2,#Taille des frontières côtières 
            countrywidth = 2,#Taille des frontières entre les pays
            showcountries = True,#afficher les frontières pour voir les pays
            rivercolor = "blue",#Choisir de la couleur des fleuves
            showrivers = True,#Afficher les fleuves
            riverwidth = 1,#Taille des fleuves
            showocean=True,#Affiche les océans
            lakecolor="LightBlue"#Choix de la couleur des lacs
        )

        #Cette partie est dédiée à l'HTML, 
        #Les html.H1, H2, H3 correspondent aux titres ou sous titre donc plus gros que le reste.
        #Les html.P correspondent aux paragraphes
        #Les html.Br() permettent d'aller a la ligne
        #Les dcc.Graph permettent d'afficher une figure en spécifiant l'ID, la figure et la taille
        app.layout = html.Div( style={'backgroundColor': colors['background']},children=[
        html.H1(
            children='Les aéroports les plus visités de monde face au Covid-19.',#Choix du texte
            style={
                'textAlign': 'center',#On le veut centrer sur la page
                'color': colors['title'],#On choisi la couleur définit plus haut
                'border':'thick double #32a1ce'#On choisi une bordure autour du texte
            }
        ),
        html.H2(["Le but de notre dashboard est, en premier temps de représenter précisémment la plupart des aéroports du monde.",
            " Ensuite, nous avons voulus sélectionner seulement les 50 premiers pour avoir une meilleure idée de la répartition dans le monde et ainsi pouvoir afficher un diagramme en bâton et un camembert.",
            html.Br(),
            "Pour terminer, on a voulu représenter l'impact du Covid-19 sur les aéroports Européens."
            ],
            style={
                    'textAlign': 'center',
                    'color': '#828FA4'
                }
        ),
        dcc.Graph(
            id='graph1',
            figure=figCarteEntiere,
            style={
                "width": "100%",#Taille de la figure qui s'adapte en fonction de l'écran de l'utilisateur
                "height": "100%"
            }
        ),
        html.H3(
            children='Représentation de 7000 aéroports dans le monde.',
            style={
                'textAlign': 'center',
                'color': colors['title'],
                "text-decoration":"underline"#Permet de souligner un texte
            }
        ),
        html.P("Nous pouvons nous déplacer dans le monde entier pour observer et découvrir tous les emplacements où il y a un aéroport. En passant la souris sur un point, on y apprend son nom.",
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),
        dcc.Graph(
            id='graph2',
            figure=figMonde,
        ),
        html.H3(
            children='Top 50 des aéroports les plus visités dans le monde en 2021.',
            style={
                'textAlign': 'center',
                'color': colors['title'],
                "text-decoration":"underline"
            }
        ),
        html.P("En cliquant quelque part et ensuite en déplassant sa souris, la terre tourne sur elle-même et laisse apparaitre 50 points plus ou moins gros. Plus le point est gros, plus il y a eu des visiteurs dans l'aéroport durant l'année(la couleur signifie la même chose).",
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),
        dcc.Graph(
            id='graph3',
            figure=figBar
        ),
        html.H3(
            children='Diagramme en bâton représentant les aéroports avec le plus de visiteurs.',
            style={
                'textAlign': 'center',
                'color': colors['title'],
                "text-decoration":"underline"
            }
        ),
        html.P("Cette figure permet de condenser toutes les informations présentent sur la carte précédente pour pouvoir mieux analyser les chiffres.",
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),
        dcc.Graph(
            id='graph4',
            figure=figPie
        ),
        html.H3(
            children='Camembert avec le nombre de visiteurs par pays durant l\'année 2021.',
            style={
                'textAlign': 'center',
                'color': colors['title'],
                "text-decoration":"underline"
            }
        ),
        html.P("Ce graphique regroupe pas pays la somme de tous les voyageurs durant l'année 2021 mais seulement pour les 50 aéroports les plus grands du monde. N'en prendre seulement 50 est un choix, cela suffit pour pouvoir représenter,remarquer le monopole et la puissance des États-Unis ainsi que de la Chine.",
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),
        dcc.Graph(
            id='graph5',
            figure=figCovid
        ),
        html.H3(
            children='Représentation du nombre de voyageur en Europe pendant la période du Covid-19.',
            style={
                'textAlign': 'center',
                'color': colors['title'],
                "text-decoration":"underline"
            }
        ),
        html.P("Choisir une année:",
            style={
                'color': colors['title']
            }
        ),
        #Permet d'ajouteur un "slider" ou curseur pour le choix de l'année que l'on veut afficher
        dcc.Slider(2015,2020,#valeur de départ et de fin
            step=None,#pas de pas entre les choix
            value=2015,#valeur de départ
            marks={#différents points sur le curseur
                2015: '2015',
                2016: '2016',
                2017: '2017',
                2018: '2018',
                2019: '2019',
                2020: '2020'
            },
            id='year'
        ),
        html.P("Ce dernier graphique est dynamique et nous avons la possibilité de choisir l\'année des données en déplaçant le curseur. Cette particularité nous permet de nous placer en 2019 puis en 2020 afin de se rendre compte des conséquence qu\'a eu la crise du Covid-19 sur le tourisme et les aéroports. On remarque une baisse d\'environ 70 pourcent en Métropole et 50 pourcent en Outre-mer. La courbe ne change pas beaucoup visuellement, seulement les valeur en ordonné changent, ce qui veut dire que le Covid-19 à touché tous les aéroports en même temps.",
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),
        html.P(".",
            style={
                'textAlign': 'left',
                'color': 'black'
            }
        )
        ]
        )
        #permet de rendre un graphique dynamique avec un parametrage sur la page internet
        @app.callback(
             
            Output("graph5", "figure"),#On choisi quel graphique va être impliqué 
            Input("year", "value"))#On choisi quel valeur va changer
        #permet de mettre a jour le graphique a fonction du choix de l'utilisateur 
        def display_year(year):
            df = self.dfeurope 
            fig = px.line(df, 
                x='Ligne aérienne', #valeur en abscisse
                y=str(year),#valeur en ordonnée qui va changer
                color_discrete_sequence = ['red'],#Choix de la couleur de la courbe
                markers = True,#On affiche des points sur la courbe
                template="plotly_dark",
                line_shape='spline')
            return fig

        app.run_server(debug=True) #On lance le serveur
