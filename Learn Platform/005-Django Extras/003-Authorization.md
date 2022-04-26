# The Auth Model

Hopefully by this point we are starting to feel how Django can make our development lives easier. This next step is going to double that feeling!

[https://docs.djangoproject.com/en/2.2/topics/auth/](https://docs.djangoproject.com/en/2.2/topics/auth/)

Since we haven’t done too much to our initial installation (in terms of which apps we are including or not including) we should be ready to use the auth model now!

Think of django.contrib.auth as an app that we are just going to include in our project, much like an app that we built would be included. So if we want to use a model from one of our apps, we might do something like this:

from ..apps.myOtherApp.models import Blogs, Posts

To use Django’s prebuilt model for Users in our (controller)  [views.py](http://views.py/), we’d just add this line in our views:

from django.contrib.auth.models import User

That model is a bit complex and has its own custom manager, but the primary fields in it are:

username, password, email, first_name, last_name

And it is just a model like any other one that we’ve built, but has a bunch of extra methods that would be tedious to build out ourselves, and these allows improved integration with other aspects of Django. Eventually, we will be playing around and will be using an abstracted layer to build our own advanced User class that integrates like this prebuilt one.

Here’s a quick video setting it up!

Here's the rundown:

Start a new project, make an apps/ folder and start a new app 'testUser', then add 'apps.testUser' to INSTALLED_APPS

Set up your outer urls.py then create urls.py in apps/testUser:
```py
python
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index)
]
```
views.py:
```py
from django.shortcuts import render
from django.contrib.auth.models import User
import random
def index(request):
  User.objects.create_user(first_name="Mike", last_name="Hannon", username=str(random.randint(0,100)))
  # Creating a random string as an arbitrary username, since usernames must be unique
  context = {
  'users' : User.objects.all() #retrieves all users
  }
  return render(request, 'index.html', context)
```
templates/testUser/index.html:
```html
<body>
    {% for user in users %}
        <p>{{ user.first_name }} {{ user.username }}</p>
    {% endfor %}
</body>
```

# Login and Registration Using Auth

Let’s start with our login using the prebuilt Django Auth model.

When we made our own validation for login, how we did it was basically retrieve a user based on the unique identifier (email) and then check the hashed password versus the password that was already in the database. If this was successful, then we told our controller to set the proper session variables and off we went!

Well… Django’s auth model does the same thing - in your views.py:
```py
from django.contrib.auth import authenticate, login
```
The authenticate method: Pass it username and password as parameters:
```py
 testuser=authenticate(username=request.POST['username'], password=request.POST['password'])
```
and it return a user object(if there is one) that matches those parameters.

To clarify: it returns either a user object or none… So you can make an conditional logic statement based on this (e.g. if …)

### Note: you have to authenticate a user before logging in using the Django auth. model!

The login function takes a user object, extracts the id and sets a request variable named request.user (this is set in session).
```py
from django.contrib.auth import login
def doStuff(request):
  ... code that works ...
  login(request,testuser)
  print(request.user.first_name)
```
One of the neat things is that user is usable as an element on the templates with request prefixing it.

Not only that, but we could extend a creation form if you wanted to, just like we extended the models.Manager and other classes before now! Yay OOP. (in our  `forms.py`)
```py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)
    # you can set extra validations here to prevent is_valid from succeeding f you don't want it to.
    first_name = forms.CharField(max_length=30,required=True)
    last_name = forms.CharField(max_length=30,required=True)
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        # let's say we wanted to make our data all caps, we could do that here!
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user
```
What about registering a new login?
```py
def register(request):
    form = AuthenticationForm
    form2 = UserCreationForm(request.POST)
    print(form2.is_valid())
    if form2.is_valid():
      user = form2.save(commit=False) # commit = False creates a new user object that isn't yet in the database.
      user.save() # if we didn't have anything else we needed to do with the user.
    print(form2.errors)
    return render(request, "testUser/index.html", {"form":form(), "form2":form2})
```
Search for cleaned_data in the documentation below to understand what is going on here:  [https://docs.djangoproject.com/en/2.2/topics/forms/](https://docs.djangoproject.com/en/2.2/topics/forms/)

# Login and Registration Using Auth

Let’s start with our login using the prebuilt Django Auth model.

When we made our own validation for login, how we did it was basically retrieve a user based on the unique identifier (email) and then check the hashed password versus the password that was already in the database. If this was successful, then we told our controller to set the proper session variables and off we went!

Well… Django’s auth model does the same thing - in your views.py:
```py
from django.contrib.auth import authenticate, login
```
The authenticate method: Pass it username and password as parameters:
```py
 testuser=authenticate(username=request.POST['username'], password=request.POST['password'])
```
and it return a user object(if there is one) that matches those parameters.

To clarify: it returns either a user object or none… So you can make an conditional logic statement based on this (e.g. if …)

### Note: you have to authenticate a user before logging in using the Django auth. model!

The login function takes a user object, extracts the id and sets a request variable named request.user (this is set in session).
```py
from django.contrib.auth import login
def doStuff(request):
  ... code that works ...
  login(request,testuser)
  print(request.user.first_name)
```
One of the neat things is that user is usable as an element on the templates with request prefixing it.

Not only that, but we could extend a creation form if you wanted to, just like we extended the models.Manager and other classes before now! Yay OOP. (in our  `forms.py`)
```py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)
    # you can set extra validations here to prevent is_valid from succeeding f you don't want it to.
    first_name = forms.CharField(max_length=30,required=True)
    last_name = forms.CharField(max_length=30,required=True)
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        # let's say we wanted to make our data all caps, we could do that here!
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user
```
What about registering a new login?
```py
def register(request):
    form = AuthenticationForm
    form2 = UserCreationForm(request.POST)
    print(form2.is_valid())
    if form2.is_valid():
      user = form2.save(commit=False) # commit = False creates a new user object that isn't yet in the database.
      user.save() # if we didn't have anything else we needed to do with the user.
    print(form2.errors)
    return render(request, "testUser/index.html", {"form":form(), "form2":form2})
```
Search for cleaned_data in the documentation below to understand what is going on here:  [https://docs.djangoproject.com/en/2.2/topics/forms/](https://docs.djangoproject.com/en/2.2/topics/forms/)

### For this Assignment, try making a successful login and registration page using Django Forms and Django Auth!

# Regulating who can do what!

[https://docs.djangoproject.com/en/2.2/topics/auth/default/#topic-authorization](https://docs.djangoproject.com/en/2.2/topics/auth/default/#topic-authorization)

Let’s say we’ve created a fantastic site that requires users to login. How do we prevent people from just typing in the url and accessing those pages that we want to reserve for logged-in users? (Or for that matter, different groups of users?)

We can do this in a few ways, but for now we'll be looking at the  **decorator**  strategy.

Decorators are basically a shortcut to add functionality to a function.

#### Examine this Python code:
```py
# our decorator
def counter_above_31(inner_function):
    def checker(a, b):
        if counter < 31:
            return "Counter not high enough"
        else:
            return inner_function(a, b)
    return checker
def add(a, b):
    return a + b
# now lets imagine we only want to be able to add things in our program when the counter is above 31:
add = counter_above_31(add)
counter = 29
add = counter_above_31(add)
print(add(12,45))
counter = 45
print(add(12,45))
```
It's a bit confusing, we admit! But basically we’ve created a decorator called counter_above_31. This function returns another function called checker, which takes two variables a, b. We then pass in an inner_function to this decorator (add in this case) which is returned with a, b from  **checker**  if counter is greater than 31.

Django auth has created a decorator for us for login, called login_required. Before the ‘inner_function’ is run, it checks to see whether or not a user is logged in. If they aren’t logged in, they get sent to a specific url passed in as a **kwarg with the key login_url, otherwise it runs the inner function (in this case login_success, but you can, of course name it whatever you want!).

#### Example Snippet
```py
from django.contrib.auth.decorators import login_required
@login_required(login_url='/')
def login_success(request):
    return render(request,"ourApp/show.html")
```
If a user isn’t logged in, we redirect the user to the root route (’/’), otherwise the normal login_success function runs!

For more fun, we can give specific users permissions, and give certain groups permission to access specific pages (and add specific users to groups) to further refine user experience on our Django sites!

[https://docs.djangoproject.com/en/2.2/ref/contrib/auth/#django-contrib-auth](https://docs.djangoproject.com/en/2.2/ref/contrib/auth/#django-contrib-auth)
