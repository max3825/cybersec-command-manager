from flask import Flask, render_template, request, jsonify, redirect, url_for
from models import db, Command, Certification, CheatSheet, Tool, Vulnerability, Note, Favorite, SearchHistory, Badge
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost:5432/cybersec_manager')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

db.init_app(app)

with app.app_context():
    db.create_all()
    print("✅ Database tables initialized")

# ============ ROUTE DASHBOARD ============
@app.route('/')
def dashboard():
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
        if cat in categories:
            categories[cat] += 1
        else:
            categories[cat] = 1
    
    return render_template('dashboard.html',
                         stats=stats,
                         recent_commands=recent_commands_data,
                         certifications=certifications_data,
                         badges=badges,
                         categories=categories)

# ============ ROUTES COMMANDES ============
@app.route('/commandes')
def index():
    commands = Command.query.all()
    # Convertir en dictionnaires
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
                           commands=commands_dict,  # ⬅️ Dictionnaires au lieu d'objets
                           categories=categories,
                           platforms=platforms,
                           favorites=favorites,
                           stats=stats)


@app.route('/api/commands', methods=['GET'])
def get_commands():
    commands = Command.query.all()
    return jsonify([cmd.to_dict() for cmd in commands])

@app.route('/api/commands', methods=['POST'])
def add_command():
    data = request.get_json()
    required_fields = ['nom', 'description', 'categorie', 'plateforme', 'arguments_options', 'exemple', 'usage', 'tags']

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

@app.route('/api/commands/<int:cmd_id>', methods=['PUT'])
def update_command(cmd_id):
    cmd = Command.query.get(cmd_id)
    if not cmd:
        return jsonify({'error': 'Non trouvé'}), 404
    
    data = request.get_json()
    for key, value in data.items():
        if hasattr(cmd, key):
            setattr(cmd, key, value)
    
    cmd.date_modification = datetime.utcnow()
    db.session.commit()
    return jsonify({'message': 'Mise à jour réussie'})

@app.route('/api/commands/<int:cmd_id>', methods=['DELETE'])
def delete_command(cmd_id):
    cmd = Command.query.get(cmd_id)
    if not cmd:
        return jsonify({'error': 'Non trouvé'}), 404
    
    db.session.delete(cmd)
    db.session.commit()
    return jsonify({'message': 'Suppression réussie'})

# ============ ROUTES CERTIFICATIONS ============
@app.route('/certifications')
def certifications():
    certs = Certification.query.all()
    # Convertir en dictionnaires
    certs_data = [cert.to_dict() for cert in certs]
    return render_template('certifications.html', certifications=certs_data)

# ============ ROUTES CERTIFICATIONS (ÉDITION) ============
@app.route('/certifications/<int:cert_id>', methods=['GET'])
def edit_certification_form(cert_id):
    cert = Certification.query.get(cert_id)
    if not cert:
        return redirect(url_for('certifications'))
    
    return render_template('edit_certification.html', certification=cert.to_dict(), cert_id=cert_id)

@app.route('/api/certifications/<int:cert_id>', methods=['PUT'])
def update_certification(cert_id):
    cert = Certification.query.get(cert_id)
    if not cert:
        return jsonify({'error': 'Non trouvé'}), 404
    
    data = request.get_json()
    for key, value in data.items():
        if hasattr(cert, key):
            setattr(cert, key, value)
    
    db.session.commit()
    return jsonify({'message': 'Certification mise à jour'})


@app.route('/api/certifications', methods=['GET'])
def get_certifications():
    certs = Certification.query.all()
    return jsonify([cert.to_dict() for cert in certs])

@app.route('/api/certifications', methods=['POST'])
def add_certification():
    data = request.get_json()
    cert = Certification(**data)
    db.session.add(cert)
    db.session.commit()
    return jsonify({'message': 'Certification ajoutée', 'id': cert.id}), 201

@app.route('/api/certifications/<int:cert_id>', methods=['DELETE'])
def delete_certification(cert_id):
    cert = Certification.query.get(cert_id)
    if not cert:
        return jsonify({'error': 'Non trouvé'}), 404
    
    db.session.delete(cert)
    db.session.commit()
    return jsonify({'message': 'Certification supprimée'})

# ============ ROUTES CHEAT SHEETS ============
@app.route('/cheatsheets')
def cheatsheets():
    sheets = CheatSheet.query.all()
    sheets_data = [sheet.to_dict() for sheet in sheets]
    return render_template('cheatsheets.html', cheatsheets=sheets_data)

# ============ ROUTES CHEATSHEETS (ÉDITION) ============
@app.route('/cheatsheets/<int:sheet_id>', methods=['GET'])
def edit_cheatsheet_form(sheet_id):
    sheet = CheatSheet.query.get(sheet_id)
    if not sheet:
        return redirect(url_for('cheatsheets'))
    
    return render_template('edit_cheatsheet.html', cheatsheet=sheet.to_dict(), sheet_id=sheet_id)

@app.route('/api/cheatsheets/<int:sheet_id>', methods=['PUT'])
def update_cheatsheet(sheet_id):
    sheet = CheatSheet.query.get(sheet_id)
    if not sheet:
        return jsonify({'error': 'Non trouvé'}), 404
    
    data = request.get_json()
    for key, value in data.items():
        if hasattr(sheet, key):
            setattr(sheet, key, value)
    
    db.session.commit()
    return jsonify({'message': 'Cheat sheet mis à jour'})



@app.route('/api/cheatsheets', methods=['GET'])
def get_cheatsheets():
    sheets = CheatSheet.query.all()
    return jsonify([sheet.to_dict() for sheet in sheets])

@app.route('/api/cheatsheets', methods=['POST'])
def add_cheatsheet():
    data = request.get_json()
    sheet = CheatSheet(**data)
    db.session.add(sheet)
    db.session.commit()
    return jsonify({'message': 'Cheat sheet ajoutée', 'id': sheet.id}), 201

@app.route('/api/cheatsheets/<int:sheet_id>', methods=['DELETE'])
def delete_cheatsheet(sheet_id):
    sheet = CheatSheet.query.get(sheet_id)
    if not sheet:
        return jsonify({'error': 'Non trouvé'}), 404
    
    db.session.delete(sheet)
    db.session.commit()
    return jsonify({'message': 'Cheat sheet supprimée'})

# ============ ROUTES NOTES/DOCUMENTATION ============
@app.route('/notes')
def notes():
    notes_list = Note.query.all()
    return render_template('notes.html', notes=notes_list)

@app.route('/api/notes', methods=['GET'])
def get_notes():
    notes_list = Note.query.all()
    return jsonify([note.to_dict() for note in notes_list])

@app.route('/api/notes', methods=['POST'])
def add_note():
    data = request.get_json()
    note = Note(**data)
    db.session.add(note)
    db.session.commit()
    return jsonify({'message': 'Note créée', 'id': note.id}), 201

@app.route('/api/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    note = Note.query.get(note_id)
    if not note:
        return jsonify({'error': 'Non trouvé'}), 404
    
    data = request.get_json()
    for key, value in data.items():
        if hasattr(note, key):
            setattr(note, key, value)
    
    note.date_modification = datetime.utcnow()
    db.session.commit()
    return jsonify({'message': 'Note mise à jour'})

@app.route('/api/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    note = Note.query.get(note_id)
    if not note:
        return jsonify({'error': 'Non trouvé'}), 404
    
    db.session.delete(note)
    db.session.commit()
    return jsonify({'message': 'Note supprimée'})

# ============ ROUTES OUTILS ============
@app.route('/tools')
def tools():
    tools_list = Tool.query.all()
    tools_data = [tool.to_dict() for tool in tools_list]
    return render_template('tools.html', tools=tools_data)

# ============ ROUTES TOOLS (ÉDITION) ============
@app.route('/tools/<int:tool_id>', methods=['GET'])
def edit_tool_form(tool_id):
    tool = Tool.query.get(tool_id)
    if not tool:
        return redirect(url_for('tools'))
    
    return render_template('edit_tool.html', tool=tool.to_dict(), tool_id=tool_id)

@app.route('/api/tools/<int:tool_id>', methods=['PUT'])
def update_tool(tool_id):
    tool = Tool.query.get(tool_id)
    if not tool:
        return jsonify({'error': 'Non trouvé'}), 404
    
    data = request.get_json()
    for key, value in data.items():
        if hasattr(tool, key):
            setattr(tool, key, value)
    
    db.session.commit()
    return jsonify({'message': 'Outil mis à jour'})


@app.route('/api/tools', methods=['GET'])
def get_tools():
    tools_list = Tool.query.all()
    return jsonify([tool.to_dict() for tool in tools_list])

@app.route('/api/tools', methods=['POST'])
def add_tool():
    data = request.get_json()
    tool = Tool(**data)
    db.session.add(tool)
    db.session.commit()
    return jsonify({'message': 'Outil ajouté', 'id': tool.id}), 201

@app.route('/api/tools/<int:tool_id>', methods=['DELETE'])
def delete_tool(tool_id):
    tool = Tool.query.get(tool_id)
    if not tool:
        return jsonify({'error': 'Non trouvé'}), 404
    
    db.session.delete(tool)
    db.session.commit()
    return jsonify({'message': 'Outil supprimé'})

# ============ ROUTES VULNÉRABILITÉS ============
@app.route('/vulnerabilities')
def vulnerabilities():
    vulns = Vulnerability.query.all()
    vulns_data = [vuln.to_dict() for vuln in vulns]
    return render_template('vulnerabilities.html', vulnerabilities=vulns_data)


@app.route('/api/vulnerabilities', methods=['GET'])
def get_vulnerabilities():
    vulns = Vulnerability.query.all()
    return jsonify([vuln.to_dict() for vuln in vulns])

@app.route('/api/vulnerabilities', methods=['POST'])
def add_vulnerability():
    data = request.get_json()
    vuln = Vulnerability(**data)
    db.session.add(vuln)
    db.session.commit()
    return jsonify({'message': 'Vulnérabilité ajoutée', 'id': vuln.id}), 201

@app.route('/api/vulnerabilities/<int:vuln_id>', methods=['DELETE'])
def delete_vulnerability(vuln_id):
    vuln = Vulnerability.query.get(vuln_id)
    if not vuln:
        return jsonify({'error': 'Non trouvé'}), 404
    
    db.session.delete(vuln)
    db.session.commit()
    return jsonify({'message': 'Vulnérabilité supprimée'})

# ============ ROUTES VULNÉRABILITÉS (ÉDITION) ============
@app.route('/vulnerabilities/<int:vuln_id>', methods=['GET'])
def edit_vulnerability_form(vuln_id):
    vuln = Vulnerability.query.get(vuln_id)
    if not vuln:
        return redirect(url_for('vulnerabilities'))
    
    return render_template('edit_vulnerability.html', vulnerability=vuln.to_dict(), vuln_id=vuln_id)

@app.route('/api/vulnerabilities/<int:vuln_id>', methods=['PUT'])
def update_vulnerability(vuln_id):
    vuln = Vulnerability.query.get(vuln_id)
    if not vuln:
        return jsonify({'error': 'Non trouvé'}), 404
    
    data = request.get_json()
    for key, value in data.items():
        if hasattr(vuln, key):
            setattr(vuln, key, value)
    
    vuln.date_ajout = datetime.utcnow()
    db.session.commit()
    return jsonify({'message': 'Vulnérabilité mise à jour'})


# ============ ROUTES SEARCH GLOBALE ============
@app.route('/api/search/global', methods=['GET'])
def search_global():
    """Recherche globale across all modules"""
    query = request.args.get('q', '').lower()

    if not query or len(query) < 2:
        return jsonify([])

    results = {
        'commands': [],
        'cheatsheets': [],
        'tools': [],
        'vulnerabilities': [],
        'certifications': [],
        'notes': []
    }

    # Search commands
    commands = Command.query.filter(
        (Command.nom.ilike(f'%{query}%')) |
        (Command.description.ilike(f'%{query}%')) |
        (Command.tags.ilike(f'%{query}%'))
    ).all()
    for cmd in commands:
        results['commands'].append({
            'id': cmd.id,
            'nom': cmd.nom,
            'description': cmd.description,
            'type': 'command'
        })

    # Search cheatsheets
    sheets = CheatSheet.query.filter(
        (CheatSheet.titre.ilike(f'%{query}%')) |
        (CheatSheet.description.ilike(f'%{query}%'))
    ).all()
    for sheet in sheets:
        results['cheatsheets'].append({
            'id': sheet.id,
            'titre': sheet.titre,
            'description': sheet.description,
            'type': 'cheatsheet'
        })

    # Search tools
    tools_list = Tool.query.filter(
        (Tool.nom.ilike(f'%{query}%')) |
        (Tool.description.ilike(f'%{query}%'))
    ).all()
    for tool in tools_list:
        results['tools'].append({
            'id': tool.id,
            'nom': tool.nom,
            'description': tool.description,
            'type': 'tool'
        })

    # Search vulnerabilities
    vulns = Vulnerability.query.filter(
        (Vulnerability.cve.ilike(f'%{query}%')) |
        (Vulnerability.titre.ilike(f'%{query}%'))
    ).all()
    for vuln in vulns:
        results['vulnerabilities'].append({
            'id': vuln.id,
            'cve': vuln.cve,
            'titre': vuln.titre,
            'type': 'vulnerability'
        })

    # Search certifications
    certs = Certification.query.filter(
        (Certification.nom.ilike(f'%{query}%')) |
        (Certification.description.ilike(f'%{query}%'))
    ).all()
    for cert in certs:
        results['certifications'].append({
            'id': cert.id,
            'nom': cert.nom,
            'description': cert.description,
            'type': 'certification'
        })

    # Search notes
    notes_list = Note.query.filter(
        (Note.titre.ilike(f'%{query}%')) |
        (Note.contenu.ilike(f'%{query}%'))
    ).all()
    for note in notes_list:
        results['notes'].append({
            'id': note.id,
            'titre': note.titre,
            'contenu': note.contenu[:100],
            'type': 'note'
        })

    return jsonify(results)

@app.route('/api/search/suggestions', methods=['GET'])
def search_suggestions():
    """Get suggestions based on recent searches"""
    history = SearchHistory.query.order_by(SearchHistory.date.desc()).limit(20).all()
    suggestions = []

    seen = set()
    for entry in history:
        search_term = entry.search_term
        if search_term and search_term not in seen:
            suggestions.append(search_term)
            seen.add(search_term)

    return jsonify(suggestions[:10])

@app.route('/api/search/add-history', methods=['POST'])
def add_search_history():
    """Add search to history"""
    data = request.get_json()
    
    hist = SearchHistory(
        search_term=data.get('search'),
        type=data.get('type', 'general')
    )
    db.session.add(hist)
    db.session.commit()
    
    return jsonify({'message': 'Search added to history'}), 201

# ============ ROUTES HISTORIQUE ============
@app.route('/api/history', methods=['GET'])
def get_history():
    history = SearchHistory.query.order_by(SearchHistory.date.desc()).all()
    return jsonify([h.to_dict() for h in history])

@app.route('/api/history/add', methods=['POST'])
def add_to_history():
    data = request.get_json()
    hist = SearchHistory(**data)
    db.session.add(hist)
    db.session.commit()
    return jsonify({'message': 'Ajouté à l\'historique'}), 201

# ============ ROUTES FAVORIS ============
@app.route('/api/favorites', methods=['GET'])
def get_favorites():
    favorites = Favorite.query.all()
    return jsonify([fav.to_dict() for fav in favorites])

@app.route('/api/favorites', methods=['POST'])
def add_favorite():
    data = request.get_json()
    command_id = data.get('command_id')
    
    # Vérifier si déjà en favori
    existing = Favorite.query.filter_by(command_id=command_id).first()
    if existing:
        return jsonify({'message': 'Déjà en favoris'}), 200
    
    fav = Favorite(command_id=command_id)
    db.session.add(fav)
    db.session.commit()
    return jsonify({'message': 'Ajouté aux favoris'}), 201

@app.route('/api/favorites/<int:cmd_id>', methods=['POST'])
def favorite_command(cmd_id):
    """Add command to favorites"""
    existing = Favorite.query.filter_by(command_id=cmd_id).first()
    if existing:
        return jsonify({'message': 'Déjà en favoris'}), 200
    
    fav = Favorite(command_id=cmd_id)
    db.session.add(fav)
    db.session.commit()
    return jsonify({'message': 'Ajouté aux favoris'})

@app.route('/api/favorites/<int:cmd_id>', methods=['DELETE'])
def unfavorite_command(cmd_id):
    """Remove command from favorites"""
    fav = Favorite.query.filter_by(command_id=cmd_id).first()
    if fav:
        db.session.delete(fav)
        db.session.commit()
    return jsonify({'message': 'Retiré des favoris'})

# ============ ROUTES BADGES/GAMIFICATION ============
@app.route('/api/badges', methods=['GET'])
def get_badges():
    badges = Badge.query.all()
    return jsonify([badge.to_dict() for badge in badges])

@app.route('/api/badges/check', methods=['POST'])
def check_badges():
    """Vérifie et attribue les badges basés sur les activités"""
    history_count = SearchHistory.query.count()
    badges = Badge.query.all()
    existing_badge_ids = {b.badge_id for b in badges}

    # Logique des badges
    badge_rules = [
        {'id': 'first_copy', 'condition': history_count >= 1, 'title': '🚀 Premier pas', 'description': 'Première commande copiée'},
        {'id': 'copy_10', 'condition': history_count >= 10, 'title': '⚡ 10 copies', 'description': '10 commandes copiées'},
        {'id': 'copy_100', 'condition': history_count >= 100, 'title': '🔥 100 copies', 'description': '100 commandes copiées'},
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
    return jsonify({'earned': earned_badges, 'badges': [b.to_dict() for b in all_badges]})

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
    # Récupérer la commande depuis la DB
    cmd = Command.query.get(cmd_id)
    
    # Si pas trouvée, rediriger
    if not cmd:
        return redirect(url_for('dashboard'))
    
    # Récupérer toutes les commandes pour les catégories/platforms
    commands = Command.query.all()
    categories = sorted({c.categorie for c in commands})
    platforms = sorted({c.plateforme for c in commands})
    
    # Convertir en dict pour le template
    command_dict = cmd.to_dict()
    
    return render_template('edit_command.html',
                           command=command_dict,  # ⬅️ Dict au lieu d'objet
                           cmd_id=cmd_id,
                           categories=categories,
                           platforms=platforms)


# ============ ROUTES STATS ============
@app.route('/stats')
def stats():
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

# ============ ROUTES EXPORT ============
@app.route('/api/export/<export_type>', methods=['GET'])
def export_data(export_type):
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

# ============ ERROR HANDLERS ============
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500

@app.route('/api/search', methods=['GET'])
def global_search():
    query = request.args.get('q', '').lower()
    print(f"🔍 Recherche: '{query}'")  # Debug
    
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
        print(f"✅ Commandes trouvées: {len(commands)}")  # Debug
        results['commands'] = [cmd.to_dict() for cmd in commands]
        
        # Recherche dans les vulnérabilités
        vulns = Vulnerability.query.filter(
            db.or_(
                Vulnerability.cve.ilike(f'%{query}%'),
                Vulnerability.titre.ilike(f'%{query}%'),
                Vulnerability.description.ilike(f'%{query}%')
            )
        ).limit(5).all()
        print(f"✅ CVE trouvées: {len(vulns)}")  # Debug
        results['vulnerabilities'] = [vuln.to_dict() for vuln in vulns]
        
        # Recherche dans les outils
        tools = Tool.query.filter(
            db.or_(
                Tool.nom.ilike(f'%{query}%'),
                Tool.description.ilike(f'%{query}%'),
                Tool.categorie.ilike(f'%{query}%')
            )
        ).limit(5).all()
        print(f"✅ Outils trouvés: {len(tools)}")  # Debug
        results['tools'] = [tool.to_dict() for tool in tools]
        
        # Recherche dans les certifications
        certs = Certification.query.filter(
            db.or_(
                Certification.nom.ilike(f'%{query}%'),
                Certification.description.ilike(f'%{query}%'),
                Certification.organisme.ilike(f'%{query}%')
            )
        ).limit(5).all()
        print(f"✅ Certifications trouvées: {len(certs)}")  # Debug
        results['certifications'] = [cert.to_dict() for cert in certs]
        
        # Recherche dans les cheat sheets
        sheets = CheatSheet.query.filter(
            db.or_(
                CheatSheet.titre.ilike(f'%{query}%'),
                CheatSheet.description.ilike(f'%{query}%'),
                CheatSheet.categorie.ilike(f'%{query}%')
            )
        ).limit(5).all()
        print(f"✅ Cheat Sheets trouvés: {len(sheets)}")  # Debug
        results['cheatsheets'] = [sheet.to_dict() for sheet in sheets]
        
        print(f"📊 Total résultats: {sum(len(v) for v in results.values())}")  # Debug
        
    except Exception as e:
        print(f"❌ Erreur recherche: {e}")  # Debug
        import traceback
        traceback.print_exc()
    
    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
