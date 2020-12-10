
from django.shortcuts import render, HttpResponse, redirect

# Create your views here.


def index(request):
    setpoint = getSetPoint(request)
    counter = getCounter(request)
    if counter > 0:
        increaseCount(request)
    else:
        request.session['counter'] = setpoint

    context = {
        'session': request.session,

    }
    return render(request, 'index.html', context)


def destroy_session(request):
    try:
        del request.session['counter']
    except:
        pass
    try:
        del request.session['setpoint']
    except:
        pass

    return redirect('/')


def plus_two(request):
    try:
        if request.session['counter'] > 0:
            request.session['counter'] += 1
    except:
        request.session['counter'] = 1

    return redirect('/')


def setIncrement(request):
    request.session['useSetpoint'] = True
    try:
        request.session['setpoint'] = request.POST['setpoint']
    except:
        pass
    return redirect('/')


def getSetPoint(request):
    setpoint = 1
    try:
        setpoint = request.session['setpoint']
    except:
        request.session['setpoint'] = 1
    return setpoint


def getCounter(request):
    counter = 0
    try:
        counter = request.session['counter']
    except:
        request.session['counter'] = counter
    return counter


def increaseCount(request):
    counter = 1
    setpoint = 1
    try:
        setpoint = request.session['setpoint']
        counter = request.session['counter']
        print(counter, setpoint)
        try:
            request.session['counter'] = int(counter) + int(setpoint)
        except:
            pass
    except:
        print(counter, setpoint)
    return None
