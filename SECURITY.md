# 🔒 Guide de Sécurité - CyberSec Command Manager

## Configuration Initiale

### 1. Variables d'Environnement

Copiez le fichier d'exemple:
```bash
cp .env.example .env
```

Générez des secrets forts avec PowerShell:
```powershell
# Mot de passe PostgreSQL (32 caractères)
$pgPass = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | ForEach-Object {[char]$_})
Write-Host "POSTGRES_PASSWORD=$pgPass"

# Secret Key Flask (64 caractères hexa)
$secret = -join ((48..57) + (97..102) | Get-Random -Count 64 | ForEach-Object {[char]$_})
Write-Host "SECRET_KEY=$secret"

# Mot de passe PgAdmin (24 caractères)
$adminPass = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 24 | ForEach-Object {[char]$_})
Write-Host "PGADMIN_DEFAULT_PASSWORD=$adminPass"
```

### 2. Fichiers à NE JAMAIS Commiter

- `.env` (contient les secrets)
- `pgdata/` (données de la base)
- `backups/` (sauvegardes sensibles)

### 3. Bonnes Pratiques

✅ Toujours utiliser des mots de passe forts (32+ caractères)
✅ Changer tous les secrets par défaut
✅ Utiliser HTTPS en production
✅ Limiter l'accès réseau aux conteneurs
✅ Sauvegarder régulièrement les données
✅ Mettre à jour les dépendances

❌ Ne jamais commiter le fichier `.env`
❌ Ne pas utiliser les secrets d'exemple
❌ Ne pas exposer PgAdmin publiquement
❌ Ne pas activer FLASK_DEBUG en production

## Déploiement Production

1. **Configurez un pare-feu** pour limiter l'accès
2. **Utilisez un reverse proxy** (Nginx/Traefik) avec SSL
3. **Activez les logs** pour l'audit
4. **Surveillez les vulnérabilités** des dépendances
5. **Sauvegardez** quotidiennement

## Audit de Sécurité

Vérifiez périodiquement:
```bash
# Secrets non committés
git log --all -S "POSTGRES_PASSWORD"

# Permissions des fichiers
ls -la .env

# Ports exposés
docker-compose ps
```
