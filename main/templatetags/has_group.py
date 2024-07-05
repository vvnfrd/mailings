from django import template

from main.models import Mailing, Client

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.filter
def media_filter(path):
    if path:
        return f'/media/{path}'
    else:
        return '#'


@register.filter(name='total_mailings')
def total_mailings(trash):
    trash = trash
    return len(Mailing.objects.all())


@register.filter(name='active_mailings')
def active_mailings(trash):
    trash = trash
    return len(Mailing.objects.filter(status=True))


@register.filter(name='client_count')
def client_count(trash):
    trash = trash
    return len(Client.objects.all())