from django import template

register = template.Library()

@register.filter
def join_names(procedures):
    return ", ".join(procedure.name for procedure in procedures)
