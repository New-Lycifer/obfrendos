from django import template

register = template.Library()

@register.filter(name='bold_label')
def bold_label(field):
    return field.label_tag(attrs={'class': 'strong'})