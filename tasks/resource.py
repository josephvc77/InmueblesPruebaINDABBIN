from import_export import resources
from .models import Inmueble

class InmuebleResource(resources.ModelResource):
    class Meta:
        model = Inmueble
        # Puedes especificar campos adicionales o personalizar la importación aquí
