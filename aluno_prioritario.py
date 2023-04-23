import pickle
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import joblib

# Charger le modèle
with open("/Users/soniabouden/Downloads/ekinox/notebooks/02_models/kmeans_model.joblib", "rb") as f:
    modele_kmeans = joblib.load(f)

# Charger les données
donnees = pd.read_csv("/Users/soniabouden/Downloads/ekinox/data/student_data.csv")

# Initialiser l'application Dash
app = dash.Dash(__name__)

# Ajouter le logo en haut à droite
logo = html.Div(html.Img(src="/Users/soniabouden/Downloads/ekinox/src/logo.png", style={"height": "50px", "width": "auto", "position": "absolute", "top": 0, "right": 0}))


# Créer les options pour la liste déroulante des écoles
ecoles = donnees["school"].unique()
options_ecoles = [{"label": ecole, "value": ecole} for ecole in ecoles]

# Créer les options pour la liste déroulante des étudiants
options_eleves = [{"label": eleve, "value": eleve} for eleve in donnees[donnees["school"] == ecoles[0]]["StudentID"].unique()]

# Définir la mise en page de l'application
app.layout = html.Div([
    html.H1("Dashboard Aluno Prioritário"),
    html.Label("Selecione uma escola: "),
    dcc.Dropdown(
        id='dropdown-ecole',
        options=options_ecoles,
        value=ecoles[0],
        style={"width": "50%"}
    ),
    html.Br(),
    html.Label("Selecione um aluno: "),
    dcc.Dropdown(
        id='dropdown-eleve',
        options=options_eleves,
        style={"width": "50%"}
    ),
    html.Br(),
    html.Label("Filtros: "),
    dcc.Checklist(
        id='filtres',
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
    html.Button('Validar', id='valider'),
    html.Br(),
    dcc.Graph(id='graphique')
])

# Définir la fonction de mise à jour des options de la liste déroulante des étudiants
@app.callback(
    Output('dropdown-eleve', 'options'),
    Input('dropdown-ecole', 'value')
)
def update_options_eleves(ecole):
    eleves = donnees[donnees["school"] == ecole]["StudentID"].unique()
    options_eleves = [{"label": eleve, "value": eleve} for eleve in eleves]
    return options_eleves

# Définir la fonction de mise à jour du graphique
@app.callback(
    Output('graphique', 'figure'),
    Input('dropdown-eleve', 'value'),
    Input('filtres', 'value')
)

# Définir la fonction de mise à jour du graphique
@app.callback(
    Output('graphique', 'figure'),
    Input('dropdown-eleve', 'value'),
    Input('filtres', 'value')
)
def update_figure(eleve, filtres):
    # Récupérer la valeur de la liste déroulante des écoles
    ecole = dash.callback_context.inputs['dropdown-ecole.value']

    # Filtrer les données en fonction de l'école et de l'étudiant sélectionnés
    if eleve is not None:
        donnees_filtrees = donnees[(donnees["school"] == ecole) & (donnees["StudentID"] == eleve)]
    else:
        donnees_filtrees = donnees[donnees["school"] == ecole]

    # Appliquer les filtres sélectionnés
    for filtre in filtres:
        donnees_filtrees = donnees_filtrees[donnees_filtrees[filtre] == 1]

    # Initialiser la liste des matières
    matieres = list(donnees_filtrees.columns[7:13])

    # Calculer la moyenne des notes des matières pour l'étudiant sélectionné
    moyennes_matieres = {}
    for matiere in matieres:
        moyenne_matiere = donnees_filtrees[matiere].mean()
        moyennes_matieres[matiere] = moyenne_matiere

    # Créer un graphique en barres avec les moyennes des notes des matières pour l'étudiant sélectionné
    fig = px.bar(x=list(moyennes_matieres.keys()), y=list(moyennes_matieres.values()), title="Moyennes des notes des matières")
    return fig

if __name__ == '__main__':
    app.run_server(debug=True) 
