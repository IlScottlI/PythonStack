from django.shortcuts import render, HttpResponse, redirect
from time import gmtime, strftime
import datetime
import random
import pytz
from django.utils import timezone


def index(request):
    # request.session.clear()
    type_ = getSet(request, 'type')
    farmGold = getSet(request, 'farmGold')
    caveGold = getSet(request, 'caveGold')
    houseGold = getSet(request, 'houseGold')
    casinoGold = getSet(request, 'casinoGold')
    log = getSetLog(request)
    try:
        total = farmGold + caveGold + houseGold + casinoGold
    except:
        pass
    context = {
        'request': request,
        'type': type_,
        'farmGold': farmGold,
        'caveGold': caveGold,
        'houseGold': houseGold,
        'casinoGold': casinoGold,
        'log': log,
        'total': total,
    }
    print(context)
    return render(request, 'index.html', context)


def process_money(request):
    number = 0
    type_ = getSet(request, 'type')
    farmGold = getSet(request, 'farmGold')
    caveGold = getSet(request, 'caveGold')
    houseGold = getSet(request, 'houseGold')
    casinoGold = getSet(request, 'casinoGold')
    if type_ == 'Farm':
        number = random.randint(10, 20)
        try:
            request.session['farmGold'] = farmGold + number
        except:
            print('Failed to modify')
    if type_ == 'Cave':
        number = random.randint(5, 10)
        try:
            request.session['caveGold'] = caveGold + number
        except:
            print('Failed to modify')
    if type_ == 'House':
        number = random.randint(2, 5)
        try:
            request.session['houseGold'] = houseGold + number
        except:
            print('Failed to modify')
    if type_ == 'Casino':
        number = random.randint(-50, 50)
        try:
            request.session['casinoGold'] = casinoGold + number
        except:
            print('Failed to modify')
    timestamp = moment()['now']
    if number > 0:
        string = f"Earned {number} golds from the {type_}! ({timestamp})"
        color = 'success'
    else:
        color = 'danger'
        string = f"Earned 0 {type_} and lost {abs(number)} golds... Ouch.. ({timestamp})"
    insertLog(request, {
        'type': type_,
        'number': number,
        'timestamp': timestamp,
        'color': color,
        'string': string,
    }
    )
    log = getSet(request, 'log')
    context = {
        'type': type_,
        'farmGold': farmGold,
        'caveGold': caveGold,
        'houseGold': houseGold,
        'casinoGold': casinoGold,
        'number': number,
        'log': log,
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


def insertLog(request, object_):
    try:
        log = getSetLog(request)
        if len(log) > 0:
            temp = []
            for item in log:
                temp.append(item)
            temp.insert(0, object_)
            request.session['log'] = temp
        else:
            request.session['log'] = [object_]
    except:
        print('failed',  request.session['log'])
    return


def getSetLog(request):
    response = []
    name = 'log'
    try:
        response = request.session[name]
    except:
        pass
    for key, value in request.session.items():
        if key == name:
            response = value
    return response


def moment():
    context = {
        "time": strftime("%I:%M %p", gmtime()),
        "datetime": datetime.datetime.now(),
        "day": datetime.datetime.now().strftime("%d"),
        "month": datetime.datetime.now().strftime("%b"),
        "year": datetime.datetime.now().strftime("%Y"),
        'now': timezone.localtime(timezone.now()).strftime("%Y/%m/%d %I:%M %p"),
    }
    return context
