#!/bin/bash

echo "🔍 Vérification de la configuration..."
echo ""

# Vérifier si .env existe
if [ ! -f .env ]; then
    echo "❌ Fichier .env introuvable !"
    exit 1
fi

echo "✅ Fichier .env trouvé"
echo ""

# Charger les variables
source .env

# Vérifier les variables critiques
echo "📋 Variables chargées :"
echo "  - POSTGRES_USER: ${POSTGRES_USER:-❌ Non défini}"
echo "  - POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:+✅ Défini (caché)}"
echo "  - POSTGRES_DB: ${POSTGRES_DB:-❌ Non défini}"
echo "  - SECRET_KEY: ${SECRET_KEY:+✅ Défini (caché)}"
echo "  - FLASK_ENV: ${FLASK_ENV:-❌ Non défini}"
echo "  - DATABASE_URL: ${DATABASE_URL:+✅ Défini}"
echo ""

# Vérifier si les mots de passe par défaut sont encore utilisés
if [[ "$POSTGRES_PASSWORD" == "secure_password_here" ]]; then
    echo "⚠️  ATTENTION: Mot de passe PostgreSQL par défaut détecté !"
fi

if [[ "$SECRET_KEY" == "your-super-secret-key-change-me" ]]; then
    echo "⚠️  ATTENTION: SECRET_KEY par défaut détectée !"
fi

if [[ "$PGADMIN_DEFAULT_PASSWORD" == "admin_password_change_me" ]]; then
    echo "⚠️  ATTENTION: Mot de passe PgAdmin par défaut détecté !"
fi

echo ""
echo "✅ Vérification terminée"
