FROM python:3.11-slim

# Variables d'environnement
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Répertoire de travail
WORKDIR /app

# Installer les dépendances système pour PostgreSQL
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copier requirements et installer
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier TOUT le dossier app/
COPY app/ /app/

# Exposer le port
EXPOSE 5000

# Commande de démarrage
CMD ["python", "app.py"]
