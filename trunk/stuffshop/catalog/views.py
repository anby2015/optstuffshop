# Create your views here.
from django.http import HttpResponse
from catalog.models import *
from django.views.generic.simple import direct_to_template
from django import template
register = template.Library()

def main_page(request):
    new_products = Product.objects.all().order_by('date')[:6]
    special_products = Product.objects.filter(is_special=True)[:6]
    return direct_to_template(request, 'main_page.html', {'new_products': new_products, 'special_products':special_products})

def details(request, product_slug):
    product = Product.objects.get(slug=product_slug)
    menu_node_id = product.menu_node_id.id
    return direct_to_template(request, 'details.html', {'product': product, 'menu_node_id':menu_node_id})

def catalog(request, id):
    products = Product.objects.filter(menu_node_id=id)
    title = MenuNode.objects.get(id=id).name
    return direct_to_template(request, 'catalog.html', {'menu_node_id':int(id),'products':products,'title':title})




