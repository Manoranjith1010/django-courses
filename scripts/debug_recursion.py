import django, os, sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE','courseproject.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser
from apps.courses.views import index

sys.setrecursionlimit(80)
factory = RequestFactory()
req = factory.get('/')
req.user = AnonymousUser()

try:
    resp = index(req)
    print('OK', resp.status_code)
except RecursionError as e:
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("=== LAST 25 FRAMES ===")
    for frame in tb[-25:]:
        print(f'{frame.filename.split("django-courses")[-1]}:{frame.lineno} in {frame.name}')
        print('   ', frame.line)
except Exception as e:
    import traceback
    traceback.print_exc()
