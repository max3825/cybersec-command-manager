from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()


# ============ COMMAND MODEL ============
class Command(db.Model):
    __tablename__ = 'commands'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), unique=True, nullable=False, index=True)
    description = db.Column(db.String(500), nullable=False)
    categorie = db.Column(db.String(100), nullable=False, index=True)
    plateforme = db.Column(db.String(100), nullable=False, index=True)
    arguments_options = db.Column(db.Text, nullable=False)
    exemple = db.Column(db.Text, nullable=False)
    usage = db.Column(db.Text, nullable=False)
    tags = db.Column(db.String(500), nullable=False)
    niveau = db.Column(db.String(50), default='Débutant', index=True)
    ressources = db.Column(db.String(500))
    date_ajout = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    date_modification = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    favorites = db.relationship('Favorite', backref='command', lazy=True, cascade='all, delete-orphan')
    search_history = db.relationship('SearchHistory', backref='command', lazy=True)

    def __repr__(self):
        return f'<Command {self.nom}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'description': self.description,
            'categorie': self.categorie,
            'plateforme': self.plateforme,
            'arguments_options': self.arguments_options,
            'exemple': self.exemple,
            'usage': self.usage,
            'tags': self.tags,
            'niveau': self.niveau,
            'ressources': self.ressources,
            'date_ajout': self.date_ajout.isoformat() if self.date_ajout else None,
            'date_modification': self.date_modification.isoformat() if self.date_modification else None
        }


# ============ CERTIFICATION MODEL ============
class Certification(db.Model):
    __tablename__ = 'certifications'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), unique=True, nullable=False, index=True)
    organisme = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    niveau = db.Column(db.String(50), nullable=False, index=True)
    prix_usd = db.Column(db.Integer, nullable=False)
    duree_validite = db.Column(db.Integer, default=36)
    duree_etude = db.Column(db.String(100))
    domaines = db.Column(db.Text)  # JSON string
    commandes_recommandees = db.Column(db.Text)  # JSON string
    prerequisites = db.Column(db.String(500))
    lien = db.Column(db.String(500))
    date_ajout = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Certification {self.nom}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'organisme': self.organisme,
            'description': self.description,
            'niveau': self.niveau,
            'prix_usd': self.prix_usd,
            'duree_validite': self.duree_validite,
            'duree_etude': self.duree_etude,
            'domaines': json.loads(self.domaines) if self.domaines else [],
            'commandes_recommandees': json.loads(self.commandes_recommandees) if self.commandes_recommandees else [],
            'prerequisites': self.prerequisites,
            'lien': self.lien,
            'date_ajout': self.date_ajout.isoformat() if self.date_ajout else None
        }


# ============ CHEATSHEET MODEL ============
class CheatSheet(db.Model):
    __tablename__ = 'cheatsheets'

    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), unique=True, nullable=False, index=True)
    description = db.Column(db.String(500), nullable=False)
    categorie = db.Column(db.String(100), nullable=False, index=True)
    niveau = db.Column(db.String(50), nullable=False, index=True)
    contenu = db.Column(db.Text, nullable=False)
    commandes = db.Column(db.Text)  # JSON string list
    ressources = db.Column(db.Text)
    date_ajout = db.Column(db.DateTime, default=datetime.utcnow)
    date_modification = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<CheatSheet {self.titre}>'

    def to_dict(self):
        return {
            'id': self.id,
            'titre': self.titre,
            'description': self.description,
            'categorie': self.categorie,
            'niveau': self.niveau,
            'contenu': self.contenu,
            'commandes': json.loads(self.commandes) if self.commandes else [],
            'ressources': json.loads(self.ressources) if self.ressources else [],
            'date_ajout': self.date_ajout.isoformat() if self.date_ajout else None,
            'date_modification': self.date_modification.isoformat() if self.date_modification else None
        }


# ============ TOOL MODEL ============
class Tool(db.Model):
    __tablename__ = 'tools'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), unique=True, nullable=False, index=True)
    description = db.Column(db.String(500), nullable=False)
    categorie = db.Column(db.String(100), nullable=False, index=True)
    type = db.Column(db.String(100), nullable=False)
    installation = db.Column(db.String(500), nullable=False)
    documentation = db.Column(db.String(500), nullable=False)
    prix = db.Column(db.String(50), default='Gratuit', index=True)
    plateforme = db.Column(db.Text)  # JSON string list
    commandes_courantes = db.Column(db.Text)  # JSON string list
    alternatives = db.Column(db.Text)  # JSON string list
    date_ajout = db.Column(db.DateTime, default=datetime.utcnow)
    date_modification = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Tool {self.nom}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'description': self.description,
            'categorie': self.categorie,
            'type': self.type,
            'installation': self.installation,
            'documentation': self.documentation,
            'prix': self.prix,
            'plateforme': json.loads(self.plateforme) if self.plateforme else [],
            'commandes_courantes': json.loads(self.commandes_courantes) if self.commandes_courantes else [],
            'alternatives': json.loads(self.alternatives) if self.alternatives else [],
            'date_ajout': self.date_ajout.isoformat() if self.date_ajout else None,
            'date_modification': self.date_modification.isoformat() if self.date_modification else None
        }


# ============ VULNERABILITY MODEL ============
class Vulnerability(db.Model):
    __tablename__ = 'vulnerabilities'

    id = db.Column(db.Integer, primary_key=True)
    cve = db.Column(db.String(50), unique=True, nullable=False, index=True)
    titre = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    severite = db.Column(db.String(50), nullable=False, index=True)
    score_cvss = db.Column(db.Float, nullable=False)
    mitigation = db.Column(db.Text, nullable=False)
    plateforme = db.Column(db.Text)  # JSON string list
    date_decouverte = db.Column(db.String(50))
    date_correction = db.Column(db.String(50))
    commandes_test = db.Column(db.Text)  # JSON string list
    ressources = db.Column(db.Text)
    tools = db.Column(db.Text)  # JSON string list
    date_ajout = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Vulnerability {self.cve}>'

    def to_dict(self):
        return {
            'id': self.id,
            'cve': self.cve,
            'titre': self.titre,
            'description': self.description,
            'severite': self.severite,
            'score_cvss': self.score_cvss,
            'mitigation': self.mitigation,
            'plateforme': json.loads(self.plateforme) if self.plateforme else [],
            'date_decouverte': self.date_decouverte,
            'date_correction': self.date_correction,
            'commandes_test': json.loads(self.commandes_test) if self.commandes_test else [],
            'ressources': self.ressources,
            'tools': json.loads(self.tools) if self.tools else [],
            'date_ajout': self.date_ajout.isoformat() if self.date_ajout else None
        }


# ============ NOTE MODEL ============
class Note(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200), nullable=False, index=True)
    contenu = db.Column(db.Text, nullable=False)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    date_modification = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Note {self.titre}>'

    def to_dict(self):
        return {
            'id': self.id,
            'titre': self.titre,
            'contenu': self.contenu,
            'date_creation': self.date_creation.isoformat() if self.date_creation else None,
            'date_modification': self.date_modification.isoformat() if self.date_modification else None
        }


# ============ FAVORITE MODEL ============
class Favorite(db.Model):
    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True)
    command_id = db.Column(db.Integer, db.ForeignKey('commands.id', ondelete='CASCADE'), nullable=False, index=True)
    date_ajout = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Favorite command_id={self.command_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'command_id': self.command_id,
            'date_ajout': self.date_ajout.isoformat() if self.date_ajout else None
        }


# ============ SEARCH HISTORY MODEL ============
class SearchHistory(db.Model):
    __tablename__ = 'search_history'

    id = db.Column(db.Integer, primary_key=True)
    search_term = db.Column(db.String(200), nullable=False, index=True)
    type = db.Column(db.String(50), default='general', index=True)
    command_id = db.Column(db.Integer, db.ForeignKey('commands.id', ondelete='SET NULL'), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def __repr__(self):
        return f'<SearchHistory {self.search_term}>'

    def to_dict(self):
        return {
            'id': self.id,
            'search_term': self.search_term,
            'type': self.type,
            'command_id': self.command_id,
            'date': self.date.isoformat() if self.date else None
        }


# ============ BADGE MODEL ============
class Badge(db.Model):
    __tablename__ = 'badges'

    id = db.Column(db.Integer, primary_key=True)
    badge_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    icon = db.Column(db.String(50))  # emoji ou URL
    date_earned = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Badge {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'badge_id': self.badge_id,
            'title': self.title,
            'description': self.description,
            'icon': self.icon,
            'date_earned': self.date_earned.isoformat() if self.date_earned else None
        }


# ============ STATS MODEL ============
class UserStats(db.Model):
    __tablename__ = 'user_stats'

    id = db.Column(db.Integer, primary_key=True)
    total_searches = db.Column(db.Integer, default=0)
    total_commands_viewed = db.Column(db.Integer, default=0)
    total_commands_copied = db.Column(db.Integer, default=0)
    favorite_commands_count = db.Column(db.Integer, default=0)
    notes_created = db.Column(db.Integer, default=0)
    last_visited = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<UserStats>'

    def to_dict(self):
        return {
            'id': self.id,
            'total_searches': self.total_searches,
            'total_commands_viewed': self.total_commands_viewed,
            'total_commands_copied': self.total_commands_copied,
            'favorite_commands_count': self.favorite_commands_count,
            'notes_created': self.notes_created,
            'last_visited': self.last_visited.isoformat() if self.last_visited else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
