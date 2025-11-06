import csv
import json
import sys
from app import app, db
from models import Command, Tool, Certification, Vulnerability, CheatSheet, Note, Badge

TABLES = {
    'command': Command,
    'tool': Tool,
    'certification': Certification,
    'cheatsheet': CheatSheet,
    'vulnerability': Vulnerability,
    'note': Note,
    'badge': Badge
}

def import_json(table_name, json_file):
    table_cls = TABLES[table_name]
    with app.app_context():
        with open(json_file, encoding="utf-8") as f:
            data = json.load(f)
            count = 0
            for item in data:
                unique_field = 'nom' if hasattr(table_cls, 'nom') else 'titre'
                value = item.get(unique_field)
                if not value:
                    continue
                query = {unique_field: value}
                exists = table_cls.query.filter_by(**query).first()
                if not exists:
                    obj = table_cls(**{k: v for k, v in item.items() if hasattr(table_cls, k)})
                    db.session.add(obj)
                    count += 1
            db.session.commit()
            print(f"✅ {count} éléments importés dans {table_name} depuis JSON : {json_file}")

def import_csv(table_name, csv_file):
    table_cls = TABLES[table_name]
    with app.app_context():
        with open(csv_file, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                unique_field = 'nom' if hasattr(table_cls, 'nom') else 'titre'
                value = row.get(unique_field)
                if not value:
                    continue
                query = {unique_field: value}
                exists = table_cls.query.filter_by(**query).first()
                if not exists:
                    obj = table_cls(**{k: v for k, v in row.items() if hasattr(table_cls, k)})
                    db.session.add(obj)
                    count += 1
            db.session.commit()
            print(f"✅ {count} éléments importés dans {table_name} depuis CSV : {csv_file}")

if __name__ == '__main__':
    if len(sys.argv) != 4 or sys.argv[1] not in {"json", "csv"} or sys.argv[2] not in TABLES:
        print("Usage: python import_any_dataset.py [json|csv] [command|tool|certification|cheatsheet|vulnerability|note|badge] <file>")
        sys.exit(1)
    mode, table, file = sys.argv[1], sys.argv[2], sys.argv[3]
    if mode == "json":
        import_json(table, file)
    else:
        import_csv(table, file)
