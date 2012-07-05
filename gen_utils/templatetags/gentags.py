from django import template

register = template.Library()

@register.filter
def replace_dashes(value):
    return value.replace('SELECT', 'REPLACED-SELECT')
replace_dashes.is_safe = True
