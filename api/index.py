import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'babuclinic.settings')

import django

django.setup()

# Ensure database tables exist on serverless deploys (no-op if already migrated)
try:
    from django.core.management import call_command
    call_command('migrate', run_syncdb=True, verbosity=0)
except Exception as e:
    print(f'Migration check skipped: {e}')

from django.core.wsgi import get_wsgi_application

app = get_wsgi_application()
