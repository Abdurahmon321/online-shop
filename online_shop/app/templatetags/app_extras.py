from django import template
from ..models import Category, Product
register = template.Library()


@register.simple_tag
def all_categories():
    return Category.objects.all()


@register.simple_tag
def all_products():
    return Product.objects.all().order_by('-date_time')


@register.simple_tag
def products_comment_by_id(id):
    return Product.objects.filter(pk=id)


