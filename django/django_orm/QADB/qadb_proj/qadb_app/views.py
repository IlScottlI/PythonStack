from django.shortcuts import render, redirect
from .models import QADB

# Create your views here.


def index(request):
    ul = []
    context = {
        'dojos': [],
        'ninjas': [],
        'ul': ul,
    }
    print(context)
    return render(request, 'index.html', context)
