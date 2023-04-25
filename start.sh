#!/bin/sh

# Démarrer l'application Dash 1
python -m aluno_prioritario1.py --port $APP1_PORT &

# Démarrer l'application Dash 2
python -m clusters.py --port $APP2_PORT &