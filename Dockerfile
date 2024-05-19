# Utilisez une image Python comme base
FROM python:3.10

# Définir le répertoire de travail
WORKDIR /service

# Copier les fichiers nécessaires dans l'image Docker
COPY searchEngine/ /service/searchEngine/

# Installer les dépendances
RUN pip install -r /service/searchEngine/requirements.txt

EXPOSE 8000

RUN chmod +x /service/searchEngine/start.sh

# Commande à exécuter lorsque le conteneur démarre
CMD ["/service/searchEngine/start.sh"]