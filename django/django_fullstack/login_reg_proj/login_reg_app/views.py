from django.shortcuts import render, redirect
from login_reg_app.models import User
from django.contrib import messages


# Create your views here.


def index(request):
    try:
        postData = request.session['postData']
    except:
        postData = {}
    context = {
        'postData': postData
    }
    return render(request, 'index.html', context)


def process(request):
    action = redirect('/')
    print(request.POST)
    if getSet(request, 'type') == 'reg':
        action = userReg(request)
    elif getSet(request, 'type') == 'login':
        action = userLogin(request)
    return action


def userLogin(request):
    action = redirect("/")
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        action = redirect("/")
    else:
        request.session['userLogged'] = User.objects.filter(
            email=request.POST['login_email'])[0].id
        request.session['loginType'] = "Logged in"
        action = redirect("/success")
    return action


def userReg(request):
    errors = User.objects.basic_validator(request.POST)
    request.session['postData'] = request.POST
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        action = redirect("/")
        return action
    else:
        newItem = User.objects.create(
            first_name=getSet(request, 'first_name'),
            last_name=getSet(request, 'last_name'),
            email=getSet(request, 'email'),
            password=getSet(request, 'password'),
        )
        messages.info(request, "User Account Successfully Created",
                      extra_tags='upper')
        # Cleaning up the reg form
        request.session['first_name'] = ''
        request.session['last_name'] = ''
        request.session['password'] = ''
        request.session['email'] = ''
        # Saving user to session storage
        request.session['userLogged'] = newItem.id
        request.session['loginType'] = "Registered"
        # Redirecting to success/
        action = redirect("/success/")
    return action


def success(request):
    try:
        userLogged = request.session['userLogged']
    except:
        userLogged = {}
    try:
        loginType = request.session['loginType']
    except:
        loginType = ""
    if userLogged == {}:
        action = redirect('/')
    else:
        context = {
            'userLogged': userLogged,
            'userObject': User.objects.get(id=userLogged),
            'loginType': loginType
        }
        action = render(request, 'success.html', context)
    return action


def logout(request):
    request.session.clear()
    return redirect('/')


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
