from django.shortcuts import render, HttpResponse, redirect
from time import gmtime, strftime
import datetime
import random
import pytz
from django.utils import timezone
from users_app.models import Users


def index(request):
    users = Users.objects.all()
    context = {
        'request': request,
        'users': users,
    }
    print(context)
    return render(request, 'index.html', context)


def process(request):
    first_name = getSet(request, 'first_name')
    last_name = getSet(request, 'last_name')
    email_address = getSet(request, 'email_address')
    age = getSet(request, 'age')
    users = Users.objects.all()
    new_user = Users.objects.create(
        first_name=first_name,
        last_name=last_name,
        email_address=email_address,
        age=age
    )
    context = {
        'request': request,
        'users': users,
        'first_name': first_name,
        'last_name': last_name,
        'email_address': email_address,
        'age': age,
        'new_user': new_user,
    }
    print(context)
    return redirect('/')


def getSet(request, name):
    response = 0
    try:
        if request.POST[name]:
            response = request.POST[name]
            request.session[name] = response
    except:
        pass
    for key, value in request.session.items():
        if key == name:
            response = value

    return response
