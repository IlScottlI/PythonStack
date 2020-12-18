from django.shortcuts import render, redirect
from wall_app.models import User, Message, Comment
from django.contrib import messages


def login(request):
    request.session['userLogged'] = {}
    try:
        postData = request.session['postData']
    except:
        postData = {}
    context = {
        'postData': postData,
    }
    print(context)
    return render(request, 'login.html', context)


def process(request):
    action = redirect('/login')
    print(request.POST)
    if getSet(request, 'type') == 'reg':
        action = userReg(request)
    elif getSet(request, 'type') == 'login':
        action = userLogin(request)
    elif getSet(request, 'type') == 'post_message':
        action = postMessage(request)
    elif getSet(request, 'type') == 'post_comment':
        action = postComment(request)
    return action


def postComment(request):
    action = redirect("/wall")
    errors = Comment.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        action = redirect("/wall")
    else:
        newComment = Comment.objects.create(
            comment=request.POST['comment'],
            author=User.objects.get(id=request.POST['user_id']),
            message=Message.objects.get(id=request.POST['message_id'])
        )
        messages.success(request, "Comment Created")
        action = redirect(f"/wall")
    return action


def postMessage(request):
    action = redirect("/wall")
    errors = Message.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        action = redirect("/wall")
    else:
        newPost = Message.objects.create(message=request.POST['message'], author=User.objects.get(
            id=request.POST['user_id']))
        messages.success(request, "Post Created")
        action = redirect(f"/wall")
    return action


def userLogin(request):
    action = redirect("/login")
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        action = redirect("/login")
    else:
        request.session['userLogged'] = User.objects.filter(
            email=request.POST['login_email'])[0].id
        request.session['loginType'] = "Logged in"
        action = redirect("/wall")
    return action


def userReg(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        request.session['postData'] = request.POST
        action = redirect("/login")
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
        action = redirect("/wall")
    return action


def index(request):
    action = redirect('/wall')
    return action


def wall(request):
    Posts = []
    try:
        userLogged = request.session['userLogged']
    except:
        userLogged = {}
    try:
        loginType = request.session['loginType']
    except:
        loginType = ""
    if userLogged == {}:
        action = redirect('/login')
    else:
        try:
            userObject = User.objects.get(id=userLogged)
        except:
            userObject = {}
        try:
            for item in Message.objects.all():
                Posts.append({
                    'Messages': item,
                    'comments': Comment.objects.filter(message=item)
                })
        except:
            Posts = []
        context = {
            'userLogged': userLogged,
            'userObject': userObject,
            'loginType': loginType,
            'Posts': Posts,
        }
        print(context)
        action = render(request, 'wall.html', context)
    return action


def logout(request):
    request.session.clear()
    return redirect('/login')


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
