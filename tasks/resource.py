from import_export import resources
from .models import Inmueble, Llamadas

class InmuebleResource(resources.ModelResource):
    class Meta:
        model = Inmueble
        # Puedes especificar campos adicionales o personalizar la importación aquí


class LlamadaResource(resources.ModelResource):
    class Meta:
        model = Llamadas
        # Puedes especificar campos adicionales o personalizar la importación aquí