-- Initialisation PostgreSQL - Minimal
-- Les tables seront créées par SQLAlchemy

-- Créer les extensions utiles
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- C'est tout ! Les indexes seront créés par migrate_json_to_db.py
