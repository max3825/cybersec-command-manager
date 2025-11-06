# 🔐 Cybersec Command Manager

Une application web complète pour gérer les commandes de cybersécurité, certifications, cheat sheets, outils, vulnérabilités et notes.

## 🚀 Stack Technique

- **Backend** : Flask + SQLAlchemy + PostgreSQL
- **Frontend** : HTML5 + CSS3 + Vanilla JavaScript
- **Déploiement** : Docker + Docker Compose
- **Admin DB** : pgAdmin 4

## 📋 Fonctionnalités

✅ **Commandes** - Recherche avancée, filtrage, favoris, édition
✅ **Certifications** - Filtrage par niveau, prix, domaines
✅ **Cheat Sheets** - Affichage, export, édition Markdown
✅ **Outils** - Gestion des outils de pentest avec alternatives
✅ **Vulnérabilités CVE** - Score CVSS, mitigation, commandes de test
✅ **Notes** - Prise de notes personnalisées
✅ **Favoris** - Marquer les commandes préférées
✅ **Interface dark/light** - Thème personnalisable

## 🛠️ Installation & Démarrage

### Prérequis
- Docker & Docker Compose installés

### Démarrer l'application

```bash
# Cloner le repo
git clone <repo>
cd cybersec-command-manager

# Lancer l'application
docker compose up -d

# L'app est accessible sur http://localhost:5000
```

### Services accessibles

- **App** : http://localhost:5000
- **pgAdmin** : http://localhost:5050 (admin@example.com / admin)
- **PostgreSQL** : localhost:5432

## 📂 Structure du projet

```
cybersec-command-manager/
├── app/
│   ├── app.py                 # Routes Flask principales
│   ├── models.py              # Modèles SQLAlchemy
│   ├── migrate_json_to_db.py  # Import données JSON
│   ├── requirements.txt        # Dépendances Python
│   ├── data/                  # Fichiers JSON (données)
│   └── templates/             # Pages HTML
│       ├── base.html
│       ├── index.html
│       ├── certifications.html
│       ├── cheatsheets.html
│       ├── tools.html
│       ├── vulnerabilities.html
│       ├── edit_command.html
│       ├── edit_certification.html
│       ├── edit_cheatsheet.html
│       ├── edit_tool.html
│       └── edit_vulnerability.html
│   └── static/
│       ├── css/style.css
│       └── js/main.js
├── docker-compose.yml
├── Dockerfile
└── README.md
```

## 🔧 Configuration

### Variables d'environnement (`docker-compose.yml`)

```yaml
DATABASE_URL: postgresql://postgres:secure_password@db:5432/cybersec_manager
FLASK_ENV: production
SECRET_KEY: your-secret-key-change-me
```

### Importer les données JSON

Les données JSON sont automatiquement importées au démarrage. Pour réimporter :

```bash
docker compose exec web python migrate_json_to_db.py
```

## 📖 Utilisation

### Pages principales

| Page | URL | Fonction |
|------|-----|----------|
| Commandes | `/commandes` | Liste, search, filtrage, favoris |
| Certifications | `/certifications` | Détails, prix, domaines |
| Cheat Sheets | `/cheatsheets` | Affichage, export, édition |
| Outils | `/tools` | Catégories, prix, alternatives |
| Vulnérabilités | `/vulnerabilities` | CVE, CVSS, mitigation |

### Fonctionnalités clés

**Recherche & Filtrage**
- Recherche par texte en temps réel
- Filtrage par catégorie, niveau, prix
- Filtres multiples combinables

**Édition & CRUD**
- ✏️ Éditer tous les éléments
- 🗑️ Supprimer
- ➕ Ajouter nouveaux éléments

**Favoris**
- ⭐ Marquer comme favori
- 🔍 Vue favoris uniquement
- 📊 Statistiques

**Export & Partage**
- 📥 Exporter cheat sheets en TXT
- 📋 Copier commandes au clipboard
- 📖 Liens vers documentation externe

## 🛠️ API Endpoints

### Commandes
- `GET /api/commands` - Lister
- `POST /api/commands` - Créer
- `PUT /api/commands/<id>` - Modifier
- `DELETE /api/commands/<id>` - Supprimer

### Certifications
- `GET /api/certifications` - Lister
- `POST /api/certifications` - Créer
- `PUT /api/certifications/<id>` - Modifier
- `DELETE /api/certifications/<id>` - Supprimer

*Et similaire pour: Cheat Sheets, Tools, Vulnerabilities*

### Favoris
- `POST /api/favorites/<cmd_id>` - Ajouter aux favoris
- `DELETE /api/favorites/<cmd_id>` - Retirer des favoris

## 📊 Base de données

**Tables principales**
- `commands` - 97+ commandes Linux/Windows
- `certifications` - Certifications cybersec (OSCP, CEH, CISSP, etc.)
- `cheatsheets` - Guides rapides par catégorie
- `tools` - Outils de pentest et security
- `vulnerabilities` - CVE avec scores CVSS
- `notes` - Notes personnalisées
- `favorites` - Favoris utilisateur
- `badges` - Gamification

## 🚨 Dépannage

**L'app ne démarre pas**
```bash
# Vérifier les logs
docker compose logs web

# Rebuilder
docker compose down -v
docker compose up --build
```

**Base de données vide**
```bash
# Réimporter les données
docker compose exec web python migrate_json_to_db.py
```

**Erreur 404**
- Vérifier que la route existe dans `app.py`
- Redémarrer l'app : `docker compose restart web`

**Problème de port**
```bash
# Changer le port dans docker-compose.yml
ports:
  - "5001:5000"  # Utiliser 5001 au lieu de 5000
```

## 🔐 Sécurité

⚠️ **Production**
- Changer `SECRET_KEY` dans `docker-compose.yml`
- Utiliser `FLASK_ENV=production`
- Utiliser un serveur WSGI (Gunicorn)
- HTTPS/SSL activé

## 📝 Modèles de données

```python
Command
├── nom (unique)
├── description
├── categorie
├── plateforme
├── arguments_options
├── exemple
├── usage
├── tags
├── niveau
└── ressources

Certification
├── nom
├── organisme
├── description
├── niveau
├── prix_usd
├── duree_validite
├── duree_etude
├── domaines (JSON)
├── commandes_recommandees (JSON)
└── prerequisites

CheatSheet
├── titre
├── description
├── categorie
├── niveau
├── contenu (Markdown)
├── commandes (JSON)
└── ressources

Tool
├── nom
├── description
├── categorie
├── type
├── installation
├── documentation
├── prix
├── plateforme (JSON)
├── commandes_courantes (JSON)
└── alternatives (JSON)

Vulnerability
├── cve
├── titre
├── description
├── severite
├── score_cvss
├── mitigation
├── plateforme (JSON)
├── date_decouverte
├── date_correction
├── commandes_test (JSON)
├── ressources
└── tools (JSON)
```

## 📞 Support

Pour toute question ou bug report, consultez la documentation du projet.

---

**Version** : 1.0.0
**Dernière mise à jour** : Novembre 2025