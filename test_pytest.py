import pytest
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from app import app

# Test de la création de l'application Dash
def test_dash_app():
    assert isinstance(app, dash.Dash)

# Test du layout
def test_layout():
    assert isinstance(app.layout, html.Div)
    assert len(app.layout.children) == 7
    assert isinstance(app.layout.children[0], html.H1)

# Test des listes déroulantes des écoles et des étudiants
def test_dropdowns():
    assert isinstance(app.layout.children[2], dcc.Dropdown)
    assert app.layout.children[2].id == 'dropdown-ecole'
    assert isinstance(app.layout.children[4], dcc.Dropdown)
    assert app.layout.children[4].id == 'dropdown-eleve'

# Test des filtres
def test_filters():
    assert isinstance(app.layout.children[6], dcc.Checklist)
    assert app.layout.children[6].id == 'filtres'

# Test de la fonction de mise à jour des options de la liste déroulante des étudiants
def test_update_options_eleves():
    with app.app_context():
        app.callback_map[Output('dropdown-eleve', 'options')].inputs[0]['id'] == 'dropdown-ecole'
        options = app.callback_map[Output('dropdown-eleve', 'options')].func(ecole='GP')
        assert len(options) == 7
        assert options[0]['value'] == 'GP_001'

# Test de la fonction de mise à jour du graphique
def test_update_figure():
    with app.app_context():
        app.callback_map[Output('graphique', 'figure')].inputs[0]['id'] == 'dropdown-eleve'
        app.callback_map[Output('graphique', 'figure')].inputs[1]['id'] == 'filtres'
        fig = app.callback_map[Output('graphique', 'figure')].func(eleve='GP_001', filtres=['schoolsup', 'internet'])
        assert isinstance(fig, dict)
        assert fig['data'][0]['x'] == ['Portuguese', 'Mathematics', 'Science', 'History', 'Geography', 'English']
