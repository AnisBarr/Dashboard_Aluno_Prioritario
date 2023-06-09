# Utiliser une image de base existante
FROM python:3.9-slim

# Copier les fichiers du projet dans l'image Docker
COPY . /app

# Se déplacer dans le répertoire de travail
WORKDIR /app

# Installer les dépendances du projet
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    ffmpeg libsm6 libxext6 \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*


# Copiez le code de l'application Dash 1 dans le conteneur
COPY app1 app1

# Copiez le code de l'application Dash 2 dans le conteneur
COPY app2 app2


# Installez les dépendances
RUN pip install --no-cache-dir -r app1/requirements.txt && pip install --no-cache-dir -r app2/requirements.txt


# Définir les variables d'environnement pour chaque application
ENV APP1_PORT=8050
ENV APP2_PORT=8888

# Exposez les ports des deux applications
EXPOSE $APP1_PORT
EXPOSE $APP2_PORT

#healthcheck
HEALTHCHECK CMD curl --fail http://localhost:$APP1_PORT/_stcore/health && curl --fail http://localhost:$APP2_PORT/_stcore/health

# Commande pour exécuter le script de démarrage
CMD ["sh", "start.sh"]

HEALTHCHECK CMD curl --fail http://localhost:$APP1_PORT/_stcore/health && curl --fail http://localhost:$APP2_PORT/_stcore/health
