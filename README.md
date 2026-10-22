# Millionaire Club Kinshasa — Menu Flipbook 3D & Backend Django

Projet complet pour le **Millionaire Club** (Kinshasa, RDC), comprenant un frontend menu flipbook 3D StPageFlip stabilisé et un backend Django d'administration et de gestion des commandes.

## 🌟 Démo en ligne (Surge)
- **Front-end Flipbook 3D (Démo Surge)** : [https://millionnaire-club.surge.sh](https://millionnaire-club.surge.sh)

## 📁 Structure du Projet
```
millionnaire-club/
├── frontend/               # Menu Flipbook 3D StPageFlip
│   ├── index.html          # Interface flipbook 3D, panier et commandes
│   ├── page-flip.browser.min.js  # Moteur StPageFlip 3D
│   └── 404.html            # Redirection SPA pour hébergeurs statiques
├── backend/                # API REST & Admin Django
│   ├── manage.py
│   ├── requirements.txt
│   ├── config/             # Configuration Django (settings, urls, wsgi)
│   ├── menuapp/            # App backend (models, views, admin, migrations)
│   └── frontend/           # Copie du front pour service same-origin Django
├── .gitignore
└── README.md
```

## ✨ Caractéristiques Frontend (Flipbook 3D)
- Moteur StPageFlip 3D stabilisé avec effet page-curl tactile et souris.
- Branding luxueux aux couleurs du Millionaire Club Kinshasa (`#0D0D0D`, `#D4AF37`, `#F8F9FA`).
- Catégories complètes : Signatures du Club, Grillades & Viandes, Fruits de Mer & Tapas, Cocktails Signatures, Champagnes & Spiritueux, Boissons & Softs, Desserts Prestige.
- Injection directe et idempotente des boutons d'ajout au panier avec gestion propre des événements (`stopPropagation`).
- Panier dynamique et système de commande avec repli automatique en `localStorage` si hors ligne.
- Footer obligatoire : *Inspire by YuuStore* lié au `+243 977 555 768`.

## ⚙️ Backend Django & Contrat API
- **Admin Django** : `/admin/` (gestion des commandes et appels serveur).
- **Endpoint Commande** : `POST /api/submitOrder/`
  - Body payload : `{"restaurant_slug": "millionnaire", "table_number": "7", "items": [{"name": "...", "price": 45, "quantity": 1}], "special_notes": "..."}`
  - Réponse contrat : `{"success": true, "total": 45.0, "id": 1}`
- **Endpoint Appel Serveur** : `POST /api/callWaiter/`
  - Body payload : `{"restaurant_slug": "millionnaire", "table_number": "7"}`
  - Réponse contrat : `{"success": true}`

## 🚀 Déploiement Production Gunicorn / Nginx sur VPS

### 1. Installation des dépendances & venv
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt gunicorn
```

### 2. Migrations et Collectstatic
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 3. Configuration Systemd (Gunicorn)
Fichier `/etc/systemd/system/millionnaire.service` :
```ini
[Unit]
Description=Gunicorn daemon for Millionaire Club Django
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/millionnaire-club/backend
ExecStart=/var/www/millionnaire-club/backend/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 config.wsgi:application

[Install]
WantedBy=multi-user.target
```

### 4. Configuration Nginx
Fichier `/etc/nginx/sites-available/millionnaire-club` :
```nginx
server {
    listen 80;
    server_name millionnaire.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /var/www/millionnaire-club/backend/staticfiles/;
    }
}
```
Activer et recharger Nginx :
```bash
ln -s /etc/nginx/sites-available/millionnaire-club /etc/nginx/sites-enabled/
systemctl restart gunicorn
systemctl restart nginx
```

## 📄 Licence
Développé par **Guy Muzongo (Yuuggyy)** pour le Millionaire Club Kinshasa.
