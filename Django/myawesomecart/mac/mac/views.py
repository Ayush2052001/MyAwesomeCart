from typing import Dict

from django.db.models import AutoField
from django.shortcuts import render
from django.http import HttpResponse
# from .models import Products, Contact, Orders
# from math import ceil


def index(request):
    # return render(request, 'index.html')
    return render(request, 'index.html')