from flask import Flask, render_template, request, jsonify, redirect, url_for
from models import db, Command, Certification, CheatSheet, Tool, Vulnerability, Note, Favorite, SearchHistory, Badge
from datetime import datetime
from dotenv import load_dotenv
import os
import sys

# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__)

# ============ CONFIGURATION ============
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL', 
    'postgresql://postgres:password@localhost:5432/cybersec_manager'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-CHANGE-ME')
app.config['SQLALCHEMY_ECHO'] = os.getenv('FLASK_DEBUG', '0') == '1'
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,  # Vérifier les connexions avant utilisation
    'pool_recycle': 300,    # Recycler les connexions après 5min
}

# Configuration Flask
app.config['ENV'] = os.getenv('FLASK_ENV', 'production')
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', '0') == '1'
app.config['JSON_AS_ASCII'] = False  # Support UTF-8 dans JSON

# Initialiser la DB
db.init_app(app)

# ============ INITIALISATION BASE DE DONNÉES ============
with app.app_context():
    try:
        # Test de connexion
        connection = db.engine.connect()
        connection.close()
        print("✅ Connexion PostgreSQL réussie")
        
        # Afficher l'URI (sans le mot de passe)
        db_uri = app.config['SQLALCHEMY_DATABASE_URI']
        safe_uri = db_uri.split('@')[1] if '@' in db_uri else db_uri
        print(f"📍 Database: {safe_uri}")
        
        # Créer toutes les tables
        db.create_all()
        print("✅ Tables de base de données initialisées")
        
        # Statistiques au démarrage
        try:
            stats = {
                'Commandes': Command.query.count(),
                'Outils': Tool.query.count(),
                'CVE': Vulnerability.query.count(),
                'Certifications': Certification.query.count(),
                'Cheat Sheets': CheatSheet.query.count(),
                'Notes': Note.query.count(),
                'Favoris': Favorite.query.count()
            }
            
            print("📊 Statistiques au démarrage:")
            for key, value in stats.items():
                print(f"  - {key}: {value}")
                
        except Exception as e:
            print(f"⚠️  Impossible de récupérer les stats: {e}")
        
    except Exception as e:
        print(f"❌ Erreur critique de connexion à la base de données:")
        print(f"   {str(e)}")
        print(f"   URI: {app.config['SQLALCHEMY_DATABASE_URI'].split('@')[0]}@...")
        print("\n💡 Vérifiez:")
        print("   1. PostgreSQL est démarré")
        print("   2. Les credentials dans .env sont corrects")
        print("   3. La base de données existe")
        sys.exit(1)


# ============ ROUTE DASHBOARD ============
@app.route('/')
def dashboard():
    try:
        # Stats
        stats = {
            'total_commands': Command.query.count(),
            'total_certifications': Certification.query.count(),
            'total_cheatsheets': CheatSheet.query.count(),
            'total_tools': Tool.query.count(),
            'total_vulnerabilities': Vulnerability.query.count(),
            'total_favorites': Favorite.query.count()
        }
        
        # Commandes récentes (5 dernières)
        recent_commands = Command.query.order_by(Command.date_ajout.desc()).limit(5).all()
        recent_commands_data = [cmd.to_dict() for cmd in recent_commands]
        
        # Certifications (3 premières)
        certifications = Certification.query.limit(3).all()
        certifications_data = [cert.to_dict() for cert in certifications]
        
        # Badges (fictif pour l'instant)
        badges = [
            {'title': '🏆 Premier pas', 'icon': '🏆'},
            {'title': '⭐ 10 commandes', 'icon': '⭐'},
            {'title': '🎯 Expert', 'icon': '🎯'}
        ]
        
        # Catégories breakdown
        categories = {}
        commands = Command.query.all()
        for cmd in commands:
            cat = cmd.categorie
            categories[cat] = categories.get(cat, 0) + 1
        
        return render_template('dashboard.html',
                             stats=stats,
                             recent_commands=recent_commands_data,
                             certifications=certifications_data,
                             badges=badges,
                             categories=categories)
    except Exception as e:
        print(f"❌ Erreur dashboard: {e}")
        return f"Erreur: {str(e)}", 500


# ============ ROUTES COMMANDES ============
@app.route('/commandes')
def index():
    try:
        commands = Command.query.all()
        commands_dict = [cmd.to_dict() for cmd in commands]
        
        categories = sorted({cmd.categorie for cmd in commands})
        platforms = sorted({cmd.plateforme for cmd in commands})
        favorites = [f.command_id for f in Favorite.query.all()]

        stats = {
            'total': len(commands),
            'linux': sum(1 for cmd in commands if 'Linux' in cmd.plateforme),
            'windows': sum(1 for cmd in commands if 'Windows' in cmd.plateforme),
            'categories': len(categories)
        }

        return render_template('index.html',
                               commands=commands_dict,
                               categories=categories,
                               platforms=platforms,
                               favorites=favorites,
                               stats=stats)
    except Exception as e:
        print(f"❌ Erreur index: {e}")
        return f"Erreur: {str(e)}", 500


@app.route('/api/commands', methods=['GET'])
def get_commands():
    try:
        commands = Command.query.all()
        return jsonify([cmd.to_dict() for cmd in commands])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/commands', methods=['POST'])
def add_command():
    try:
        data = request.get_json()
        required_fields = ['nom', 'description', 'categorie', 'plateforme', 
                          'arguments_options', 'exemple', 'usage', 'tags']

        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Champ manquant: {field}'}), 400

        cmd = Command(
            nom=data['nom'],
            description=data['description'],
            categorie=data['categorie'],
            plateforme=data['plateforme'],
            arguments_options=data['arguments_options'],
            exemple=data['exemple'],
            usage=data['usage'],
            tags=data['tags'],
            niveau=data.get('niveau', 'Débutant'),
            ressources=data.get('ressources', '')
        )
        db.session.add(cmd)
        db.session.commit()
        return jsonify({'message': 'Commande ajoutée', 'id': cmd.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/commands/<int:cmd_id>', methods=['PUT'])
def update_command(cmd_id):
    try:
        cmd = Command.query.get_or_404(cmd_id)
        data = request.get_json()
        
        for key, value in data.items():
            if hasattr(cmd, key):
                setattr(cmd, key, value)
        
        cmd.date_modification = datetime.utcnow()
        db.session.commit()
        return jsonify({'message': 'Mise à jour réussie'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/commands/<int:cmd_id>', methods=['DELETE'])
def delete_command(cmd_id):
    try:
        cmd = Command.query.get_or_404(cmd_id)
        db.session.delete(cmd)
        db.session.commit()
        return jsonify({'message': 'Suppression réussie'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ============ ROUTES CERTIFICATIONS ============
@app.route('/certifications')
def certifications():
    try:
        certs = Certification.query.all()
        certs_data = [cert.to_dict() for cert in certs]
        return render_template('certifications.html', certifications=certs_data)
    except Exception as e:
        return f"Erreur: {str(e)}", 500


@app.route('/certifications/<int:cert_id>', methods=['GET'])
def edit_certification_form(cert_id):
    cert = Certification.query.get_or_404(cert_id)
    return render_template('edit_certification.html', 
                          certification=cert.to_dict(), 
                          cert_id=cert_id)


@app.route('/api/certifications/<int:cert_id>', methods=['PUT'])
def update_certification(cert_id):
    try:
        cert = Certification.query.get_or_404(cert_id)
        data = request.get_json()
        
        for key, value in data.items():
            if hasattr(cert, key):
                setattr(cert, key, value)
        
        db.session.commit()
        return jsonify({'message': 'Certification mise à jour'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/certifications', methods=['GET'])
def get_certifications():
    certs = Certification.query.all()
    return jsonify([cert.to_dict() for cert in certs])


@app.route('/api/certifications', methods=['POST'])
def add_certification():
    try:
        data = request.get_json()
        cert = Certification(**data)
        db.session.add(cert)
        db.session.commit()
        return jsonify({'message': 'Certification ajoutée', 'id': cert.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/certifications/<int:cert_id>', methods=['DELETE'])
def delete_certification(cert_id):
    try:
        cert = Certification.query.get_or_404(cert_id)
        db.session.delete(cert)
        db.session.commit()
        return jsonify({'message': 'Certification supprimée'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ============ ROUTES CHEAT SHEETS ============
@app.route('/cheatsheets')
def cheatsheets():
    sheets = CheatSheet.query.all()
    sheets_data = [sheet.to_dict() for sheet in sheets]
    return render_template('cheatsheets.html', cheatsheets=sheets_data)


@app.route('/cheatsheets/<int:sheet_id>', methods=['GET'])
def edit_cheatsheet_form(sheet_id):
    sheet = CheatSheet.query.get_or_404(sheet_id)
    return render_template('edit_cheatsheet.html', 
                          cheatsheet=sheet.to_dict(), 
                          sheet_id=sheet_id)


@app.route('/api/cheatsheets/<int:sheet_id>', methods=['PUT'])
def update_cheatsheet(sheet_id):
    try:
        sheet = CheatSheet.query.get_or_404(sheet_id)
        data = request.get_json()
        
        for key, value in data.items():
            if hasattr(sheet, key):
                setattr(sheet, key, value)
        
        db.session.commit()
        return jsonify({'message': 'Cheat sheet mis à jour'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/cheatsheets', methods=['GET'])
def get_cheatsheets():
    sheets = CheatSheet.query.all()
    return jsonify([sheet.to_dict() for sheet in sheets])


@app.route('/api/cheatsheets', methods=['POST'])
def add_cheatsheet():
    try:
        data = request.get_json()
        sheet = CheatSheet(**data)
        db.session.add(sheet)
        db.session.commit()
        return jsonify({'message': 'Cheat sheet ajoutée', 'id': sheet.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/cheatsheets/<int:sheet_id>', methods=['DELETE'])
def delete_cheatsheet(sheet_id):
    try:
        sheet = CheatSheet.query.get_or_404(sheet_id)
        db.session.delete(sheet)
        db.session.commit()
        return jsonify({'message': 'Cheat sheet supprimée'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ============ ROUTES NOTES/DOCUMENTATION ============
@app.route('/notes')
def notes():
    notes_list = Note.query.all()
    notes_data = [note.to_dict() for note in notes_list]
    return render_template('notes.html', notes=notes_data)


@app.route('/api/notes', methods=['GET'])
def get_notes():
    notes_list = Note.query.all()
    return jsonify([note.to_dict() for note in notes_list])


@app.route('/api/notes', methods=['POST'])
def add_note():
    try:
        data = request.get_json()
        note = Note(**data)
        db.session.add(note)
        db.session.commit()
        return jsonify({'message': 'Note créée', 'id': note.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    try:
        note = Note.query.get_or_404(note_id)
        data = request.get_json()
        
        for key, value in data.items():
            if hasattr(note, key):
                setattr(note, key, value)
        
        note.date_modification = datetime.utcnow()
        db.session.commit()
        return jsonify({'message': 'Note mise à jour'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    try:
        note = Note.query.get_or_404(note_id)
        db.session.delete(note)
        db.session.commit()
        return jsonify({'message': 'Note supprimée'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ============ ROUTES OUTILS ============
@app.route('/tools')
def tools():
    tools_list = Tool.query.all()
    tools_data = [tool.to_dict() for tool in tools_list]
    return render_template('tools.html', tools=tools_data)


@app.route('/tools/<int:tool_id>', methods=['GET'])
def edit_tool_form(tool_id):
    tool = Tool.query.get_or_404(tool_id)
    return render_template('edit_tool.html', tool=tool.to_dict(), tool_id=tool_id)


@app.route('/api/tools/<int:tool_id>', methods=['PUT'])
def update_tool(tool_id):
    try:
        tool = Tool.query.get_or_404(tool_id)
        data = request.get_json()
        
        for key, value in data.items():
            if hasattr(tool, key):
                setattr(tool, key, value)
        
        db.session.commit()
        return jsonify({'message': 'Outil mis à jour'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/tools', methods=['GET'])
def get_tools():
    tools_list = Tool.query.all()
    return jsonify([tool.to_dict() for tool in tools_list])


@app.route('/api/tools', methods=['POST'])
def add_tool():
    try:
        data = request.get_json()
        tool = Tool(**data)
        db.session.add(tool)
        db.session.commit()
        return jsonify({'message': 'Outil ajouté', 'id': tool.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/tools/<int:tool_id>', methods=['DELETE'])
def delete_tool(tool_id):
    try:
        tool = Tool.query.get_or_404(tool_id)
        db.session.delete(tool)
        db.session.commit()
        return jsonify({'message': 'Outil supprimé'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ============ ROUTES VULNÉRABILITÉS ============
@app.route('/vulnerabilities')
def vulnerabilities():
    vulns = Vulnerability.query.all()
    vulns_data = [vuln.to_dict() for vuln in vulns]
    return render_template('vulnerabilities.html', vulnerabilities=vulns_data)


@app.route('/vulnerabilities/<int:vuln_id>', methods=['GET'])
def edit_vulnerability_form(vuln_id):
    vuln = Vulnerability.query.get_or_404(vuln_id)
    return render_template('edit_vulnerability.html', 
                          vulnerability=vuln.to_dict(), 
                          vuln_id=vuln_id)


@app.route('/api/vulnerabilities/<int:vuln_id>', methods=['PUT'])
def update_vulnerability(vuln_id):
    try:
        vuln = Vulnerability.query.get_or_404(vuln_id)
        data = request.get_json()
        
        for key, value in data.items():
            if hasattr(vuln, key):
                setattr(vuln, key, value)
        
        vuln.date_ajout = datetime.utcnow()
        db.session.commit()
        return jsonify({'message': 'Vulnérabilité mise à jour'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/vulnerabilities', methods=['GET'])
def get_vulnerabilities():
    vulns = Vulnerability.query.all()
    return jsonify([vuln.to_dict() for vuln in vulns])


@app.route('/api/vulnerabilities', methods=['POST'])
def add_vulnerability():
    try:
        data = request.get_json()
        vuln = Vulnerability(**data)
        db.session.add(vuln)
        db.session.commit()
        return jsonify({'message': 'Vulnérabilité ajoutée', 'id': vuln.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/vulnerabilities/<int:vuln_id>', methods=['DELETE'])
def delete_vulnerability(vuln_id):
    try:
        vuln = Vulnerability.query.get_or_404(vuln_id)
        db.session.delete(vuln)
        db.session.commit()
        return jsonify({'message': 'Vulnérabilité supprimée'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ============ ROUTES RECHERCHE GLOBALE ============
@app.route('/api/search', methods=['GET'])
def global_search():
    """Recherche globale dans tous les modules"""
    query = request.args.get('q', '').lower().strip()
    
    if len(query) < 2:
        return jsonify({})
    
    results = {
        'commands': [],
        'vulnerabilities': [],
        'tools': [],
        'certifications': [],
        'cheatsheets': []
    }
    
    try:
        # Recherche dans les commandes
        commands = Command.query.filter(
            db.or_(
                Command.nom.ilike(f'%{query}%'),
                Command.description.ilike(f'%{query}%'),
                Command.tags.ilike(f'%{query}%')
            )
        ).limit(5).all()
        results['commands'] = [cmd.to_dict() for cmd in commands]
        
        # Recherche dans les vulnérabilités
        vulns = Vulnerability.query.filter(
            db.or_(
                Vulnerability.cve.ilike(f'%{query}%'),
                Vulnerability.titre.ilike(f'%{query}%'),
                Vulnerability.description.ilike(f'%{query}%')
            )
        ).limit(5).all()
        results['vulnerabilities'] = [vuln.to_dict() for vuln in vulns]
        
        # Recherche dans les outils
        tools = Tool.query.filter(
            db.or_(
                Tool.nom.ilike(f'%{query}%'),
                Tool.description.ilike(f'%{query}%'),
                Tool.categorie.ilike(f'%{query}%')
            )
        ).limit(5).all()
        results['tools'] = [tool.to_dict() for tool in tools]
        
        # Recherche dans les certifications
        certs = Certification.query.filter(
            db.or_(
                Certification.nom.ilike(f'%{query}%'),
                Certification.description.ilike(f'%{query}%'),
                Certification.organisme.ilike(f'%{query}%')
            )
        ).limit(5).all()
        results['certifications'] = [cert.to_dict() for cert in certs]
        
        # Recherche dans les cheat sheets
        sheets = CheatSheet.query.filter(
            db.or_(
                CheatSheet.titre.ilike(f'%{query}%'),
                CheatSheet.description.ilike(f'%{query}%'),
                CheatSheet.categorie.ilike(f'%{query}%')
            )
        ).limit(5).all()
        results['cheatsheets'] = [sheet.to_dict() for sheet in sheets]
        
    except Exception as e:
        print(f"❌ Erreur recherche: {e}")
        import traceback
        traceback.print_exc()
    
    return jsonify(results)


@app.route('/api/search/suggestions', methods=['GET'])
def search_suggestions():
    """Suggestions basées sur l'historique"""
    try:
        history = SearchHistory.query.order_by(
            SearchHistory.date.desc()
        ).limit(20).all()
        
        suggestions = []
        seen = set()
        
        for entry in history:
            search_term = entry.search_term
            if search_term and search_term not in seen:
                suggestions.append(search_term)
                seen.add(search_term)
        
        return jsonify(suggestions[:10])
    except Exception as e:
        return jsonify([]), 500


@app.route('/api/search/add-history', methods=['POST'])
def add_search_history():
    """Ajouter une recherche à l'historique"""
    try:
        data = request.get_json()
        hist = SearchHistory(
            search_term=data.get('search'),
            type=data.get('type', 'general')
        )
        db.session.add(hist)
        db.session.commit()
        return jsonify({'message': 'Ajouté à l\'historique'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ============ ROUTES HISTORIQUE ============
@app.route('/api/history', methods=['GET'])
def get_history():
    history = SearchHistory.query.order_by(SearchHistory.date.desc()).all()
    return jsonify([h.to_dict() for h in history])


# ============ ROUTES FAVORIS ============
@app.route('/api/favorites', methods=['GET'])
def get_favorites():
    favorites = Favorite.query.all()
    return jsonify([fav.to_dict() for fav in favorites])


@app.route('/api/favorites', methods=['POST'])
def add_favorite():
    try:
        data = request.get_json()
        command_id = data.get('command_id')
        
        existing = Favorite.query.filter_by(command_id=command_id).first()
        if existing:
            return jsonify({'message': 'Déjà en favoris'}), 200
        
        fav = Favorite(command_id=command_id)
        db.session.add(fav)
        db.session.commit()
        return jsonify({'message': 'Ajouté aux favoris'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/favorites/<int:cmd_id>', methods=['POST'])
def favorite_command(cmd_id):
    try:
        existing = Favorite.query.filter_by(command_id=cmd_id).first()
        if existing:
            return jsonify({'message': 'Déjà en favoris'}), 200
        
        fav = Favorite(command_id=cmd_id)
        db.session.add(fav)
        db.session.commit()
        return jsonify({'message': 'Ajouté aux favoris'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/favorites/<int:cmd_id>', methods=['DELETE'])
def unfavorite_command(cmd_id):
    try:
        fav = Favorite.query.filter_by(command_id=cmd_id).first()
        if fav:
            db.session.delete(fav)
            db.session.commit()
        return jsonify({'message': 'Retiré des favoris'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ============ ROUTES BADGES/GAMIFICATION ============
@app.route('/api/badges', methods=['GET'])
def get_badges():
    badges = Badge.query.all()
    return jsonify([badge.to_dict() for badge in badges])


@app.route('/api/badges/check', methods=['POST'])
def check_badges():
    """Vérifie et attribue les badges"""
    try:
        history_count = SearchHistory.query.count()
        badges = Badge.query.all()
        existing_badge_ids = {b.badge_id for b in badges}

        badge_rules = [
            {
                'id': 'first_copy', 
                'condition': history_count >= 1, 
                'title': '🚀 Premier pas', 
                'description': 'Première commande copiée'
            },
            {
                'id': 'copy_10', 
                'condition': history_count >= 10, 
                'title': '⚡ 10 copies', 
                'description': '10 commandes copiées'
            },
            {
                'id': 'copy_100', 
                'condition': history_count >= 100, 
                'title': '🔥 100 copies', 
                'description': '100 commandes copiées'
            },
        ]

        earned_badges = []
        for rule in badge_rules:
            if rule['condition'] and rule['id'] not in existing_badge_ids:
                badge = Badge(
                    badge_id=rule['id'],
                    title=rule['title'],
                    description=rule['description'],
                    icon=rule['title'].split()[0]
                )
                db.session.add(badge)
                earned_badges.append(rule['title'])

        db.session.commit()
        all_badges = Badge.query.all()
        
        return jsonify({
            'earned': earned_badges, 
            'badges': [b.to_dict() for b in all_badges]
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ============ ROUTES FORMULAIRES ============
@app.route('/add')
def add_form():
    commands = Command.query.all()
    categories = sorted({cmd.categorie for cmd in commands})
    platforms = sorted({cmd.plateforme for cmd in commands})
    return render_template('add_command.html', 
                           categories=categories, 
                           platforms=platforms)


@app.route('/edit/<int:cmd_id>')
def edit_form(cmd_id):
    cmd = Command.query.get_or_404(cmd_id)
    commands = Command.query.all()
    categories = sorted({c.categorie for c in commands})
    platforms = sorted({c.plateforme for c in commands})
    
    command_dict = cmd.to_dict()
    
    return render_template('edit_command.html',
                           command=command_dict,
                           cmd_id=cmd_id,
                           categories=categories,
                           platforms=platforms)


# ============ ROUTES STATS ============
@app.route('/stats')
def stats():
    try:
        commands = Command.query.all()
        certifications = Certification.query.all()
        tools_list = Tool.query.all()
        vulnerabilities = Vulnerability.query.all()
        history = SearchHistory.query.all()

        categories = {}
        platforms = {}

        for cmd in commands:
            categories[cmd.categorie] = categories.get(cmd.categorie, 0) + 1
            platforms[cmd.plateforme] = platforms.get(cmd.plateforme, 0) + 1

        stats_data = {
            'total_commands': len(commands),
            'total_certs': len(certifications),
            'total_tools': len(tools_list),
            'total_vulns': len(vulnerabilities),
            'total_history': len(history),
            'categories': categories,
            'platforms': platforms
        }

        return render_template('stats.html', stats=stats_data)
    except Exception as e:
        return f"Erreur: {str(e)}", 500


# ============ ROUTES EXPORT ============
@app.route('/api/export/<export_type>', methods=['GET'])
def export_data(export_type):
    try:
        if export_type == 'all':
            data = {
                'commands': [c.to_dict() for c in Command.query.all()],
                'certifications': [c.to_dict() for c in Certification.query.all()],
                'tools': [t.to_dict() for t in Tool.query.all()],
                'vulnerabilities': [v.to_dict() for v in Vulnerability.query.all()],
            }
        elif export_type == 'commands':
            data = [c.to_dict() for c in Command.query.all()]
        elif export_type == 'certifications':
            data = [c.to_dict() for c in Certification.query.all()]
        elif export_type == 'tools':
            data = [t.to_dict() for t in Tool.query.all()]
        elif export_type == 'vulnerabilities':
            data = [v.to_dict() for v in Vulnerability.query.all()]
        else:
            return jsonify({'error': 'Type non reconnu'}), 400

        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============ HEALTH CHECK ============
@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint pour vérifier la santé de l'application"""
    try:
        # Test connexion DB
        db.session.execute(db.text('SELECT 1'))
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 503


# ============ ERROR HANDLERS ============
@app.errorhandler(404)
def not_found(error):
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Ressource non trouvée'}), 404
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(error):
    db.session.rollback()
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Erreur serveur interne'}), 500
    return render_template('500.html'), 500


@app.errorhandler(Exception)
def handle_exception(error):
    """Handler générique pour toutes les exceptions non gérées"""
    db.session.rollback()
    print(f"❌ Exception non gérée: {error}")
    import traceback
    traceback.print_exc()
    
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Une erreur est survenue'}), 500
    return "Une erreur est survenue", 500


# ============ COMMANDE CLI (Optionnel) ============
@app.cli.command()
def init_db():
    """Initialise la base de données"""
    db.create_all()
    print("✅ Base de données initialisée")


@app.cli.command()
def seed_db():
    """Remplit la base avec des données de test"""
    print("🌱 Seeding de la base de données...")
    # Tu peux ajouter du code ici pour insérer des données de test
    print("✅ Seeding terminé")


# ============ DÉMARRAGE ============
if __name__ == '__main__':
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', '0') == '1'
    
    print(f"\n{'='*50}")
    print(f"🚀 CyberSec Command Manager")
    print(f"{'='*50}")
    print(f"📍 Host: {host}")
    print(f"🔌 Port: {port}")
    print(f"🐛 Debug: {debug}")
    print(f"🗄️  Database: {app.config['SQLALCHEMY_DATABASE_URI'].split('@')[1] if '@' in app.config['SQLALCHEMY_DATABASE_URI'] else 'Local'}")
    print(f"{'='*50}\n")
    
    app.run(debug=debug, host=host, port=port)
