from catalog.models import Product
import urllib
import json

def get_cart(request):
    try:
        cart = request.session['cart']
    except:
        cart = {}
    cart_list = []
    for i in cart.keys():
        el = {}
        if cart[i]!=0:
            el['product'] = Product.objects.get(id=i)
            el['count'] = int(cart[i])
            cart_list.append(el)
    return cart_list

def get_delivery_param(city_to, weight):
    city_from = 'city--blagoveshhensk'
    f=urllib.urlopen('http://emspost.ru/api/rest?callback=a&method=ems.calculate&from=%s&to=%s&weight=%s'%(city_from,city_to,weight))
    #json.loads(f.read())['a']
    #return f.read()
    son = json.loads(f.read()[2:-1])['rsp']
    return (son['price'],son['term']['min'],son['term']['max'])

    

