from django import template
import os

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Obtiene un valor de un diccionario por su clave"""
    if dictionary is None:
        return None
    return dictionary.get(key)

@register.filter
def get_attr(obj, attr_name):
    """Devuelve el valor de un campo de un objeto por nombre"""
    if obj is None:
        return None
    return getattr(obj, attr_name, None)

@register.filter
def get_file_icon(filename):
    """Retorna el icono de Bootstrap Icons según la extensión del archivo"""
    if not filename:
        return 'bi-file-earmark-fill'
    
    ext = filename.lower().split('.')[-1] if '.' in filename else ''
    
    icon_map = {
        'pdf': 'bi-file-earmark-pdf-fill',
        'doc': 'bi-file-earmark-word-fill',
        'docx': 'bi-file-earmark-word-fill',
        'xls': 'bi-file-earmark-excel-fill',
        'xlsx': 'bi-file-earmark-excel-fill',
        'jpg': 'bi-file-earmark-image-fill',
        'jpeg': 'bi-file-earmark-image-fill',
        'png': 'bi-file-earmark-image-fill',
        'gif': 'bi-file-earmark-image-fill',
        'zip': 'bi-file-earmark-zip-fill',
        'rar': 'bi-file-earmark-zip-fill',
    }
    
    return icon_map.get(ext, 'bi-file-earmark-fill')

@register.filter
def split(value, arg):
    """Divide una cadena por un delimitador"""
    if value is None:
        return []
    return str(value).split(arg)

