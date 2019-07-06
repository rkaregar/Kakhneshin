from django import template
from django.template.loader import render_to_string

register = template.Library()


@register.simple_tag
def divisions_autocomplete_input(only_cities=True, default_value='', default_value_name='', field_name='division',
                                 errors=''):
    context = {
        'only_cities': 'true' if only_cities else 'false',
        'default_value': default_value,
        'default_value_name': default_value_name,
        'field_name': field_name,
        'input_class': 'is-invalid' if errors else ''
    }
    return render_to_string('geographic_division/input.html', context=context)
