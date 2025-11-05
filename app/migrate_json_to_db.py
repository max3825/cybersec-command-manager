import json
import os
from app import app, db
from models import Command, Certification, CheatSheet, Tool, Vulnerability, Note


def migrate_json_to_database():
    """Migrate toutes les données JSON vers PostgreSQL"""

    with app.app_context():
        # Vérifier si data existe déjà
        if Command.query.first() is not None:
            print("⚠️  Base de données déjà peuplée, abandon de la migration")
            return

        print("🚀 Migration des données JSON vers PostgreSQL...\n")

        # ============ IMPORT COMMANDS ============
        try:
            if os.path.exists('data/commands.json'):
                with open('data/commands.json', 'r', encoding='utf-8') as f:
                    commands = json.load(f)
                    for cmd_data in commands:
                        cmd = Command(
                            nom=cmd_data.get('nom'),
                            description=cmd_data.get('description'),
                            categorie=cmd_data.get('categorie'),
                            plateforme=cmd_data.get('plateforme'),
                            arguments_options=cmd_data.get('arguments_options', ''),
                            exemple=cmd_data.get('exemple', ''),
                            usage=cmd_data.get('usage', ''),
                            tags=cmd_data.get('tags', ''),
                            niveau=cmd_data.get('niveau', 'Débutant'),
                            ressources=cmd_data.get('ressources', '')
                        )
                        db.session.add(cmd)
                    db.session.commit()
                    print(f"✅ {len(commands)} commandes importées")
        except Exception as e:
            print(f"❌ Erreur import commands: {e}")

        # ============ IMPORT CERTIFICATIONS ============
        try:
            if os.path.exists('data/certifications.json'):
                with open('data/certifications.json', 'r', encoding='utf-8') as f:
                    certs = json.load(f)
                    for cert_data in certs:
                        cert = Certification(
                            nom=cert_data.get('nom'),
                            organisme=cert_data.get('organisme'),
                            description=cert_data.get('description'),
                            niveau=cert_data.get('niveau'),
                            prix_usd=cert_data.get('prix_usd', 0),
                            duree_validite=cert_data.get('duree_validite', 36),
                            duree_etude=cert_data.get('duree_etude'),
                            domaines=json.dumps(cert_data.get('domaines', [])) if isinstance(cert_data.get('domaines'),
                                                                                             list) else cert_data.get(
                                'domaines'),
                            commandes_recommandees=json.dumps(
                                cert_data.get('commandes_recommandees', [])) if isinstance(
                                cert_data.get('commandes_recommandees'), list) else cert_data.get(
                                'commandes_recommandees'),
                            prerequisites=cert_data.get('prerequisites'),
                            lien=cert_data.get('lien')
                        )
                        db.session.add(cert)
                    db.session.commit()
                    print(f"✅ {len(certs)} certifications importées")
        except Exception as e:
            print(f"❌ Erreur import certifications: {e}")

        # ============ IMPORT CHEATSHEETS ============
        try:
            if os.path.exists('data/cheatsheets.json'):
                with open('data/cheatsheets.json', 'r', encoding='utf-8') as f:
                    sheets = json.load(f)
                    for sheet_data in sheets:
                        sheet = CheatSheet(
                            titre=sheet_data.get('titre'),
                            description=sheet_data.get('description'),
                            categorie=sheet_data.get('categorie'),
                            niveau=sheet_data.get('niveau'),
                            contenu=sheet_data.get('contenu', ''),
                            commandes=json.dumps(sheet_data.get('commandes', [])) if isinstance(
                                sheet_data.get('commandes'), list) else sheet_data.get('commandes'),
                            ressources=sheet_data.get('ressources', '')
                        )
                        db.session.add(sheet)
                    db.session.commit()
                    print(f"✅ {len(sheets)} cheat sheets importées")
        except Exception as e:
            print(f"❌ Erreur import cheatsheets: {e}")

        # ============ IMPORT TOOLS ============
        try:
            if os.path.exists('data/tools.json'):
                with open('data/tools.json', 'r', encoding='utf-8') as f:
                    tools = json.load(f)
                    for tool_data in tools:
                        tool = Tool(
                            nom=tool_data.get('nom'),
                            description=tool_data.get('description'),
                            categorie=tool_data.get('categorie'),
                            type=tool_data.get('type'),
                            installation=tool_data.get('installation'),
                            documentation=tool_data.get('documentation'),
                            prix=tool_data.get('prix', 'Gratuit'),
                            plateforme=json.dumps(tool_data.get('plateforme', [])) if isinstance(
                                tool_data.get('plateforme'), list) else tool_data.get('plateforme'),
                            commandes_courantes=json.dumps(tool_data.get('commandes_courantes', [])) if isinstance(
                                tool_data.get('commandes_courantes'), list) else tool_data.get('commandes_courantes'),
                            alternatives=json.dumps(tool_data.get('alternatives', [])) if isinstance(
                                tool_data.get('alternatives'), list) else tool_data.get('alternatives')
                        )
                        db.session.add(tool)
                    db.session.commit()
                    print(f"✅ {len(tools)} outils importés")
        except Exception as e:
            print(f"❌ Erreur import tools: {e}")

        # ============ IMPORT VULNERABILITIES ============
        try:
            if os.path.exists('data/vulnerabilities.json'):
                with open('data/vulnerabilities.json', 'r', encoding='utf-8') as f:
                    vulns = json.load(f)
                    for vuln_data in vulns:
                        vuln = Vulnerability(
                            cve=vuln_data.get('cve'),
                            titre=vuln_data.get('titre'),
                            description=vuln_data.get('description', ''),
                            severite=vuln_data.get('severite'),
                            score_cvss=vuln_data.get('score_cvss', 0.0),
                            mitigation=vuln_data.get('mitigation', ''),
                            plateforme=json.dumps(vuln_data.get('plateforme', [])) if isinstance(
                                vuln_data.get('plateforme'), list) else vuln_data.get('plateforme'),
                            date_decouverte=vuln_data.get('date_decouverte'),
                            date_correction=vuln_data.get('date_correction'),
                            commandes_test=json.dumps(vuln_data.get('commandes_test', [])) if isinstance(
                                vuln_data.get('commandes_test'), list) else vuln_data.get('commandes_test'),
                            ressources=vuln_data.get('ressources'),
                            tools=json.dumps(vuln_data.get('tools', [])) if isinstance(vuln_data.get('tools'),
                                                                                       list) else vuln_data.get('tools')
                        )
                        db.session.add(vuln)
                    db.session.commit()
                    print(f"✅ {len(vulns)} vulnérabilités importées")
        except Exception as e:
            print(f"❌ Erreur import vulnerabilities: {e}")

        # ============ IMPORT NOTES ============
        try:
            if os.path.exists('data/notes.json'):
                with open('data/notes.json', 'r', encoding='utf-8') as f:
                    notes = json.load(f)
                    for note_data in notes:
                        note = Note(
                            titre=note_data.get('titre'),
                            contenu=note_data.get('contenu', '')
                        )
                        db.session.add(note)
                    db.session.commit()
                    print(f"✅ {len(notes)} notes importées")
        except Exception as e:
            print(f"❌ Erreur import notes: {e}")

        print("\n" + "=" * 50)
        print("✅ ✅ ✅ Migration terminée avec succès ! ✅ ✅ ✅")
        print("=" * 50)


if __name__ == '__main__':
    migrate_json_to_database()
