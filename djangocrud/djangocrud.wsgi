import os
import sys

# Ajusta la ruta a la carpeta del proyecto
sys.path.append('/djangocrud/')

# Ajusta el entorno de Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'djangocrud.settings'

# Importa el módulo WSGI de Django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
