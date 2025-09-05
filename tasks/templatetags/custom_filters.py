from django import template

register = template.Library()

@register.filter
def get_attr(obj, attr_name):
    """Devuelve el valor de un campo de un objeto por nombre."""
    return getattr(obj, attr_name, "")
