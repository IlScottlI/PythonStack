from django.shortcuts import render, redirect
from .models import Show
from django.contrib import messages


def shows(request):
    context = {
        'shows': Show.objects.all()
    }
    return render(request, 'shows.html', context)


def new(request):
    return render(request, 'new.html')


def view(request, show_id):
    context = {
        'show_id': show_id,
        'show_obj': Show.objects.get(id=show_id),
    }
    return render(request, 'view.html', context)


def destroy(request, show_id):
    Show.objects.get(id=show_id).delete()
    messages.success(request, "Show was Successfully Deleted")
    return redirect('/shows')


def edit(request, show_id):
    context = {
        'show_id': show_id,
        'show_obj': Show.objects.get(id=show_id),
        'show_rel_date': Show.objects.get(id=show_id).release_date.strftime("%Y-%m-%d")
    }
    return render(request, 'edit.html', context)


def process(request):
    action = redirect('/shows')
    type_ = request.POST['type']

    if type_ == 'new':
        action = newForm(request)
    if type_ == 'update':
        show_id = getSet(request, 'show_id')
        action = updateForm(request, show_id)
    return action


def getSet(request, name):
    response = None
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


def updateForm(request, id):
    errors = Show.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        action = redirect(f"/shows/{id}/edit")
        return action
    else:
        if len(request.POST['description']) > 0:
            description = request.POST['description']
        else:
            description = ''
        show_to_update = Show.objects.get(id=id)
        show_to_update.title = getSet(request, 'title')
        show_to_update.network = getSet(request, 'network')
        show_to_update.release_date = getSet(request, 'release_date')
        show_to_update.description = description
        show_to_update.save()
        messages.success(request, "Show Successfully Updated")
        action = redirect(f"/shows/{id}")
        return action


def newForm(request):
    errors = Show.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():

            messages.error(request, value)
        action = redirect(f"/shows/new")
        return action
    else:
        messages.success(request, "Show Successfully Created")
        # redirect to a success route
        newItem = Show.objects.create(
            title=getSet(request, 'title'),
            network=getSet(request, 'network'),
            release_date=getSet(request, 'release_date'),
            description=getSet(request, 'description'),
        )
        action = redirect(f"/shows/{newItem.id}")
        return action
