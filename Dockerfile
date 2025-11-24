FROM python:3.11-slim

# Variables d'environnement
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DEBIAN_FRONTEND=noninteractive

# Répertoire de travail
WORKDIR /app

# Installer les dépendances système pour PostgreSQL
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    postgresql-client \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Créer les dossiers nécessaires
RUN mkdir -p /app/data /app/logs /app/uploads

# Copier requirements et installer les dépendances Python
COPY app/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copier TOUT le dossier app/
COPY app/ /app/

# Définir les permissions
RUN chmod -R 755 /app && \
    chmod +x /app/*.py 2>/dev/null || true

# Exposer le port
EXPOSE 5000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000').read()" || exit 1

# Commande de démarrage par défaut (peut être overridée par docker-compose)
CMD ["python", "app.py"]
