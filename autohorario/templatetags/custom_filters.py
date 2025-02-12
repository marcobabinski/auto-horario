from django import template

register = template.Library()

@register.filter(name='get')
def get(dictionary, key):
    return dictionary.get(key)

@register.filter
def index(sequence, position):
    try:
        return sequence[position]
    except (IndexError, TypeError):
        return None

