from django import template
from django.template.loader import render_to_string


register = template.Library()

@register.simple_tag
def navbar(request):
    role = request.COOKIES.get('role')
    context = {'role': role}
    return render_to_string('navbar.html', context=context)

@register.simple_tag(takes_context=True)
def role_tag(context):
    request = context['request']
    role = request.COOKIES.get('role')
    # Ketika role mengandung kata "atlet", maka return teks "Atlet"
    if 'atlet' in role:
        return "Atlet"
    else:
        return role