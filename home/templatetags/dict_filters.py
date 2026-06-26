import ast
import json
from django import template

register = template.Library()

@register.filter(name='to_dict')
def to_dict(value):
    """Converts a string into a Python dictionary."""
    try:
        return json.loads(value)
    except (ValueError, TypeError) as e:
        print(e)
        print(value)
        return {} # Return empty dict if parsing fails