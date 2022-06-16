from typing import Dict

from django.db.models import AutoField
from django.shortcuts import render
import datetime
import json
from django.core import serializers
from django.http import HttpResponse
from .models import Products, Contact, Orders, OrderUpdate
from math import ceil


# Create your views here.
# shop view page
def index(request):
    products = Products.objects.all()

    # n= len(products)
    # nslides= n//4+ ceil((n/4)-(n//4))
    allProds = []

    catprods = Products.objects.values('category', 'id')

    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Products.objects.filter(category=cat)
        n = len(prod)
        nslides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nslides), nslides])
    # allProds= [[products, range(1,nslides), nslides],
    # [products, range(1,nslides), nslides]]
    params = {'allProds': allProds}
    # params= {'product': products, 'no_of_slides': nslides, 'range': range(1,nslides)}
    return render(request, 'shop/index.html', params)


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        message = request.POST.get('message', '')
        contact = Contact(name=name, email=email, phone=phone, message=message)
        contact.save()
    return render(request, 'shop/contact.html')


def search(request):
    return render(request, 'shop/search.html')


def prodview(request, myid):
    product = Products.objects.filter(id=myid)

    return render(request, 'shop/prodview.html', {'product': product[0]})


def checkout(request):
    # global thank, params
    if request.method == "POST":
        items_json = request.POST.get('itemsJson')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip', '')
        Orderphone = request.POST.get('phone', '')
        order = Orders(items_json=items_json, name=name, email=email, Orderphone=Orderphone, city=city, state=state,
                       address=address,
                       zip_code=zip_code)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The Order has been placed")
        update.save()
        thank = True
        order_id = order.order_id
        return render(request, 'shop/checkout.html', {'thank': thank, 'order_id': order_id})
    return render(request, 'shop/checkout.html')


def tracker(request):
    if request.method == "POST":
        order_id = request.POST.get('order_id', '')
        email = request.POST.get('email', '')
        # return HttpResponse(f"{order_id} and {email}")
        try:
            order = Orders.objects.filter(order_id=order_id, email=email)

            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=order_id)
                updates = []
                for item in update:
                    # str_timestamp= str(item.timestamp)
                    time = str(item.timestamp)
                    # time= item.timestamp
                    updates.append({'text': item.update_desc, 'time': time})

                    print(type(updates))
                    response = json.dumps([updates, order[0].items_json], default=str)
                    print(response)
                return HttpResponse(response)

            else:
                return HttpResponse('{erre}')
        except Exception as e:
            return HttpResponse(e)
    return render(request, 'shop/tracker.html')

# def tracker(request):
#     if request.method == "POST":
#         order_id = request.POST.get('order_id', '')
#         email = request.POST.get('email', '')
#         try:
#             order = Orders.objects.filter(order_id=order_id, email=email)
#             if len(order) > 0:
#                 update = OrderUpdate.objects.filter(order_id=order_id)
#                 updates = []
#                 for item in update:
#                     updates.append({'text': item.update_desc, 'time': item.timestamp})
#                     response = json.dumps(updates, default=str)
#                 return HttpResponse(response)
#             else:
#                 return HttpResponse('{}')
#         except Exception as e:
#             return HttpResponse('{}')
#
#     return render(request, 'shop/tracker.html')
    # return render(request, 'shop/tracker.html')
