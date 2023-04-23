import dash
import dash_bootstrap_components as dbc
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from sklearn.cluster import KMeans
import plotly.graph_objs as go


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Charger les données
ds = pd.read_csv("data/student_data.csv")
logo = html.Img(src=app.get_asset_url('logo.png'), style={"margin":"20px", "position": "absolute", "top": 0, "right": 0})
ds = ds[['age', 'traveltime', 'studytime', 'failures','Dalc', 'Walc', 'health', 'absences', 'FinalGrade']]

# Créer le modèle KMeans
kmeans = KMeans(n_clusters=3, n_init=10, random_state=0).fit(ds[['age', 'traveltime', 'studytime', 'failures','Dalc', 'Walc', 'health', 'absences']])
cluster_palette = ['#EF476F', '#06D6A0', '#118AB2', '#1183B2', '#128AB2']

controls = dbc.Card(
    [
        html.Div(
            [
                dbc.Label("X variable"),
                dcc.Dropdown(
                    id="x-variable",
                    options=[
                        {"label": col, "value": col} for col in ds.columns
                    ],
                    value="absences",
                ),
            ]
        ),
        html.Div(
            [
                dbc.Label("Y variable"),
                dcc.Dropdown(
                    id="y-variable",
                    options=[{"label": "FinalGrade", "value": "FinalGrade"}],
                    value="FinalGrade",
                ),
            ]
        ),
        html.Div(
            [
                dbc.Label("Cluster count"),
                dbc.Input(id="cluster-count", type="number", value=3),
            ]
        ),
    ],
    body=True,
)

app.layout = dbc.Container(
    [   logo,
        html.H1("Dashboard Aluno Prioritário", style={"margin":"20px"}),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls, md=4),
                dbc.Col(dcc.Graph(id="cluster-graph"), md=8),
            ],
            align="center",
        ),
    ],
    fluid=True,
)


@app.callback(
    Output("cluster-graph", "figure"),
    [
        Input("x-variable", "value"),
        Input("y-variable", "value"),
        Input("cluster-count", "value"),
    ],
)
def make_graph(x, y, n_clusters):
    # minimal input validation, make sure there's at least one cluster
    km = KMeans(n_clusters=max(n_clusters, 1))
    df = ds.loc[:, [x, y]]

    km.fit(df.values)
    df["cluster"] = km.labels_

    centers = km.cluster_centers_

    data = [
        go.Scatter(
            x=df.loc[df.cluster == c, x],
            y=df.loc[df.cluster == c, y],
            mode="markers",
            marker={"size": 8},
            name="Cluster {}".format(c),
        )
        for c in range(n_clusters)
    ]

    data.append(
        go.Scatter(
            x=centers[:, 0],
            y=centers[:, 1],
            mode="markers",
            marker={"color": "#000", "size": 12, "symbol": "diamond"},
            name="Cluster centers",
        )
    )

    layout = {"xaxis": {"title": x}, "yaxis": {"title": y}}

    return go.Figure(data=data, layout=layout)


# make sure that x and y values can't be the same variable
def filter_options(v):
    """Disable option v"""
    return [
        {"label": col, "value": col, "disabled": col == v}
        for col in ds.columns
    ]


# functionality is the same for both dropdowns, so we reuse filter_options
app.callback(Output("x-variable", "options"), [Input("y-variable", "value")])(
    filter_options
)
# app.callback(Output("y-variable", "options"), [Input("x-variable", "value")])(
#     filter_options
# )


if __name__ == "__main__":
    app.run_server(debug=True, port=8888)