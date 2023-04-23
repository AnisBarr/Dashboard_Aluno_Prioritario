import pickle
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import joblib


# Charger le modèle
with open("notebooks/02_models/kmeans_model.joblib", "rb") as f:
    modele_kmeans = joblib.load(f)

# Charger les données
donnees = pd.read_csv("data/student_data.csv")
#/Users/soniabouden/Downloads/ekinox/

# Initialiser l'application Dash
app = dash.Dash(__name__)

# Ajouter le logo en haut à droite
logo = html.Img(src=app.get_asset_url('logo.png'), style={"margin":"20px", "position": "absolute", "top": 0, "right": 0})

# Créer les options pour la liste déroulante des écoles
escolas = donnees["school"].unique()
opcoes_escolas = [{"label": escola, "value": escola} for escola in escolas]

# Définir la mise en page de l'application
app.layout = html.Div([
    logo,
    html.H1("Dashboard Aluno Prioritário", style={"margin":"20px"}),
    html.Div([
        html.Label("Selecione uma escola: "),
        dcc.Dropdown(
            id='dropdown-escola',
            options=opcoes_escolas,
            value=escolas[0],
            style={"width": "50%"}
        ),
        html.Br(),
        html.Label("Selecione um aluno: "),
        
        html.Br(),
        html.Label("Filtros: "),
        dcc.Checklist(
            id='filtros',
            options=[
                {'label': 'Suporte educacional extra', 'value': 'schoolsup'},
                {'label': 'Suporte educacional familiar', 'value': 'famsup'},
                {'label': 'Aulas particulares pagas', 'value': 'paid'},
                {'label': 'Deseja continuar estudando', 'value': 'higher'},
                {'label': 'Acesso à internet em casa', 'value': 'internet'}
            ],
            value=[]
        ),
        html.Br(),
        html.Label("Tempo de viagem de casa para a escola: "),
        dcc.RadioItems(
            id='tempo_viagem',
            options=[
                {'label': '< 15 min', 'value': '1'},
                {'label': '15-30 min', 'value': '2'},
                {'label': '30 min - 1 hora', 'value': '3'},
                {'label': '> 1 hora', 'value': '4'}
            ],
            value='1'
        ),
        html.Br(),
        html.Label("Tempo de estudo semanal: "),
        dcc.RadioItems(
            id='tempo_estudo',
            options=[
                {'label': '< 2 horas', 'value': '1'},
                {'label': '2-5 horas', 'value': '2'},
                {'label': '5-10 horas', 'value': '3'},
                {'label': '> 10 horas', 'value': '4'}
            ],
            value='1'
        ),
        html.Br(),
        html.Label("Número de reprovações em anos anteriores: "),
        dcc.Slider(
            id='reprovacoes_slider',
            min=0,
            max=3,
            marks={
                0: '0',
                1: '1',
                2: '2',
                3: '3 ou mais'
            },
            value=0,
            className='custom-slider'
        ),    
        html.Br(),
        html.Button('Validar', id='valider'),
    ], className='sidebar', style={'width': '20%', 'float': 'center','margin-top': '5%', 'margin-left': '2%'}),
    html.Div(
    children=[
        html.Iframe(
            src="assets/my_plot.html",
            style={'display': 'flex', 'flex-grow': '1', 'margin-left': '20%',"height": "850px", "width": "76%", 'margin-top': '5%', 'margin-right': '2%'},
        )
    ])
                    
])

# @app.callback(
#     Output('graphique', 'figure'),
#     Input('dropdown-eleve', 'value'),
#     Input('filtres', 'value'),
#     Input('dropdown-ecole', 'value')
# )
# def update_figure(eleve, filtres, ecole):
#     # Filtrer les données en fonction de l'école et de l'étudiant sélectionnés
#     if eleve is not None:
#         donnees_filtrees = donnees[(donnees["school"] == ecole) & (donnees["StudentID"] == eleve)]
#     else:
#         donnees_filtrees = donnees[donnees["school"] == ecole]

#     # Appliquer les filtres sélectionnés
#     for filtre in filtres:
#         donnees_filtrees = donnees_filtrees[donnees_filtrees[filtre] == 1]

#     # Initialiser la liste des matières
#     matieres = list(donnees_filtrees.columns[7:13])

#     # Calculer la moyenne des notes des matières pour l'étudiant sélectionné
#     moyennes_matieres = {}
#     for matiere in matieres:
#         moyenne_matiere = donnees_filtrees[matiere].mean()
#         moyennes_matieres[matiere] = moyenne_matiere

#     # Créer un graphique en barres avec les moyennes des notes des matières pour l'étudiant sélectionné
#     fig = px.bar(x=list(moyennes_matieres.keys()), y=list(moyennes_matieres.values()), title="Moyennes des notes des matières")
#     return fig

if __name__ == '__main__':
    app.run_server(debug=True) 
