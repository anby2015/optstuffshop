# -*- coding: utf-8 -*-
# Create your views here.
from django.http import HttpResponse
from catalog.models import *
from django.views.generic.simple import direct_to_template
from django import template
from catalog.utils import get_cart, get_delivery_param


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
    menu_ids = [ x.id for x in MenuNode.objects.get(id=id).get_descendants()]
    products = Product.objects.filter(menu_node_id__in=menu_ids)
    title = MenuNode.objects.get(id=id).name
    return direct_to_template(request, 'catalog.html', {'menu_node_id':int(id),'products':products,'title':title,'filter_form':PhoneForm})

def search(request):
    products = Product.objects.filter(title__contains=request.GET['search'])
    title = u'Поиск по запросу: %s' % (request.GET['search'])
    return direct_to_template(request, 'catalog.html', {'products':products,'title':title})



#have no fucking idea how it works
#do not touch!!
def ajax(request):
    try:
        cart = request.session['cart']
    except:
        cart = {}
    if(request.GET['action']=='cart_show'):
        cart_list = get_cart(request)
        product_price = 0
        weight = 0
        shipping_price = 0
        for el in cart_list:
            product_price += el['product'].cast().get_price()*el['count']
            weight += el['product'].cast().weight*el['count']
        shipping_price = 0#get_delivery_param(request.COOKIES['city'],weight)[0]
        return direct_to_template(request, 'cart.html',{
            'cart_list': cart_list,
            'product_price':product_price,
            'shipping_price':shipping_price,
            'total_price':int(shipping_price)+int(product_price),
            })
    if(request.GET['action']=='cart_add'):
        product_id = request.GET['product_id']
        new_id = -1
        try:
            cart[product_id] += 1
        except:
            cart[product_id] = 1
        if cart[product_id] == 1: new_id = product_id
        request.session['cart'] = cart
        return HttpResponse(new_id)
    if(request.GET['action']=='cart_del'):
        product_id = request.GET['product_id']
        if(cart[product_id]<=1):
            cart[product_id] = 0
        else:
            cart[product_id] -= 1
        request.session['cart'] = cart
        return HttpResponse('ok')






