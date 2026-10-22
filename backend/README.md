# Backend Django — Millionaire Club Kinshasa Flipbook (Menu 3D StPageFlip)

Backend Django auto-hébergé pour le **menu interactif flipbook 3D du Millionaire Club Kinshasa**, basé sur le moteur StPageFlip. Servit en same-origin avec l'application frontend.

## Contenu & API
- `POST /api/submitOrder/` — Contrat exact : `{restaurant_slug, table_number, items:[{name, price, quantity}], special_notes}` → `{success: true, total: <float>}`
- `POST /api/callWaiter/` — Contrat exact : `{restaurant_slug, table_number}` → `{success: true}`
- `GET /api/stats/` — Statistiques des commandes et appels
- Panneau d'administration `/admin/` : gestion des commandes (statuts reçue → en_cours → terminée) et appels serveur.
- `frontend/` : Application flipbook 3D servie à la racine (`/`) same-origin.

## Lancer en local
```bash
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@millionnaireclub.cd', 'MillionClubAdmin2026')"
python3 manage.py runserver 8000
```
- Le menu est servi sur : `http://127.0.0.1:8000/`
- Administration Django : `http://127.0.0.1:8000/admin/` (Identifiants : `admin` / `MillionClubAdmin2026`)

## Slug du restaurant
- Slug par défaut : `millionnaire`

## Déploiement VPS (Production)
```bash
pip install gunicorn
gunicorn config.wsgi --bind 127.0.0.1:8000 --workers 3
```
Nginx sert le reverse proxy vers Gunicorn.
<<<<<<< HEAD

## Déploiement express sur Render (gratuit, admin public en 5 minutes)

1. Crée un compte sur https://render.com avec ton GitHub (bouton "Sign in with GitHub")
2. New + → "Web Service" → choisis le repo `Yuuggyy/millionnaire-club` → dossier racine : `backend`
   (ou pousse le dossier backend dans son propre repo)
3. Render lit le `render.yaml` inclus : build et commande sont déjà configurés
4. Dans "Environment", ajoute : `ADMIN_PASSWORD` = ton mot de passe admin (défaut : MillionClubAdmin2026)
5. Deploy → tu obtiens une URL `https://xxx.onrender.com` → l'admin est sur `https://xxx.onrender.com/admin/`
   et le front avec commandes en ligne est servi sur `https://xxx.onrender.com/`

Note : l'offre gratuite s'endort après ~15 min d'inactivité (première visite = ~30s de réveil).
=======
>>>>>>> aeacd5e (Logo officiel du club : filigrane doré sur le papier du menu + logo en couverture (design épuré))
