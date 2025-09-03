from import_export import resources
from .models import DatosLlamadasInmuebles, Inmueble

class InmuebleResource(resources.ModelResource):
    class Meta:
        model = Inmueble
        import_id_fields = ('rfi',)   # campo único en tu modelo
        fields = ('rfi', 'NombreInmueble', 'estado', 'telefono', 'direccion')
        skip_unchanged = True
        report_skipped = True



class LlamadaResource(resources.ModelResource):
    class Meta:
        model = DatosLlamadasInmuebles
        # Puedes especificar campos adicionales o personalizar la importación aquí