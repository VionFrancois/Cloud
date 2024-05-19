# Utilisez une image Python comme base
FROM python:3.10

# Définir le répertoire de travail
WORKDIR /service

# Copier les fichiers nécessaires dans l'image Docker
COPY requirements.txt requirements.txt
COPY recherche.py recherche.py
COPY Features_train/ Features_train/

# Installer les dépendances
RUN pip install -r requirements.txt

# Commande à exécuter lorsque le conteneur démarre
ENTRYPOINT ["python3", "recherche.py"]

CMD ["0","20"]