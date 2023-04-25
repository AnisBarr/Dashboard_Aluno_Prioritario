import pickle
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.express as px
import joblib
from plotly.offline import plot


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
        html.Label("Digite a nota final do aluno: "),
        html.Br(),
        dcc.Input(id='grade_input', type='number', min=0, max=20, step=1, style={"width": "50%"}),
        html.Br(),
        html.Label("Filtros: "),
        html.Br(),
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
        html.Div([
            html.H4('Consumo de álcool durante a semana'),
            dcc.Slider(
                id='dalc_slider',
                min=1,
                max=5,
                marks={i: str(i) for i in range(1, 6)},
                value=3,
                className='custom-slider'
            ),
            html.H4('Consumo de álcool nos fins de semana'),
            dcc.Slider(
                id='walc_slider',
                min=1,
                max=5,
                marks={i: str(i) for i in range(1, 6)},
                value=3,
                className='custom-slider'
                
            ),
            html.H4('Estado de saúde atual'),
            dcc.Slider(
                id='health_slider',
                min=1,
                max=5,
                marks={i: str(i) for i in range(1, 6)},
                value=3,
                className='custom-slider'
                
            ),
            html.H4('Número de faltas na escola'),
            dcc.Input(
                id='absences_input',
                type='number',
                value=0
            ),
        ]),
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
            src="assets/complexidade.html",
            style={'display': 'flex', 'flex-grow': '1', 'margin-left': '20%',"height": "850px", "width": "76%", 'margin-top': '5%', 'margin-right': '2%'},
        )
    ])
                    
])

n_clicks = 0  # initialisation de la variable n_clicks

# # Callback pour collecter les variables et créer le dataframe
# @app.callback(
#     Output('output-data', 'children'),
#     Input('valider', 'n_clicks'),
#     # State('grade_input', 'value'),
#     State('dropdown-escola', 'value'),
#     State('filtros', 'value'),
#     State('tempo_viagem', 'value'),
#     State('tempo_estudo', 'value'),
#     State('reprovacoes_slider', 'value')
# )
# def collect_data(n_clicks, filtros, tempo_viagem, tempo_estudo, reprovacoes):
#     data = {
#         'internet': 1 if 'internet' in filtros else 0,
#         'higher': 1 if 'higher' in filtros else 0,
#         'traveltime': int(tempo_viagem),
#         'studytime': int(tempo_estudo),
#         'failures': int(reprovacoes),
#         'Dalc': int(dalc),
#         'Walc': int(walc),
#         'health': int(health),
#         'absences': int(absences)
#         # 'FinalGrade': int(grade_input)
#     }
#     df = pd.DataFrame(data, index=[0])
#     return df

# # Appeler la fonction de collecte de données et stocker les résultats dans un DataFrame
# df = collect_data(n_clicks, filtros, tempo_viagem, tempo_estudo, reprovacoes)
# print(df)



# def calcul_complexite(df, studytime, failures, Walc, Dalc, internet, higher, absences):
#     # Calcul de la nouvelle complexité
#     new_complexity = studytime*(-0.5) + failures*(0.5) + failures*0.44 + Walc*(0.75) + Dalc*(0.78) + internet*(-0.56) + higher*(-0.6)
    
#     # Création de la nouvelle observation
#     new_observation = pd.DataFrame({'studytime': [studytime],
#                                     'failures': [failures],
#                                     'Walc': [Walc],
#                                     'Dalc': [Dalc],
#                                     'internet': [internet],
#                                     'higher': [higher],
#                                     'absences': [absences],
#                                     'Complexidade': [new_complexity]})
    
#     # Ajout de la nouvelle observation au dataframe
#     df = df.append(new_observation, ignore_index=True)
    
#     # Création de la figure interactive avec la nouvelle observation
#     fig = px.scatter(df, x='FinalGrade', y='Complexidade', color='school', hover_name='FamilyName', size='absences')
#     fig.add_trace(px.scatter(new_observation, x='FinalGrade', y='Complexidade', color='red').data[0])
    
#     # Ajout du titre à la figure
#     fig.update_layout(
#         title={
#             'text': "Priorização dos alunos a serem acompanhados com base na complexidade e valor do acompanhamento.",
#             'y':0.95,
#             'x':0.5,
#             'xanchor': 'center',
#             'yanchor': 'top'})
    
#     # Affichage de la figure
#     plot(fig, filename='/assets/complexidade.html', auto_open=False)
    
#     # Retourne le dataframe avec la nouvelle observation ajoutée
#     return df

if __name__ == '__main__':
    app.run_server(debug=True) 
