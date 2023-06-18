from django import template

register = template.Library()

@register.filter
def get_id(value):
    return value.get('id')

@register.filter
def get_role(value):
    return value.get('role')


@register.filter
def get_error(value):
    return value.get('error')

