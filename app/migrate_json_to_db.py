import json
import os
from app import app, db
from models import Command, Certification, CheatSheet, Tool, Vulnerability, Note


def migrate_json_to_database():
    """Migrate toutes les données JSON vers PostgreSQL (SANS supprimer les données existantes)"""
    
    with app.app_context():
        print("\n" + "=" * 60)
        print("🚀 MIGRATION DES DONNÉES JSON VERS POSTGRESQL")
        print("=" * 60 + "\n")
        
        # ============ VÉRIFIER SI DÉJÀ IMPORTÉ ============
        existing_commands = Command.query.count()
        existing_tools = Tool.query.count()
        existing_cve = Vulnerability.query.count()
        
        if existing_commands > 0 or existing_tools > 0 or existing_cve > 0:
            print("✅ Données déjà présentes dans la base")
            print(f"   - Commandes: {existing_commands}")
            print(f"   - Outils: {existing_tools}")
            print(f"   - CVE: {existing_cve}")
            print(f"   - Notes: {Note.query.count()}")
            print("\n⏭️  Import ignoré (données déjà chargées)\n")
            return

        print("📊 Base de données vide, import des données JSON...\n")

        # ============ IMPORT COMMANDS (un par un) ============
        print("📦 Import des COMMANDES...")
        imported_commands = 0
        failed_commands = 0
        try:
            if os.path.exists('data/commands.json'):
                with open('data/commands.json', 'r', encoding='utf-8') as f:
                    commands = json.load(f)
                    for cmd_data in commands:
                        try:
                            # Vérifier si la commande existe déjà
                            existing = Command.query.filter_by(nom=cmd_data.get('nom')).first()
                            if existing:
                                continue
                            
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
                            imported_commands += 1
                        except Exception as e:
                            db.session.rollback()
                            failed_commands += 1
                            # Masquer les erreurs de duplicates
                            if 'duplicate' not in str(e).lower():
                                print(f"   ⚠️  Erreur pour '{cmd_data.get('nom')}': {str(e)[:80]}")
                    
                    print(f"   ✅ {imported_commands} commandes importées, {failed_commands} ignorées")
            else:
                print("   ⚠️  Fichier data/commands.json introuvable")
        except Exception as e:
            print(f"   ❌ Erreur générale: {e}")


        # ============ IMPORT CERTIFICATIONS ============
        print("\n📦 Import des CERTIFICATIONS...")
        try:
            if os.path.exists('data/certifications.json'):
                with open('data/certifications.json', 'r', encoding='utf-8') as f:
                    certs = json.load(f)
                    imported_certs = 0
                    for cert_data in certs:
                        # Vérifier si existe déjà
                        existing = Certification.query.filter_by(nom=cert_data.get('nom')).first()
                        if existing:
                            continue
                            
                        cert = Certification(
                            nom=cert_data.get('nom'),
                            organisme=cert_data.get('organisme'),
                            description=cert_data.get('description'),
                            niveau=cert_data.get('niveau'),
                            prix_usd=cert_data.get('prix_usd', 0),
                            duree_validite=cert_data.get('duree_validite', 36),
                            duree_etude=cert_data.get('duree_etude'),
                            domaines=json.dumps(cert_data.get('domaines', [])) if isinstance(cert_data.get('domaines'), list) else cert_data.get('domaines'),
                            commandes_recommandees=json.dumps(cert_data.get('commandes_recommandees', [])) if isinstance(cert_data.get('commandes_recommandees'), list) else cert_data.get('commandes_recommandees'),
                            prerequisites=cert_data.get('prerequisites'),
                            lien=cert_data.get('lien')
                        )
                        db.session.add(cert)
                        imported_certs += 1
                    db.session.commit()
                    print(f"   ✅ {imported_certs} certifications importées")
            else:
                print("   ⚠️  Fichier data/certifications.json introuvable")
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
            db.session.rollback()


        # ============ IMPORT CHEATSHEETS ============
        print("\n📦 Import des CHEAT SHEETS...")
        try:
            if os.path.exists('data/cheatsheets.json'):
                with open('data/cheatsheets.json', 'r', encoding='utf-8') as f:
                    sheets = json.load(f)
                    imported_sheets = 0
                    for sheet_data in sheets:
                        existing = CheatSheet.query.filter_by(titre=sheet_data.get('titre')).first()
                        if existing:
                            continue
                            
                        sheet = CheatSheet(
                            titre=sheet_data.get('titre'),
                            description=sheet_data.get('description'),
                            categorie=sheet_data.get('categorie'),
                            niveau=sheet_data.get('niveau'),
                            contenu=sheet_data.get('contenu', ''),
                            commandes=json.dumps(sheet_data.get('commandes', [])) if isinstance(sheet_data.get('commandes'), list) else sheet_data.get('commandes'),
                            ressources=sheet_data.get('ressources', '')
                        )
                        db.session.add(sheet)
                        imported_sheets += 1
                    db.session.commit()
                    print(f"   ✅ {imported_sheets} cheat sheets importées")
            else:
                print("   ⚠️  Fichier data/cheatsheets.json introuvable")
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
            db.session.rollback()


        # ============ IMPORT TOOLS ============
        print("\n📦 Import des OUTILS...")
        try:
            if os.path.exists('data/tools.json'):
                with open('data/tools.json', 'r', encoding='utf-8') as f:
                    tools = json.load(f)
                    imported_tools = 0
                    for tool_data in tools:
                        existing = Tool.query.filter_by(nom=tool_data.get('nom')).first()
                        if existing:
                            continue
                            
                        tool = Tool(
                            nom=tool_data.get('nom'),
                            description=tool_data.get('description'),
                            categorie=tool_data.get('categorie'),
                            type=tool_data.get('type'),
                            installation=tool_data.get('installation'),
                            documentation=tool_data.get('documentation'),
                            prix=tool_data.get('prix', 'Gratuit'),
                            plateforme=json.dumps(tool_data.get('plateforme', [])) if isinstance(tool_data.get('plateforme'), list) else tool_data.get('plateforme'),
                            commandes_courantes=json.dumps(tool_data.get('commandes_courantes', [])) if isinstance(tool_data.get('commandes_courantes'), list) else tool_data.get('commandes_courantes'),
                            alternatives=json.dumps(tool_data.get('alternatives', [])) if isinstance(tool_data.get('alternatives'), list) else tool_data.get('alternatives')
                        )
                        db.session.add(tool)
                        imported_tools += 1
                    db.session.commit()
                    print(f"   ✅ {imported_tools} outils importés")
            else:
                print("   ⚠️  Fichier data/tools.json introuvable")
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
            db.session.rollback()


        # ============ IMPORT VULNERABILITIES ============
        print("\n📦 Import des VULNÉRABILITÉS...")
        try:
            if os.path.exists('data/vulnerabilities.json'):
                with open('data/vulnerabilities.json', 'r', encoding='utf-8') as f:
                    vulns = json.load(f)
                    imported_vulns = 0
                    for vuln_data in vulns:
                        existing = Vulnerability.query.filter_by(cve=vuln_data.get('cve')).first()
                        if existing:
                            continue
                            
                        vuln = Vulnerability(
                            cve=vuln_data.get('cve'),
                            titre=vuln_data.get('titre'),
                            description=vuln_data.get('description', ''),
                            severite=vuln_data.get('severite'),
                            score_cvss=vuln_data.get('score_cvss', 0.0),
                            mitigation=vuln_data.get('mitigation', ''),
                            plateforme=json.dumps(vuln_data.get('plateforme', [])) if isinstance(vuln_data.get('plateforme'), list) else vuln_data.get('plateforme'),
                            date_decouverte=vuln_data.get('date_decouverte'),
                            date_correction=vuln_data.get('date_correction'),
                            commandes_test=json.dumps(vuln_data.get('commandes_test', [])) if isinstance(vuln_data.get('commandes_test'), list) else vuln_data.get('commandes_test'),
                            ressources=vuln_data.get('ressources'),
                            tools=json.dumps(vuln_data.get('tools', [])) if isinstance(vuln_data.get('tools'), list) else vuln_data.get('tools')
                        )
                        db.session.add(vuln)
                        imported_vulns += 1
                    db.session.commit()
                    print(f"   ✅ {imported_vulns} vulnérabilités importées")
            else:
                print("   ⚠️  Fichier data/vulnerabilities.json introuvable")
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
            db.session.rollback()


        # ============ NE PAS IMPORTER LES NOTES ============
        # Les notes sont créées par l'utilisateur uniquement
        print("\n📝 Notes : créées uniquement par l'utilisateur (non importées)")


        # ============ RÉSUMÉ ============
        print("\n" + "=" * 60)
        print("✅ ✅ ✅  MIGRATION TERMINÉE AVEC SUCCÈS  ✅ ✅ ✅")
        print("=" * 60)
        
        # Afficher les statistiques finales
        print("\n📊 Statistiques finales:")
        print(f"   • Commandes: {Command.query.count()}")
        print(f"   • Certifications: {Certification.query.count()}")
        print(f"   • Cheat Sheets: {CheatSheet.query.count()}")
        print(f"   • Outils: {Tool.query.count()}")
        print(f"   • Vulnérabilités: {Vulnerability.query.count()}")
        print(f"   • Notes: {Note.query.count()}")
        print()


if __name__ == '__main__':
    migrate_json_to_database()
