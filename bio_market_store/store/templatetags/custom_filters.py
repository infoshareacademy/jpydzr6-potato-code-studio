from django import template

register = template.Library()

@register.filter(name='mul')
def mul(value, arg):
    """
    Multiplies the value by the argument.
    Usage in template: {{ value|mul:arg }}
    """
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return ''