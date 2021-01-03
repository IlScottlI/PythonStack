from django.shortcuts import render, redirect
from .models import Dojo, Ninja, Sector

# Create your views here.


def index(request):
    ul = []
    for item in Dojo.objects.all():
        try:
            ul.append({'ninjas': Ninja.objects.filter(
                dojo_id=Dojo.objects.get(id=item.id)), 'dojo': item.name, 'id': item.id})
        except:
            pass
        context = {
            'dojos': [],
            'ninjas': [],
            'ul': ul,
        }
    print(context)
    return render(request, 'qadb.html', context)


def process(request):
    if getSet(request, 'type') == 'dojo':
        context = {
            'name': getSet(request, 'name'),
            'city': getSet(request, 'city'),
            'state': getSet(request, 'state'),
        }
        print(context)
        try:
            insertRow(request, 'dojo')
        except:
            print('Insert Dojo Failed')
    elif getSet(request, 'type') == 'ninja':
        context = {
            'first_name': getSet(request, 'first_name'),
            'last_name': getSet(request, 'last_name'),
            'dogo_id': getSet(request, 'dojo_id'),
        }
        try:
            insertRow(request, 'ninja')
        except:
            print('Insert Ninja Failed')
    return redirect('/')


def insertRow(request, model):
    if model == 'dojo':
        newly_created_dojo = Dojo(
            name=getSet(request, 'name'),
            city=getSet(request, 'city'),
            state=getSet(request, 'state')
        )
        newly_created_dojo.save()
    elif model == 'ninja':
        newly_created_ninja = Ninja(
            first_name=getSet(request, 'first_name'),
            last_name=getSet(request, 'last_name'),
            dojo_id=Dojo.objects.get(id=getSet(request, 'dojo_id'))
        )
        newly_created_ninja.save()
    return


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
