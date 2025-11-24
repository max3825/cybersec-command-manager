#!/bin/bash

echo "🔐 Génération de secrets sécurisés..."
echo ""

# Générer un SECRET_KEY
SECRET_KEY=$(openssl rand -hex 32)
echo "SECRET_KEY=${SECRET_KEY}"

# Générer un mot de passe PostgreSQL
POSTGRES_PASSWORD=$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-25)
echo "POSTGRES_PASSWORD=${POSTGRES_PASSWORD}"

# Générer un mot de passe PgAdmin
PGADMIN_PASSWORD=$(openssl rand -base64 24 | tr -d "=+/" | cut -c1-20)
echo "PGADMIN_DEFAULT_PASSWORD=${PGADMIN_PASSWORD}"

echo ""
echo "✅ Copie ces valeurs dans ton fichier .env"
echo "⚠️  NE PARTAGE JAMAIS CES SECRETS !"
