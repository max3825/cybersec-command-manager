# 🛡️ CyberSec Command Manager

> **Gestionnaire intelligent de commandes cybersécurité avec dashboard, recherche globale et base de données PostgreSQL.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![PostgreSQL 15](https://img.shields.io/badge/PostgreSQL-15-darkblue.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Supported-blue.svg)](https://www.docker.com/)

---

## 📋 Vue d'ensemble

**CyberSec Command Manager** est une application web moderne pour cataloguer, rechercher et gérer les commandes de cybersécurité, les certifications, les outils, les CVE et bien plus.

### Parfait pour :
- 📚 **Apprentissage cybersécurité** - Référence complète des commandes
- 🎓 **Préparation certifications** - OSCP, CEH, CISSP, Security+
- 🔧 **Opérations pentest** - Quick reference pendant les missions
- 📖 **Documentation personnelle** - Notes synchronisées
- 🏢 **Formation d'équipes** - Support pour les groupes de sécurité

---

## ✨ Fonctionnalités

### 🎯 Core Features
- ✅ **Gestionnaire de commandes** - Cataloguez et recherchez 50+ commandes
- ✅ **Recherche globale** - Cross-module avec autocomplétion
- ✅ **Dashboard intelligent** - Stats, raccourcis, commandes récentes
- ✅ **Favoris personnalisés** - Sauvegardez vos commandes
- ✅ **Interface responsive** - Desktop, tablette, mobile
- ✅ **Design moderne** - Glassmorphisme, dark mode

### 📦 Modules
- 📋 **Commandes** - 50+ commandes cybersec avec documentation
- 📜 **Certifications** - OSCP, CEH, CISSP, CompTIA Security+
- 📚 **Cheat Sheets** - Guides rapides (Linux, Web, Networks)
- 📝 **Notes** - Documentation personnelle synchronisée
- 🔧 **Outils** - Nmap, Metasploit, Burp Suite, etc.
- 🔒 **Vulnérabilités** - Base de CVE avec mitigations

### 🗄️ Backend
- 🐘 **PostgreSQL 15** - Base de données robuste
- 🐍 **Flask** - Framework web léger et rapide
- 🐳 **Docker Compose** - Déploiement facile
- 📊 **SQLAlchemy ORM** - Modèles BD élégants
- 🔌 **API REST** - Endpoints JSON pour toutes les opérations

---

## 🚀 Démarrage rapide

### Prérequis
- **Docker** & **Docker Compose** ([installer](https://docs.docker.com/get-docker/))
- **Git** (optionnel)

### Installation (5 minutes)

#### 1. Cloner/télécharger le projet
git clone https://github.com/ton-username/cyber-tool2.git
cd cyber-tool2
#### 2. Configuration
Fichier .env est déjà configuré, tu peux le modifier si nécessaire
cat .env


#### 3. Lancer l'application
docker-compose up --build
#### 4. Accéder à l'app
- 🌐 **Application** : http://localhost:5000
- 🗃️ **PgAdmin** (gérer DB) : http://localhost:5050
  - Email: `admin@cybersec.local`
  - Password: `admin`

**C'est tout ! L'app démarre avec toutes les données importées automatiquement.** ✨

---
### Avec Docker Compose
Démarrer
docker-compose up -d

Voir les logs
docker-compose logs -f

Terminal Flask
docker-compose exec web bash

Terminal PostgreSQL
docker-compose exec db psql -U postgres -d cybersec_manager

Arrêter
docker-compose down

Supprimer tout (données incluses)
docker-compose down -v

text

---

## 📊 Structure du projet

cyber-tool2/
├── app/
│ ├── app.py # Application Flask
│ ├── models.py # Modèles SQLAlchemy
│ ├── migrate_json_to_db.py # Import JSON → PostgreSQL
│ ├── templates/ # Templates Jinja2
│ ├── static/ # CSS, JS, images
│ └── data/ # Fichiers JSON (données)
├── Dockerfile # Configuration Docker
├── docker-compose.yml # Orchestration Docker+PostgreSQL
├── requirements.txt # Dépendances Python
├── .env # Variables d'environnement
└── README.md # Ce fichier

text

---

## 🗂️ Modules disponibles

### 📋 Commandes
**Route** : `/commandes`

Gère une base de données complète de commandes cybersécurité.

**Champs** :
- Nom et description
- Catégorie (Reconnaissance, Exploitation, etc.)
- Plateforme (Linux, Windows)
- Arguments et options
- Exemple d'utilisation
- Use case (quand l'utiliser)
- Tags (recherche)
- Niveau (Débutant/Intermédiaire/Avancé)
- Lien documentation officielle

**Actions** :
- ✅ Recherche par nom/description/tags
- ✅ Filtrer par catégorie/plateforme/niveau
- ✅ Copier la commande en 1 clic
- ✅ Ajouter/modifier/supprimer
- ✅ Ajouter aux favoris

### 📜 Certifications
**Route** : `/certifications`

Base des certifications cybersécurité principales.

**Incluses** :
- 🏆 OSCP (Offensive Security)
- 🎓 CEH (EC-Council)
- 🔐 CISSP (ISC2)
- 📚 CompTIA Security+

### 📚 Cheat Sheets
**Route** : `/cheatsheets`

Guides rapides par thème avec commandes clés.

### 📝 Notes
**Route** : `/notes`

Documentation personnelle synchronisée avec la DB.

### 🔧 Outils
**Route** : `/tools`

Base d'outils avec installation et documentation.

### 🔒 Vulnérabilités
**Route** : `/vulnerabilities`

CVE avec sévérité, commandes de test et mitigations.

### 📊 Statistiques
**Route** : `/stats`

Vue d'ensemble : commandes par catégorie, plateforme, etc.

---

## 🔌 API REST

### Endpoints Commandes

#### Lister toutes les commandes
GET /api/commands

text

#### Ajouter une commande
POST /api/commands
Content-Type: application/json

{
"nom": "nmap",
"description": "Scanner de ports",
"categorie": "Reconnaissance",
"plateforme": "Linux",
"arguments_options": "-sV, -sC",
"exemple": "nmap -sV 192.168.1.1",
"usage": "Scanner ports actifs",
"tags": "scan,reconnaissance",
"ressources": "https://nmap.org"
}

text

#### Supprimer une commande
DELETE /api/commands/1

text

### Endpoints Recherche

#### Recherche globale
GET /api/search/global?q=nmap

text

Retourne résultats des 6 modules.

---

## 🗄️ Base de données

### Architecture
- **PostgreSQL 15** pour production
- **SQLite** possible localement
- **Migrations automatiques** au démarrage

### Tables principales
- `commands` - Commandes cybersec
- `certifications` - Certifications
- `cheatsheets` - Guides rapides
- `tools` - Outils
- `vulnerabilities` - CVE
- `notes` - Notes personnelles
- `favorites` - Favoris utilisateur
- `search_history` - Historique recherche

### Accéder à la DB

#### Via PgAdmin (GUI)
1. Ouvre http://localhost:5050
2. Ajoute un serveur :
   - Host: `db`
   - Username: `postgres`
   - Password: `secure_password` (du `.env`)

#### Via terminal
docker-compose exec db psql -U postgres -d cybersec_manager

text

Puis des commandes SQL :
-- Voir les tables
\dt

-- Compter les commandes
SELECT COUNT(*) FROM commands;

-- Lister les commandes
SELECT nom, categorie FROM commands LIMIT 10;

text

---

## 🔧 Configuration

### Fichier `.env`
PostgreSQL
POSTGRES_USER=postgres
POSTGRES_PASSWORD=secure_password
POSTGRES_DB=cybersec_manager

Flask
FLASK_ENV=production
FLASK_DEBUG=0
SECRET_KEY=your-secret-key-change-me

text

### Modifier la configuration
1. Édite `.env`
2. Relance : `docker-compose restart`

---

## 📥 Importer des données

### Format CSV
nom,description,categorie,plateforme,arguments_options,exemple,usage,tags,niveau
nmap,Scanner de ports,Reconnaissance,Linux,-sV -sC -A,nmap -sV 192.168.1.1,Scanner les ports,scan;reconnaissance,Intermédiaire

text

### Import automatique
Les fichiers dans `data/` sont importés automatiquement au démarrage.

---

## 🐛 Troubleshooting

### "Connection refused" PostgreSQL
Vérifier que le container PostgreSQL est actif
docker-compose ps

Relancer
docker-compose restart db

text

### "Port already in use"
Port 5000 occupé
Modifier docker-compose.yml : "5001:5000" au lieu de "5000:5000"
text

### "ModuleNotFoundError"
Réinstaller les dépendances
docker-compose exec web pip install -r requirements.txt

text

### Réinitialiser la base de données
ATTENTION : supprime toutes les données !
docker-compose down -v
docker-compose up --build

text

---

## 🚀 Déploiement Production

### Sur un serveur

#### Option 1 : Docker (recommandé)
Sur le serveur
git clone <ton-repo>
cd cyber-tool2

Modifier .env (sécurité)
nano .env

Lancer
docker-compose -f docker-compose.yml up -d

text

#### Option 2 : Heroku/Railway
1. Push sur GitHub
2. Connecte à Heroku/Railway
3. Ajoute les variables d'environnement
4. Deploy !

### Considérations sécurité
- ✅ Change `SECRET_KEY` en `.env`
- ✅ Change `POSTGRES_PASSWORD`
- ✅ Change `PGADMIN_DEFAULT_PASSWORD`
- ✅ Active HTTPS
- ✅ Restriction d'accès PgAdmin

---

## 📚 Ressources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
- [Docker Compose](https://docs.docker.com/compose/)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [Nmap Book](https://nmap.org/book/)

---

## 🤝 Contribution

Les contributions sont bienvenues ! 

### Process
1. Fork le repository
2. Crée une branche : `git checkout -b feature/ma-feature`
3. Commit : `git commit -m 'Ajout feature'`
4. Push : `git push origin feature/ma-feature`
5. Ouvre une Pull Request

---

## 📝 Licence

Ce projet est sous licence **MIT** - voir [LICENSE](LICENSE) pour plus de détails.

---

## 👨‍💻 À propos

Développé comme référence complète pour apprendre et pratiquer la cybersécurité.

**Idéal pour** :
- Étudiants en cybersécurité
- Candidats certifications (OSCP, CEH, etc.)
- Pentesters cherchant une quick reference
- Équipes de sécurité

---

## 📞 Support

- 📧 Questions ? Ouvre une issue
- 🐛 Bug trouvé ? Signale-le
- 💡 Suggestion ? Pull request bienvenue

---

## 🌟 If you find this useful, please star ⭐

⭐ ← Click here to star the repo

text

---

**Made with ❤️ for the cybersecurity community**

*Dernière mise à jour : November 5, 2025*
