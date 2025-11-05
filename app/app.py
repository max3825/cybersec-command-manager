from flask import Flask, render_template, request, jsonify, redirect, url_for
from models import db, Command, Certification, CheatSheet, Tool, Vulnerability, Note, Favorite, SearchHistory
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Configuration depuis variables d'environnement
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'postgresql://postgres:password@localhost:5432/cybersec_manager'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

db.init_app(app)

# Créer tables au démarrage si elles n'existent pas
with app.app_context():
    db.create_all()
    print("✅ Database tables initialized")

# ... reste du code identique

# Fichiers de données
DATA_FILES = {
    'commands': 'data/commands.json',
    'certifications': 'data/certifications.json',
    'cheatsheets': 'data/cheatsheets.json',
    'notes': 'data/notes.json',
    'tools': 'data/tools.json',
    'vulnerabilities': 'data/vulnerabilities.json',
    'favorites': 'data/favorites.json',
    'history': 'data/history.json',
    'badges': 'data/badges.json',
}


def load_data(data_type):
    """Charge les données d'un type spécifique"""
    if os.path.exists(DATA_FILES[data_type]):
        with open(DATA_FILES[data_type], 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_data(data_type, data):
    """Sauvegarde les données d'un type spécifique"""
    os.makedirs('data', exist_ok=True)
    with open(DATA_FILES[data_type], 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ============ ROUTE DASHBOARD ============
@app.route('/')
def dashboard():
    """Enhanced dashboard homepage"""
    commands = load_data('commands')
    certifications = load_data('certifications')
    cheatsheets = load_data('cheatsheets')
    tools = load_data('tools')
    vulnerabilities = load_data('vulnerabilities')
    favorites = load_data('favorites')
    history = load_data('history')
    badges = load_data('badges')

    # Stats
    stats = {
        'total_commands': len(commands),
        'total_certs': len(certifications),
        'total_sheets': len(cheatsheets),
        'total_tools': len(tools),
        'total_vulns': len(vulnerabilities),
        'total_favorites': len(favorites),
        'total_history': len(history),
        'total_badges': len(badges)
    }

    # Recent commands (dernières 5)
    recent_commands = commands[-5:] if commands else []

    # Certifications progress
    cert_progress = []
    for idx, cert in enumerate(certifications[:3]):
        cert_progress.append({
            'id': idx,
            'nom': cert['nom'],
            'organisme': cert['organisme'],
            'niveau': cert['niveau'],
            'prix': cert['prix_usd'],
            'progress': 35
        })

    # Categories breakdown
    categories = {}
    for cmd in commands:
        cat = cmd['categorie']
        categories[cat] = categories.get(cat, 0) + 1

    return render_template('templates/dashboard.html',
                           stats=stats,
                           recent_commands=recent_commands,
                           cert_progress=cert_progress,
                           categories=categories,
                           favorites_count=len(favorites),
                           badges=badges)


# ============ ROUTES COMMANDES ============
@app.route('/commandes')
def index():
    commands = load_data('commands')
    categories = sorted(list(set(cmd['categorie'] for cmd in commands)))
    platforms = sorted(list(set(cmd['plateforme'] for cmd in commands)))
    favorites = load_data('favorites')

    stats = {
        'total': len(commands),
        'linux': sum(1 for cmd in commands if 'Linux' in cmd['plateforme']),
        'windows': sum(1 for cmd in commands if 'Windows' in cmd['plateforme']),
        'categories': len(categories)
    }

    return render_template('templates/index.html',
                           commands=commands,
                           categories=categories,
                           platforms=platforms,
                           favorites=favorites,
                           stats=stats)


@app.route('/api/commands', methods=['GET'])
def get_commands():
    return jsonify(load_data('commands'))


@app.route('/api/commands', methods=['POST'])
def add_command():
    data = request.get_json()
    required_fields = ['nom', 'description', 'categorie', 'plateforme', 'arguments_options', 'exemple', 'usage', 'tags']

    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Champ manquant: {field}'}), 400

    data['date_ajout'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    commands = load_data('commands')
    commands.append(data)
    save_data('commands', commands)
    return jsonify({'message': 'Commande ajoutée', 'id': len(commands) - 1}), 201


@app.route('/api/commands/<int:cmd_id>', methods=['PUT'])
def update_command(cmd_id):
    data = request.get_json()
    commands = load_data('commands')
    if 0 <= cmd_id < len(commands):
        data['date_modification'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        commands[cmd_id].update(data)
        save_data('commands', commands)
        return jsonify({'message': 'Mise à jour réussie'})
    return jsonify({'error': 'Non trouvé'}), 404


@app.route('/api/commands/<int:cmd_id>', methods=['DELETE'])
def delete_command(cmd_id):
    commands = load_data('commands')
    if 0 <= cmd_id < len(commands):
        commands.pop(cmd_id)
        save_data('commands', commands)
        return jsonify({'message': 'Suppression réussie'})
    return jsonify({'error': 'Non trouvé'}), 404


# ============ ROUTES CERTIFICATIONS ============
@app.route('/certifications')
def certifications():
    certs = load_data('certifications')
    return render_template('templates/certifications.html', certifications=certs)


@app.route('/api/certifications', methods=['GET'])
def get_certifications():
    return jsonify(load_data('certifications'))


@app.route('/api/certifications', methods=['POST'])
def add_certification():
    data = request.get_json()
    certs = load_data('certifications')
    data['date_ajout'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    certs.append(data)
    save_data('certifications', certs)
    return jsonify({'message': 'Certification ajoutée'}), 201


@app.route('/api/certifications/<int:cert_id>', methods=['DELETE'])
def delete_certification(cert_id):
    certs = load_data('certifications')
    if 0 <= cert_id < len(certs):
        certs.pop(cert_id)
        save_data('certifications', certs)
        return jsonify({'message': 'Certification supprimée'})
    return jsonify({'error': 'Non trouvé'}), 404


# ============ ROUTES CHEAT SHEETS ============
@app.route('/cheatsheets')
def cheatsheets():
    sheets = load_data('cheatsheets')
    return render_template('templates/cheatsheets.html', cheatsheets=sheets)


@app.route('/api/cheatsheets', methods=['GET'])
def get_cheatsheets():
    return jsonify(load_data('cheatsheets'))


@app.route('/api/cheatsheets', methods=['POST'])
def add_cheatsheet():
    data = request.get_json()
    sheets = load_data('cheatsheets')
    data['date_ajout'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sheets.append(data)
    save_data('cheatsheets', sheets)
    return jsonify({'message': 'Cheat sheet ajoutée'}), 201


@app.route('/api/cheatsheets/<int:sheet_id>', methods=['DELETE'])
def delete_cheatsheet(sheet_id):
    sheets = load_data('cheatsheets')
    if 0 <= sheet_id < len(sheets):
        sheets.pop(sheet_id)
        save_data('cheatsheets', sheets)
        return jsonify({'message': 'Cheat sheet supprimée'})
    return jsonify({'error': 'Non trouvé'}), 404


# ============ ROUTES NOTES/DOCUMENTATION ============
@app.route('/notes')
def notes():
    notes_list = load_data('notes')
    return render_template('templates/notes.html', notes=notes_list)


@app.route('/api/notes', methods=['GET'])
def get_notes():
    return jsonify(load_data('notes'))


@app.route('/api/notes', methods=['POST'])
def add_note():
    data = request.get_json()
    notes_list = load_data('notes')
    data['date_creation'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data['date_modification'] = data['date_creation']
    notes_list.append(data)
    save_data('notes', notes_list)
    return jsonify({'message': 'Note créée', 'id': len(notes_list) - 1}), 201


@app.route('/api/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    data = request.get_json()
    notes_list = load_data('notes')
    if 0 <= note_id < len(notes_list):
        data['date_modification'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        notes_list[note_id].update(data)
        save_data('notes', notes_list)
        return jsonify({'message': 'Note mise à jour'})
    return jsonify({'error': 'Non trouvé'}), 404


@app.route('/api/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    notes_list = load_data('notes')
    if 0 <= note_id < len(notes_list):
        notes_list.pop(note_id)
        save_data('notes', notes_list)
        return jsonify({'message': 'Note supprimée'})
    return jsonify({'error': 'Non trouvé'}), 404


# ============ ROUTES OUTILS ============
@app.route('/tools')
def tools():
    tools_list = load_data('tools')
    return render_template('templates/tools.html', tools=tools_list)


@app.route('/api/tools', methods=['GET'])
def get_tools():
    return jsonify(load_data('tools'))


@app.route('/api/tools', methods=['POST'])
def add_tool():
    data = request.get_json()
    tools_list = load_data('tools')
    data['date_ajout'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    tools_list.append(data)
    save_data('tools', tools_list)
    return jsonify({'message': 'Outil ajouté'}), 201


@app.route('/api/tools/<int:tool_id>', methods=['DELETE'])
def delete_tool(tool_id):
    tools_list = load_data('tools')
    if 0 <= tool_id < len(tools_list):
        tools_list.pop(tool_id)
        save_data('tools', tools_list)
        return jsonify({'message': 'Outil supprimé'})
    return jsonify({'error': 'Non trouvé'}), 404


# ============ ROUTES VULNÉRABILITÉS ============
@app.route('/vulnerabilities')
def vulnerabilities():
    vulns = load_data('vulnerabilities')
    return render_template('templates/vulnerabilities.html', vulnerabilities=vulns)


@app.route('/api/vulnerabilities', methods=['GET'])
def get_vulnerabilities():
    return jsonify(load_data('vulnerabilities'))


@app.route('/api/vulnerabilities', methods=['POST'])
def add_vulnerability():
    data = request.get_json()
    vulns = load_data('vulnerabilities')
    data['date_ajout'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    vulns.append(data)
    save_data('vulnerabilities', vulns)
    return jsonify({'message': 'Vulnérabilité ajoutée'}), 201


@app.route('/api/vulnerabilities/<int:vuln_id>', methods=['DELETE'])
def delete_vulnerability(vuln_id):
    vulns = load_data('vulnerabilities')
    if 0 <= vuln_id < len(vulns):
        vulns.pop(vuln_id)
        save_data('vulnerabilities', vulns)
        return jsonify({'message': 'Vulnérabilité supprimée'})
    return jsonify({'error': 'Non trouvé'}), 404


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
    commands = load_data('commands')
    for idx, cmd in enumerate(commands):
        if query in cmd['nom'].lower() or query in cmd['description'].lower() or query in cmd.get('tags', '').lower():
            results['commands'].append({
                'id': idx,
                'nom': cmd['nom'],
                'description': cmd['description'],
                'type': 'command'
            })

    # Search cheatsheets
    cheatsheets = load_data('cheatsheets')
    for idx, sheet in enumerate(cheatsheets):
        if query in sheet['titre'].lower() or query in sheet['description'].lower():
            results['cheatsheets'].append({
                'id': idx,
                'titre': sheet['titre'],
                'description': sheet['description'],
                'type': 'cheatsheet'
            })

    # Search tools
    tools_list = load_data('tools')
    for idx, tool in enumerate(tools_list):
        if query in tool['nom'].lower() or query in tool['description'].lower():
            results['tools'].append({
                'id': idx,
                'nom': tool['nom'],
                'description': tool['description'],
                'type': 'tool'
            })

    # Search vulnerabilities
    vulns = load_data('vulnerabilities')
    for idx, vuln in enumerate(vulns):
        if query in vuln['cve'].lower() or query in vuln['titre'].lower():
            results['vulnerabilities'].append({
                'id': idx,
                'cve': vuln['cve'],
                'titre': vuln['titre'],
                'type': 'vulnerability'
            })

    # Search certifications
    certs = load_data('certifications')
    for idx, cert in enumerate(certs):
        if query in cert['nom'].lower() or query in cert['description'].lower():
            results['certifications'].append({
                'id': idx,
                'nom': cert['nom'],
                'description': cert['description'],
                'type': 'certification'
            })

    # Search notes
    notes_list = load_data('notes')
    for idx, note in enumerate(notes_list):
        if query in note['titre'].lower() or query in note['contenu'].lower():
            results['notes'].append({
                'id': idx,
                'titre': note['titre'],
                'contenu': note['contenu'][:100],
                'type': 'note'
            })

    return jsonify(results)


@app.route('/api/search/suggestions', methods=['GET'])
def search_suggestions():
    """Get suggestions based on recent searches"""
    history = load_data('history')
    suggestions = []

    # Get unique searches from history (last 20)
    seen = set()
    for entry in reversed(history[-20:]):
        search_term = entry.get('search', '')
        if search_term and search_term not in seen:
            suggestions.append(search_term)
            seen.add(search_term)

    return jsonify(suggestions[:10])


@app.route('/api/search/add-history', methods=['POST'])
def add_search_history():
    """Add search to history"""
    data = request.get_json()
    history = load_data('history')

    history.append({
        'search': data.get('search'),
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'type': data.get('type', 'general')
    })

    # Keep only last 100 searches
    if len(history) > 100:
        history = history[-100:]

    save_data('history', history)
    return jsonify({'message': 'Search added to history'}), 201


# ============ ROUTES HISTORIQUE ============
@app.route('/api/history', methods=['GET'])
def get_history():
    return jsonify(load_data('history'))


@app.route('/api/history/add', methods=['POST'])
def add_to_history():
    data = request.get_json()
    history = load_data('history')
    data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    history.append(data)
    # Garder seulement les 100 derniers
    if len(history) > 100:
        history = history[-100:]
    save_data('history', history)
    return jsonify({'message': 'Ajouté à l\'historique'}), 201


# ============ ROUTES FAVORIS ============
@app.route('/api/favorites', methods=['GET'])
def get_favorites():
    return jsonify(load_data('favorites'))


@app.route('/api/favorites', methods=['POST'])
def add_favorite():
    data = request.get_json()
    favorites = load_data('favorites')
    if data not in favorites:
        favorites.append(data)
        save_data('favorites', favorites)
    return jsonify({'message': 'Ajouté aux favoris'}), 201


@app.route('/api/favorites/<int:cmd_id>', methods=['POST'])
def favorite_command(cmd_id):
    """Add command to favorites"""
    favorites = load_data('favorites')
    if cmd_id not in favorites:
        favorites.append(cmd_id)
        save_data('favorites', favorites)
    return jsonify({'message': 'Ajouté aux favoris'})


@app.route('/api/favorites/<int:cmd_id>', methods=['DELETE'])
def unfavorite_command(cmd_id):
    """Remove command from favorites"""
    favorites = load_data('favorites')
    if cmd_id in favorites:
        favorites.remove(cmd_id)
        save_data('favorites', favorites)
    return jsonify({'message': 'Retiré des favoris'})


# ============ ROUTES BADGES/GAMIFICATION ============
@app.route('/api/badges', methods=['GET'])
def get_badges():
    return jsonify(load_data('badges'))


@app.route('/api/badges/check', methods=['POST'])
def check_badges():
    """Vérifie et attribue les badges basés sur les activités"""
    history = load_data('history')
    badges = load_data('badges')

    # Logique des badges
    badge_rules = [
        {'id': 'first_copy', 'condition': len(history) >= 1, 'title': '🚀 Premier pas'},
        {'id': 'copy_10', 'condition': len(history) >= 10, 'title': '⚡ 10 copies'},
        {'id': 'copy_100', 'condition': len(history) >= 100, 'title': '🔥 100 copies'},
    ]

    earned_badges = []
    for rule in badge_rules:
        if rule['condition'] and rule['id'] not in [b.get('id') for b in badges]:
            badges.append({
                'id': rule['id'],
                'title': rule['title'],
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            earned_badges.append(rule['title'])

    save_data('badges', badges)
    return jsonify({'earned': earned_badges, 'badges': badges})


# ============ ROUTES FORMULAIRES ============
@app.route('/add')
def add_form():
    commands = load_data('commands')
    categories = sorted(list(set(cmd['categorie'] for cmd in commands)))
    platforms = sorted(list(set(cmd['plateforme'] for cmd in commands)))
    return render_template('templates/add_command.html', categories=categories, platforms=platforms)


@app.route('/edit/<int:cmd_id>')
def edit_form(cmd_id):
    commands = load_data('commands')
    if 0 <= cmd_id < len(commands):
        categories = sorted(list(set(cmd['categorie'] for cmd in commands)))
        platforms = sorted(list(set(cmd['plateforme'] for cmd in commands)))
        return render_template('templates/edit_command.html',
                               command=commands[cmd_id],
                               cmd_id=cmd_id,
                               categories=categories,
                               platforms=platforms)
    return redirect(url_for('dashboard'))


# ============ ROUTES STATS ============
@app.route('/stats')
def stats():
    commands = load_data('commands')
    certifications = load_data('certifications')
    tools_list = load_data('tools')
    vulnerabilities = load_data('vulnerabilities')
    history = load_data('history')

    categories = {}
    platforms = {}

    for cmd in commands:
        categories[cmd['categorie']] = categories.get(cmd['categorie'], 0) + 1
        platforms[cmd['plateforme']] = platforms.get(cmd['plateforme'], 0) + 1

    stats_data = {
        'total_commands': len(commands),
        'total_certs': len(certifications),
        'total_tools': len(tools_list),
        'total_vulns': len(vulnerabilities),
        'total_history': len(history),
        'categories': categories,
        'platforms': platforms
    }

    return render_template('templates/stats.html', stats=stats_data)


# ============ ROUTES EXPORT ============
@app.route('/api/export/<export_type>', methods=['GET'])
def export_data(export_type):
    if export_type == 'all':
        data = {
            'commands': load_data('commands'),
            'certifications': load_data('certifications'),
            'tools': load_data('tools'),
            'vulnerabilities': load_data('vulnerabilities'),
        }
    else:
        data = load_data(export_type + 's')

    return jsonify(data)


# ============ ERROR HANDLERS ============
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500


if __name__ == '__main__':
    # Créer les fichiers de données vides s'ils n'existent pas
    for data_type in DATA_FILES:
        os.makedirs('data', exist_ok=True)
        if not os.path.exists(DATA_FILES[data_type]):
            save_data(data_type, [])

    app.run(debug=True, host='0.0.0.0', port=5008)
