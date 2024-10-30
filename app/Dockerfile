# Utiliser une image de base officielle de Python
FROM python:3.12-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances
RUN pip install --no-cache-dir streamlit 

# Copier le fichier de l'application Streamlit
COPY ./app /app

# Exposer le port utilisé par Streamlit
EXPOSE 8501

# Commande pour lancer l'application Streamlit
CMD ["streamlit", "run", "app_streamlit.py"]