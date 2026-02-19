import os
import sys
# Ensure project path is on sys.path
sys.path.insert(0, r'd:\p\e-learning_project_django\django-courses')
os.environ.setdefault('DJANGO_SETTINGS_MODULE','courseproject.settings')
import django
django.setup()
from django.template.loader import get_template
try:
    t = get_template('account/base.html')
    print('Loaded account/base.html')
except Exception as e:
    print('ERROR:', e)
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','courseproject.settings')
import django
django.setup()
from django.template.loader import get_template
try:
    t = get_template('account/base.html')
    print('Loaded:', t.template.name if hasattr(t, 'template') else 'account/base.html')
except Exception as e:
    print('ERROR:', e)
