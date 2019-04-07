from blog import models
from django import template

register = template.Library()


@register.simple_tag
def get_recent_posts(num=5):
    return models.Post.objects.all().order_by('-created_time')[:num]


@register.simple_tag
def archives():
    return models.Post.objects.dates('created_time', 'month', order='DESC')


@register.simple_tag
def get_categories():
    return models.Category.objects.all()

