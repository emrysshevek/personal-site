import ast
import json
from django import template

register = template.Library()

@register.filter(name='to_dict')
def to_dict(value):
    print(json.loads(value))
    """Converts a string into a Python dictionary."""
    try:
        return json.loads(value)
    except (ValueError, TypeError):
        return {} # Return empty dict if parsing fails