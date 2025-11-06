from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

def safe_json_loads(value, default=None):
    """Parse JSON de façon sécurisée"""
    if not value:
        return default if default is not None else []
    if isinstance(value, (list, dict)):
        return value
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError, ValueError):
        return default if default is not None else []


class Command(db.Model):
    __tablename__ = 'commands'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    categorie = db.Column(db.String(100), nullable=False)
    plateforme = db.Column(db.String(50), nullable=False)
    arguments_options = db.Column(db.Text)
    exemple = db.Column(db.Text)
    usage = db.Column(db.Text)
    tags = db.Column(db.String(200))
    niveau = db.Column(db.String(50), default='Débutant')
    ressources = db.Column(db.Text)
    date_ajout = db.Column(db.DateTime, default=datetime.utcnow)
    date_modification = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'description': self.description,
            'categorie': self.categorie,
            'plateforme': self.plateforme,
            'arguments_options': self.arguments_options or '',
            'exemple': self.exemple or '',
            'usage': self.usage or '',
            'tags': self.tags or '',
            'niveau': self.niveau or 'Débutant',
            'ressources': self.ressources or '',
            'date_ajout': self.date_ajout.isoformat() if self.date_ajout else None
        }


class Certification(db.Model):
    __tablename__ = 'certifications'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(200), nullable=False)
    organisme = db.Column(db.String(200))
    description = db.Column(db.Text)
    niveau = db.Column(db.String(50))
    prix_usd = db.Column(db.Integer)
    duree_validite = db.Column(db.Integer, default=36)
    duree_etude = db.Column(db.String(100))
    domaines = db.Column(db.Text)
    commandes_recommandees = db.Column(db.Text)
    prerequisites = db.Column(db.Text)
    lien = db.Column(db.String(500))
    date_ajout = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'organisme': self.organisme or '',
            'description': self.description or '',
            'niveau': self.niveau or '',
            'prix_usd': self.prix_usd or 0,
            'duree_validite': self.duree_validite or 36,
            'duree_etude': self.duree_etude or '',
            'domaines': safe_json_loads(self.domaines, []),
            'commandes_recommandees': safe_json_loads(self.commandes_recommandees, []),
            'prerequisites': self.prerequisites or '',
            'lien': self.lien or '',
            'date_ajout': self.date_ajout.isoformat() if self.date_ajout else None
        }


class CheatSheet(db.Model):
    __tablename__ = 'cheatsheets'
    
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    categorie = db.Column(db.String(100))
    niveau = db.Column(db.String(50))
    contenu = db.Column(db.Text)
    commandes = db.Column(db.Text)
    ressources = db.Column(db.Text)
    date_ajout = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'titre': self.titre or '',
            'description': self.description or '',
            'categorie': self.categorie or '',
            'niveau': self.niveau or '',
            'contenu': self.contenu or '',
            'commandes': safe_json_loads(self.commandes, []),
            'ressources': self.ressources or '',
            'date_ajout': self.date_ajout.isoformat() if self.date_ajout else None
        }


class Tool(db.Model):
    __tablename__ = 'tools'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    categorie = db.Column(db.String(100))
    type = db.Column(db.String(100))
    installation = db.Column(db.Text)
    documentation = db.Column(db.String(500))
    prix = db.Column(db.String(100), default='Gratuit')
    plateforme = db.Column(db.Text)
    commandes_courantes = db.Column(db.Text)
    alternatives = db.Column(db.Text)
    date_ajout = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom or '',
            'description': self.description or '',
            'categorie': self.categorie or '',
            'type': self.type or '',
            'installation': self.installation or '',
            'documentation': self.documentation or '',
            'prix': self.prix or 'Gratuit',
            'plateforme': safe_json_loads(self.plateforme, []),
            'commandes_courantes': safe_json_loads(self.commandes_courantes, []),
            'alternatives': safe_json_loads(self.alternatives, []),
            'date_ajout': self.date_ajout.isoformat() if self.date_ajout else None
        }


class Vulnerability(db.Model):
    __tablename__ = 'vulnerabilities'
    
    id = db.Column(db.Integer, primary_key=True)
    cve = db.Column(db.String(50), unique=True)
    titre = db.Column(db.String(300))
    description = db.Column(db.Text)
    severite = db.Column(db.String(50))
    score_cvss = db.Column(db.Float)
    mitigation = db.Column(db.Text)
    plateforme = db.Column(db.Text)
    date_decouverte = db.Column(db.String(50))
    date_correction = db.Column(db.String(50))
    commandes_test = db.Column(db.Text)
    ressources = db.Column(db.Text)
    tools = db.Column(db.Text)
    date_ajout = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'cve': self.cve or '',
            'titre': self.titre or '',
            'description': self.description or '',
            'severite': self.severite or '',
            'score_cvss': self.score_cvss or 0.0,
            'mitigation': self.mitigation or '',
            'plateforme': safe_json_loads(self.plateforme, []),
            'date_decouverte': self.date_decouverte or '',
            'date_correction': self.date_correction or '',
            'commandes_test': safe_json_loads(self.commandes_test, []),
            'ressources': self.ressources or '',
            'tools': safe_json_loads(self.tools, []),
            'date_ajout': self.date_ajout.isoformat() if self.date_ajout else None
        }


class Note(db.Model):
    __tablename__ = 'notes'
    
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(300), nullable=False)
    contenu = db.Column(db.Text)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    date_modification = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'titre': self.titre or '',
            'contenu': self.contenu or '',
            'date_creation': self.date_creation.isoformat() if self.date_creation else None,
            'date_modification': self.date_modification.isoformat() if self.date_modification else None
        }


class Favorite(db.Model):
    __tablename__ = 'favorites'
    
    id = db.Column(db.Integer, primary_key=True)
    command_id = db.Column(db.Integer, nullable=False)
    date_ajout = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'command_id': self.command_id,
            'date_ajout': self.date_ajout.isoformat() if self.date_ajout else None
        }


class SearchHistory(db.Model):
    __tablename__ = 'search_history'
    
    id = db.Column(db.Integer, primary_key=True)
    search_term = db.Column(db.String(300))
    type = db.Column(db.String(50))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'search_term': self.search_term or '',
            'type': self.type or '',
            'date': self.date.isoformat() if self.date else None
        }


class Badge(db.Model):
    __tablename__ = 'badges'
    
    id = db.Column(db.Integer, primary_key=True)
    badge_id = db.Column(db.String(100), unique=True)
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    icon = db.Column(db.String(50))
    date_earned = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'badge_id': self.badge_id or '',
            'title': self.title or '',
            'description': self.description or '',
            'icon': self.icon or '',
            'date_earned': self.date_earned.isoformat() if self.date_earned else None
        }
