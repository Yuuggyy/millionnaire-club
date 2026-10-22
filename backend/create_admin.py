import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@millionnaireclub.cd', os.environ.get('ADMIN_PASSWORD', 'MillionClubAdmin2026'))
    print('Superuser admin créé')
