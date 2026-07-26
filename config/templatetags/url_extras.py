from django import template
from django.urls import reverse, NoReverseMatch

register = template.Library()

@register.simple_tag
def safe_url(name):
    if not name:
        return "#"
    try:
        return reverse(name)
    except NoReverseMatch:
        return "#"

@register.filter
def get_item(dictionary, key):
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None

@register.filter
def get_item_tuple(dictionary, args):
    """
    usage:
    perm_dict|get_item_tuple:"1,5"
    """
    try:
        role_id, submenu_id = args.split(",")
        return dictionary.get((int(role_id), int(submenu_id)))
    except:
        return None