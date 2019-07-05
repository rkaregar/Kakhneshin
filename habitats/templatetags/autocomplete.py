from django import template
from django.template.loader import render_to_string

register = template.Library()


@register.simple_tag
def divisions_autocomplete_input(only_cities=True):
    context = {
        'only_cities': 'true' if only_cities else 'false',
    }
    return render_to_string('geographic_division/input.html', context=context)
