# 🛡️ CyberSec Command Manager

> Gestionnaire complet et intelligent des commandes cybersécurité avec recherche globale avancée, dashboard personnalisé et gestion multi-modules.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com/)

---

## 📋 Table des matières

- [Fonctionnalités](#-fonctionnalités)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Structure du projet](#-structure-du-projet)
- [Modules disponibles](#-modules-disponibles)
- [API REST](#-api-rest)
- [Configuration](#-configuration)
- [Contribuer](#-contribuer)
- [Licence](#-licence)

---

## ✨ Fonctionnalités

### 🎯 Core Features
- ✅ **Gestionnaire de commandes** - Cataloguez 50+ commandes cybersécurité
- ✅ **Recherche globale avancée** - Cross-module search avec autocomplétion
- ✅ **Dashboard intelligent** - Statistiques, raccourcis, commandes récentes
- ✅ **Favoris personnalisés** - Sauvegardez vos commandes favorites
- ✅ **Historique de recherche** - Tracez vos recherches
- ✅ **Interface responsive** - Fonctionne sur desktop, tablette, mobile

### 📦 Modules
- 📋 **Commandes** - Base de données de 50+ commandes avec doc
- 📜 **Certifications** - OSCP, CEH, CISSP, GPEN avec progress tracking
- 📚 **Cheat Sheets** - Guides rapides (Linux, Windows, Web, etc.)
- 📝 **Notes** - Documentation personnelle synchronisée
- 🔧 **Outils** - Nmap, Metasploit, Burp Suite, etc. avec ressources
- 🔒 **Vulnérabilités** - CVE avec commandes de test et mitigations

### 🚀 Avancé
- 🔍 Recherche temps réel avec suggestions
- 📊 Statistiques détaillées par catégorie/plateforme
- ⭐ Système de badges et réalisations
- 💾 Export/Import données
- 📱 Interface dark mode optimisée
- 🔗 Liens directs vers documentation officielle

---

## 🛠️ Installation

### Prérequis
- Python 3.8+
- pip (Python package manager)
- Git (optionnel)

### Étapes d'installation

#### 1️⃣ Cloner le repository
git clone https://github.com/ton-username/cybersec-command-manager.git
cd cybersec-command-manager

text

#### 2️⃣ Créer un environnement virtuel
Linux/macOS
python3 -m venv venv
source venv/bin/activate

Windows
python -m venv venv
venv\Scripts\activate

text

#### 3️⃣ Installer les dépendances
pip install -r requirements.txt

text

#### 4️⃣ Lancer l'application
python app.py

text

#### 5️⃣ Accéder à l'application
Ouvrez votre navigateur et allez à :
http://localhost:5000

text

---

## 📖 Utilisation

### Démarrage rapide

#### Ajouter une commande
1. Cliquez sur **"📋 Commandes"** dans la navigation
2. Cliquez sur **"➕ Ajouter une commande"**
3. Remplissez les champs :
   - **Nom** : `nmap`
   - **Description** : Scanner de ports
   - **Catégorie** : Reconnaissance
   - **Plateforme** : Linux/Windows
   - **Arguments** : `-sV, -sC, -A`
   - **Exemple** : `nmap -sV 192.168.1.1`
   - **Ressources** : Lien vers la documentation
4. Cliquez **"💾 Ajouter"**

#### Rechercher une commande
1. Utilisez la **barre de recherche globale** en haut
2. Ou filtrez sur la page des commandes :
   - Par **catégorie**
   - Par **plateforme** (Linux/Windows)
   - Par **niveau** (Débutant/Intermédiaire/Avancé)
3. Cliquez sur un **tag** pour rechercher directement

#### Gérer les favoris
1. Cliquez sur l'**étoile ☆** sur une commande
2. Elle devient **⭐** (favori)
3. Filtrez les favoris avec le bouton **"⭐ Favoris"**

#### Copier une commande
1. Cliquez sur le bouton **"📋 Copier"** dans une carte
2. La commande est automatiquement copiée
3. Notification **"✅ Copié!"** confirme l'action

### Navigation principale

| Page | URL | Description |
|------|-----|-------------|
| 🏠 Accueil | `/` | Dashboard avec statistiques |
| 📋 Commandes | `/commandes` | Gestionnaire de commandes |
| 📜 Certifications | `/certifications` | Base certifications (OSCP, CEH, etc.) |
| 📚 Cheat Sheets | `/cheatsheets` | Guides rapides par thème |
| 📝 Notes | `/notes` | Documentation personnelle |
| 🔧 Outils | `/tools` | Base d'outils cybersécurité |
| 🔒 CVE | `/vulnerabilities` | Vulnérabilités avec commandes |
| 📊 Stats | `/stats` | Statistiques détaillées |

---

## 📁 Structure du projet

cybersec-command-manager/
├── app.py # Application Flask principale
├── requirements.txt # Dépendances Python
├── README.md # Ce fichier
│
├── templates/ # Templates Jinja2 (HTML)
│ ├── base.html # Template de base
│ ├── dashboard.html # Dashboard accueil
│ ├── index.html # Gestionnaire de commandes
│ ├── certifications.html # Module certifications
│ ├── cheatsheets.html # Module cheat sheets
│ ├── notes.html # Module notes
│ ├── tools.html # Module outils
│ ├── vulnerabilities.html # Module vulnérabilités
│ ├── stats.html # Statistiques
│ ├── add_command.html # Formulaire ajout commande
│ └── edit_command.html # Formulaire édition commande
│
├── static/ # Fichiers statiques
│ ├── css/
│ │ └── style.css # Styles CSS (2000+ lignes)
│ ├── js/
│ │ └── main.js # Scripts JavaScript
│ └── images/ # Images/icônes
│
├── data/ # Base de données (JSON)
│ ├── commands.json # 50+ commandes
│ ├── certifications.json # 4+ certifications
│ ├── cheatsheets.json # 5+ cheat sheets
│ ├── notes.json # Notes utilisateur
│ ├── tools.json # 5+ outils
│ ├── vulnerabilities.json # 3+ CVE
│ ├── favorites.json # Favoris utilisateur
│ ├── history.json # Historique recherche
│ └── badges.json # Badges réalisations
│
└── docs/ # Documentation
├── API.md # Documentation API REST
├── INSTALLATION.md # Guide installation détaillé
└── CONTRIBUTING.md # Guide contribution

text

---

## 🎯 Modules disponibles

### 📋 Module Commandes
Gère une base de données de commandes cybersécurité.

**Champs** :
- `nom` : Nom de la commande
- `description` : Description courte
- `categorie` : Catégorie (Gestion fichiers, Réseau, etc.)
- `plateforme` : Linux, Windows, Linux/Windows
- `arguments_options` : Options disponibles
- `exemple` : Exemple d'utilisation
- `usage` : Quand l'utiliser
- `tags` : Tags pour recherche
- `niveau` : Débutant/Intermédiaire/Avancé
- `ressources` : Lien documentation officielle

**Exemple** :
{
"nom": "nmap",
"description": "Scanner de ports et découverte réseau",
"categorie": "Reconnaissance",
"plateforme": "Linux/Windows",
"arguments_options": "-sT (TCP), -sS (SYN), -sV (versions)",
"exemple": "nmap -sV 192.168.1.1",
"usage": "Scanner les ports actifs",
"tags": "scan, reconnaissance, pentest",
"niveau": "Intermédiaire",
"ressources": "https://nmap.org/book/man.html"
}

text

### 📜 Module Certifications
Gère les certifications cybersécurité avec suivi de progression.

**Certifications incluses** :
- 🏆 OSCP (Offensive Security Certified Professional)
- 🎓 CEH (Certified Ethical Hacker)
- 🔐 CISSP (Certified Information Systems Security Professional)
- 🔧 GPEN (GIAC Certified Penetration Tester)

### 📚 Module Cheat Sheets
Guides rapides par thème avec commandes clés.

**Cheat Sheets inclus** :
- Linux Privilege Escalation
- Windows Privilege Escalation
- Web Penetration Testing
- Bash Scripting Essentials
- Network Reconnaissance

### 📝 Module Notes
Documentation personnelle avec historique de modification.

### 🔧 Module Outils
Base d'outils avec installation et lien vers documentation.

**Outils inclus** :
- Nmap
- Metasploit
- Burp Suite
- Wireshark
- Volatility

### 🔒 Module Vulnérabilités
CVE avec sévérité, commandes de test et mitigations.

---

## 🔌 API REST

### Endpoints Commandes

#### Lister toutes les commandes
GET /api/commands

text

**Réponse** :
[
{
"nom": "nmap",
"description": "Scanner de ports",
...
}
]

text

#### Ajouter une commande
POST /api/commands
Content-Type: application/json

{
"nom": "nmap",
"description": "Scanner de ports",
"categorie": "Reconnaissance",
"plateforme": "Linux/Windows",
"arguments_options": "-sV, -sC",
"exemple": "nmap -sV 192.168.1.1",
"usage": "Scanner ports actifs",
"tags": "scan,reconnaissance",
"ressources": "https://nmap.org"
}

text

#### Modifier une commande
PUT /api/commands/0
Content-Type: application/json

{
"description": "Nouveau descriptif"
}

text

#### Supprimer une commande
DELETE /api/commands/0

text

### Endpoints Recherche

#### Recherche globale
GET /api/search/global?q=nmap

text

**Réponse** :
{
"commands": [{...}],
"cheatsheets": [{...}],
"tools": [{...}],
"vulnerabilities": [{...}],
"certifications": [{...}],
"notes": [{...}]
}

text

#### Suggestions recherche
GET /api/search/suggestions

text

#### Ajouter à l'historique
POST /api/search/add-history
Content-Type: application/json

{
"search": "nmap",
"type": "global"
}

text

### Endpoints Favoris

#### Lister favoris
GET /api/favorites

text

#### Ajouter aux favoris
POST /api/favorites/0

text

#### Retirer des favoris
DELETE /api/favorites/0

text

---

## ⚙️ Configuration

### Variables d'environnement

Créez un fichier `.env` :

FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=votre-cle-secrete-ici
DEBUG=True
HOST=0.0.0.0
PORT=5000

text

### Configuration Flask

Modifiez `app.py` :

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key')
app.config['DEBUG'] = os.getenv('DEBUG', True)

text

---

## 📊 Importer un gros dataset

### Via CSV

1. Créez un fichier `data/import_commands.py` :

import csv
import json

def import_csv(csv_file, json_file):
data = []
with open(csv_file, 'r', encoding='utf-8') as f:
reader = csv.DictReader(f)
for row in reader:
data.append(row)

text
with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✅ {len(data)} items importés!")
import_csv('commandes.csv', 'data/commands.json')

text

2. Lancez le script :
python data/import_commands.py

text

---

## 🤝 Contribuer

Les contributions sont bienvenues ! 

### Process

1. Fork le repository
2. Créez une branche : `git checkout -b feature/votre-feature`
3. Commitez : `git commit -m 'Ajout feature'`
4. Push : `git push origin feature/votre-feature`
5. Ouvrez une Pull Request

### Guidelines

- Suivez le style de code existant
- Testez vos modifications
- Documentez les nouvelles features
- Mettez à jour le README si nécessaire

---

## 📝 Licence

Ce projet est sous licence **MIT** - voir le fichier [LICENSE](LICENSE) pour les détails.

---

## 🎓 Cas d'usage

- 📚 **Apprentissage cybersécurité** - Référence des commandes avec exemples
- 🎯 **Préparation certifications** - Suivi de progression OSCP, CEH, etc.
- 🔧 **Pentest** - Quick reference pour opérations terrain
- 📖 **Documentation** - Notes personnelles et procédures
- 🏢 **Formation** - Support pour équipes de sécurité

---

## 🐛 Signaler un bug

Créez une issue GitHub avec :
- Description du bug
- Pas pour reproduire
- Résultat attendu vs réel
- Version Python et OS

---

## 💬 Support

- 📧 Email : [contact@example.com]
- 🐙 GitHub Issues : [https://github.com/...](https://github.com/...)
- 💬 Discussions : [GitHub Discussions]

---

## 🚀 Roadmap

- [ ] Migration vers SQLite pour scalabilité
- [ ] Système d'authentification multi-utilisateurs
- [ ] Partage de collections entre utilisateurs
- [ ] API publique avec authentification
- [ ] Application mobile (React Native)
- [ ] Synchronisation cloud
- [ ] Chat intégré pour collaboration
- [ ] Intégration Slack/Discord

---

## 📚 Ressources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [Nmap Book](https://nmap.org/book/)
- [Metasploit Docs](https://docs.rapid7.com/metasploit/)

---

## 👨‍💻 Auteur

**Maxime Pélissier**
- 📍 Grenoble, France
- 🎓 Master Cybersécurité
- 🔐 Passionné par la sécurité

---

## ⭐ Si tu aimes ce projet, n'oublie pas la star !

⭐ ← Clique ici pour star le repo

text

---

**Made with ❤️ for the cybersecurity community**

*Dernière mise à jour : November 5, 2025*
