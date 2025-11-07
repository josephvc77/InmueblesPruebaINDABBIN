# inicio/context_processors.py
from django.conf import settings

def app_version(request):
    """
    Context processor para hacer disponible APP_VERSION en todos los templates.
    Lee la versión desde settings.APP_VERSION que a su vez la lee del .env
    """
    version = getattr(settings, 'APP_VERSION', '1.0.17')
    return {
        'APP_VERSION': version
    }
