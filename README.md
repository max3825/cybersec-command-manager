# 🛡️ CyberSec Command Manager

Gestionnaire de commandes et ressources pour professionnels de la cybersécurité. Base de données centralisée d'outils, CVE, certifications et cheat sheets.

## ⚡ Quick Start

git clone <repo>
cd cybersec-command-manager
docker compose up -d

Accès : http://localhost:5000

## 📦 Stack

- **Backend** : Flask + SQLAlchemy
- **Base de données** : PostgreSQL 15
- **Frontend** : HTML/CSS/JS vanilla
- **Déploiement** : Docker Compose

## 🗂️ Contenu

- **97 commandes** Linux/Windows (nmap, grep, netstat, etc.)
- **51 outils** de pentest (Metasploit, Burp Suite, etc.)
- **50 CVE** avec détails et mitigations
- **12 certifications** (OSCP, CEH, CISSP, etc.)
- **32 cheat sheets** catégorisés
- **Notes personnelles** persistantes

## 🔧 Configuration

### Variables d'environnement (.env)

POSTGRES_USER=postgres
POSTGRES_PASSWORD=votre_mot_de_passe
POSTGRES_DB=cybersec_manager
SECRET_KEY=votre_secret_key
FLASK_ENV=production
FLASK_DEBUG=0

### Commandes Docker

docker compose up -d
docker compose logs -f web
docker compose build --no-cache
docker compose down
docker compose down -v

## 📊 Endpoints API

GET    /api/commands           # Liste des commandes
POST   /api/commands           # Ajouter une commande
GET    /api/tools              # Liste des outils
GET    /api/vulnerabilities    # Liste des CVE
GET    /api/certifications     # Certifications
GET    /api/notes              # Notes personnelles
POST   /api/notes              # Créer une note
GET    /api/search?q=nmap      # Recherche globale
GET    /health                 # Health check

## 🎯 Fonctionnalités

- ✅ Recherche globale multi-tables
- ✅ Filtres par catégorie, plateforme, niveau
- ✅ Favoris et historique
- ✅ Export JSON
- ✅ Persistance PostgreSQL
- ✅ Interface responsive

## 🗄️ Backup & Restore

docker compose exec db pg_dump -U postgres cybersec_manager > backup.sql
docker compose exec -T db psql -U postgres cybersec_manager < backup.sql

## 📁 Structure

cybersec-command-manager/
├── app/
│   ├── app.py                 # Application Flask
│   ├── models.py              # Modèles SQLAlchemy
│   ├── migrate_json_to_db.py  # Script d'import
│   ├── templates/             # Templates HTML
│   ├── static/                # CSS/JS/Assets
│   └── data/                  # Fichiers JSON source
├── docker-compose.yml
├── Dockerfile
├── .env
└── README.md

## 🚀 Développement

docker compose -f docker-compose.yml -f docker-compose.dev.yml up
docker compose exec web bash
docker compose exec db psql -U postgres -d cybersec_manager

## 🔒 Sécurité

- ⚠️ Changer les mots de passe par défaut en production
- ⚠️ Ne pas exposer le port 5432 en production
- ⚠️ Utiliser Gunicorn ou uWSGI au lieu du serveur Flask dev
- ✅ Les volumes Docker assurent la persistance des données

## 📝 TODO

- [ ] Authentification utilisateur
- [ ] API REST complète avec authentification JWT
- [ ] Dark mode
- [ ] Export PDF des cheat sheets
- [ ] Intégration MITRE ATT&CK
- [ ] Notifications de nouvelles CVE

## 📄 Licence

MIT

## 👤 Auteur

Projet réalisé dans le cadre d'un apprentissage en cybersécurité.

---

**Made with ☕ by a cybersecurity enthusiast**
