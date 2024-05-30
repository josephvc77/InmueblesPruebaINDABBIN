from import_export import resources
from .models import DatosLlamadasInmuebles, Inmueble

class InmuebleResource(resources.ModelResource):
    class Meta:
        model = Inmueble
        # Puedes especificar campos adicionales o personalizar la importación aquí


class LlamadaResource(resources.ModelResource):
    class Meta:
        model = DatosLlamadasInmuebles
        # Puedes especificar campos adicionales o personalizar la importación aquí