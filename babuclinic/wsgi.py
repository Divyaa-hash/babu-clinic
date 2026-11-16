"""
WSGI config for babuclinic project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'babuclinic.settings')

application = get_wsgi_application()

# Ensure database tables exist on serverless deploys (no-op if already migrated)
try:
    from django.core.management import call_command
    call_command('migrate', run_syncdb=True, verbosity=0)
except Exception as e:
    print(f'Migration check skipped: {e}')
