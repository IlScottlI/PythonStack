from django.shortcuts import render, HttpResponse, redirect
import random


def index(request):
    number = setGetRandomNumber(request)
    status = getSet(request, 'status')
    guess = getSet(request, 'guess')
    attempt = getSet(request, 'attempt')
    tries = getSet(request, 'tries')
    percent = getSet(request, 'percent')
    winners = getSetWinners(request)
    context = {
        'request': request,
        'number': number,
        'status': status,
        'guess': guess,
        'attempt': attempt,
        'tries': tries,
        'percent': percent,
        'winners': winners,
    }
    print(context)
    return render(request, 'index.html', context)


def guess(request):
    number = setGetRandomNumber(request)
    guess = getSet(request, 'guess')
    tries = setGetTries(request)
    addTries(request, tries)
    if int(guess) > int(number):
        response = 'To High'
    elif int(guess) < int(number):
        response = 'To Low'
    else:
        response = 'Correct'
    if tries > 5:
        try:
            response = 'You Lose'
        except:
            pass
    request.session['status'] = response
    return redirect('/')


def setGetRandomNumber(request):
    number = 0
    try:
        if request.session['number']:
            number = request.session['number']
    except:
        request.session['number'] = random.randint(1, 100)
    for key, value in request.session.items():
        if key == 'number':
            if value > 0:
                number = request.session['number']
            else:
                request.session['number'] = random.randint(1, 100)
                number = request.session['number']
    return number


def setGetTries(request):
    tries = 0
    try:
        tries = request.session['tries']
    except:
        request.session['tries'] = tries
    for key, value in request.session.items():
        if key == 'tries':
            if int(value) > -1:
                request.session['tries'] = int(tries) + 1
                tries = request.session['tries']
    return tries


def getSetWinners(request):
    response = []
    name = 'winners'
    try:
        response = request.session[name]
    except:
        pass
    for key, value in request.session.items():
        if key == name:
            response = value

    return response


def addTries(request, tries):
    request.session['percent'] = (int(tries) / 5) * 100


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


def clearSession(request):
    # request.session.clear()
    request.session['number'] = 0
    request.session['status'] = 0
    request.session['guess'] = 0
    request.session['attempt'] = 0
    request.session['tries'] = 0
    request.session['percent'] = 0
    return redirect('/')


def submitResults(request):
    if getSet(request, 'status') == 'Correct':
        number = setGetRandomNumber(request)
        status = getSet(request, 'status')
        guess = getSet(request, 'guess')
        attempt = getSet(request, 'attempt')
        tries = getSet(request, 'tries')
        percent = getSet(request, 'percent')
        try:
            userName = request.POST['userName']
        except:
            userName = 'Unknown'
        try:
            request.session['temp'] = {'userName': userName, 'tries': tries}
            temp = request.session['temp']
        except:
            temp = None
        winners = getSetWinners(request)
        context = {
            'request': request,
            'number': number,
            'status': status,
            'guess': guess,
            'attempt': attempt,
            'tries': tries,
            'percent': percent,
            'winners': winners,
            'userName': userName,
            'temp': temp
        }
        print(context)
        insertWinner(request, temp)
        request.session['number'] = 0
        request.session['status'] = 0
        request.session['guess'] = 0
        request.session['attempt'] = 0
        request.session['tries'] = 0
        request.session['percent'] = 0
        action = redirect('/leaderboard')
    else:
        action = redirect('/')
    return action


def leaderboard(request):
    winners = getSetWinners(request)
    number = setGetRandomNumber(request)
    status = getSet(request, 'status')
    guess = getSet(request, 'guess')
    attempt = getSet(request, 'attempt')
    tries = getSet(request, 'tries')
    percent = getSet(request, 'percent')
    context = {
        'request': request,
        'number': number,
        'status': status,
        'guess': guess,
        'attempt': attempt,
        'tries': tries,
        'percent': percent,
        'winners': winners,
    }
    return render(request, 'leaderboard.html', context)


def insertWinner(request, winner):

    try:
        winners = getSetWinners(request)
        if len(winners) > 0:
            temp = []
            for item in winners:
                temp.append(item)
            temp.append(winner)
            request.session['winners'] = temp
        else:
            request.session['winners'] = [winner]
    except:
        print('failed',  request.session['winners'])
    return
