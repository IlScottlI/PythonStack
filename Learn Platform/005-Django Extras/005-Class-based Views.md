# Class Based Views

Much like forms, Class Based Views are part of Django’s goal to minimize how much code we have to rewrite.

We are going to start out with one route deciding between which html verb (‘GET’, ‘POST’, ‘PUT’, ‘PATCH’, ‘DELETE’, to name a few) is being called. This is going to be a generic view type!

The class method will eliminate code snippets like the following:
```py
def index(request):
  if request.method == 'POST':
    # do posty stuff
    pass
  else:
    # do get stuff!
    pass
```
We are going to begin our Class Based View introduction with a couple of quick adjustments:

In our apps  `urls.py`
```py
# urls.py
from django.urls import path
from myapp.views import Users
urlpatterns = [
    path('users', Users.as_view(), name="users"),
]
```
In MVC architecture it is standard to name CONTROLLER classes plural and model classes singular. So now we might guess that we have to create a controller class called Users.

So, in our apps  `views.py`:
```py
from django.http import HttpResponse, render
from django.views.generic import View
class Users(View):
    def get(self, request):
      # Get type view logic here!
      # (for REST this would be show all users)
        return render(request,'index.html')
    def post(self, request):
      # Post type view logic here!
      # (for REST this would be create a new user)
        return render(request,'index.html')
```
#### REST is a standardized naming convention for routing (remember that semi-RESTful routes assignment?)

# Django Leverages OOP

At this point we’ve had a chance to look at a fair bit of the Django documentation and have built a few classes. But we haven’t extended the classes we’ve built too much just yet (we’ve just extended the prebuilt Django classes - e.g. models.Model, or View).

One of the great things about Class Based Views is that we can start making View classes that generate consistent responses so we can start to DRY(Don’t Repeat Yourself) out our code.

### Here is an example:
```py
from django.shortcuts import render
from django.views.generic import View
# Create your views here.
class ExampleView(View):
  footerText = "Fake Copyright 2016, Blob the Blob"
  def get(self,request):
    context = {
    'footer':self.footerText
    }
    return render(request, 'yourApp/index.html', context)
class ExtendExample(ExampleView):
  footerText = "Fake Copyright 2017"
```
This example isn’t very exciting: we basically grab the get method from our ExampleView and rewrite the footerText, but still have access to the get method in its child class (ExtendExample).

In the urls you can use the subclass (child class) and directly get the information, or
```py
# option 1
from django.urls import path
from . import views
urlpatterns = [
    path('', views.ExtendExample.as_view(), name = 'index'),
]
# option2
from django.urls import path
from . import views
urlpatterns = [
    path('', views.ExtendExample.as_view(footerText="bananaPhone"), name = 'index'),
]
```
Give these different options a try and see how your views are rendered (maybe print out {{footer}} on those views just to clarify)!

For large projects that you really want to re-use some core functionality in your controllers, extending view classes can be a great way to clean up your code!

# Assignment: Using Class Based Views

### Create a Django project that uses Class-based Views.

-   Build out the following wireframe:
-   Have at least 3 routes in your apps  [urls.py](http://urls.py/)  (2 going to Class Based Views)

The first route being the root route.

The second route should catch ‘^products$’ with a class based view

The third route should catch ‘^products/(?P <id> \d+)$’ with a class based view

<img src="https://i.ibb.co/4KRQXry/chapter3844-6757-orm-basic-assign2.png" border="0">

-   You can add routes for updating or deleting, and if necessary, don’t be afraid to use function based views.
-   More optional fun! Make buttons to sort the data from the product listings by date, by price etc. (These should be done using the Django ORM rather than jQuery or JavaScript, for the practice with the ORM).
-   You can also add make this a single page application if you’d like! Yay AJAX!


# Python Multiple Inheritance and Class Based views

One thing we didn’t talk about much in the OOP section was Python’s ability to allow multiple inheritance.
```py
 class OurClass(Base1, Base2, Base3):
   ...
```
The above class has not just 1 parent but 3! When an instance of OurClass invokes a method, it looks in Base1, then in Base2 and then in Base3 for that method. (This is abbreviated MRO for method resolution order). If the method isn’t found in any of these Base classes, it will then start looking in the Base classes parents, in the same order.

Here is a nice Stack Overflow on this subject:

[http://stackoverflow.com/questions/3277367/how-does-pythons-super-work-with-multiple-inheritance](http://stackoverflow.com/questions/3277367/how-does-pythons-super-work-with-multiple-inheritance)

This same strategy can be used for Class Based Views in Django. If we want a derived class to have properties from other classes, we can give it multiple inheritance! This idea of adding additional classes is also described as mixing in different classes (mixins).

1.  subclassing and overriding attributes and methods in the subclass. Example:
    ```py
    from django.shortcuts import render
    from django.views.generic import View
    class Welcome(View):
        greeting = "Good Day!"
        template = "welcome/index.html"
        def get(self, request):
            return render(request, self.template, { 'greeting' : self.greeting })
    	
    ```
2.  Configure class attributes as keyword arguments to the  _as_view()_ call in the URL Conf:
    ```py
    urlpatterns = patterns('',
        path('', Welcome.as_view(greeting = "Hello, friend.", template = "welcome/index.html")),
    )
    	
    ```

#### Taking Advantage of CBV

Let's say you have two classes (Home and Profile) that you want to be rendered to two different templates. In a CBV approach, you would probably do this:
```py
class Home(View):
    template = 'home/index.html'
    user = ''
    context = {'templateData' : user }
    def get(self, request):
        return render(request, self.template, self.context)
class Profile(View):
    template = 'profile/index.html'
    user = UserObject
    context = {'templateData' : user }
    def get(self, request):
        return render(request, self.template, self.context)
```
Notice that there were codes that were repeated. Both  _Home_ and  _Profile_ class looked virtually the same as well (except for the value of  _user_ and  _template)._ We can solve this by inheriting from a class that houses common methods and properties:
```py
class Main(object)
    template = ''
    context = None
    user = None
    def get(self, request):
        context = {'templateData' : user }
        return render(request, self.template, context)
class Home(Main, View):
    template = 'home/index.html'
    user = UserObject
class Profile(Main, View):
    template = 'profile/index.html'
    user = UserObject
```
Notice that the  _Main_ class is not inheriting from anything. It's just using the object model. Since both classes (Home, Profile) commonly use _template_ and _user_ variables, we make these variables available to the  _Main_ class for reusability. And since both classes use _get_ methods to render the template, we omitted this method to each of these classes(Home and Profile) and make it available via  _Main_  class to inherit from.

Know that the above example is not yet robust code. You may find it hard to figure out _which instance variable you are supposed to override_ or _what were you supposed to do?_

We can create an extra method within our  _Main_ class to check whether the template instance variable is actually set. If it isn't then we raise an error:
```py
class Main(object):
    template = ''
    context = None
    user = None
    def get(self, request):
        context = {'templateData' : user}
        return render(request, self.get_template(), context)
    def get_template(self):
        if self.template == '':
            raise ImproperlyConfigured('"Template" not defined.')
        return self.template
class Home(Main, View):
    template = 'home/index.html'
    user = UserObject
class Profile(Main, View):
    template = 'profile/index.html'
    user = UserObject
```
Note: the demo code shown in the project below is set up for Django 1.7, using Python 3, but most of it will work with 1.9.

You can download the project demo [here](https://github.com/codingdojo88oliver/django-inheritance)

## Assignment: Class-based Views IV (Inheritance Exercise)

Create a Django project that simply prints the  _sum, difference, product,_ and _factor_ of your favorite and least favorite number. Example: (22, 1).

Your page should display:

### **The sum is: 23**

### **The difference is: 21**

### **The product is: 22**

### **The factor is: 22**

#### Create a  _Main_ class that has these attributes

-   _template = ''_
-   _favorite_number = None_
-   _least_favorite_number = None_

_Main_ class must have these methods:

-   get(self, request) - should simply render a template and should return the  _context._
-   get_template - method that raises an error if template is not defined; if it does, then it simply returns a template
-   add -  _accepts_ two parameters.  _returns_ the sum of those two parameters.
-   subtract -  _accepts_ two parameters.  _returns_ the difference of those two parameters.
-   multiply -  _accepts_ two parameters.  _returns_ the product of those two parameters.
-   divide -  _accepts_ two parameters.  _returns_ the factor of those two parameters.

#### Create a  _Calculator_ class that inherits from the  _Main_ class, and overwrites  _Main_'s attributes

Example:
```py
template = 'calculator/index.html'
favorite_number = 22
least_favorite_number = 1
sum = self.add(favorite_number, least_favorite_number)
```


# Django Prebuilt Views

Django, with its goal of minimizing how much code we actually have to write, has a huge number of prebuilt view types!

[https://docs.djangoproject.com/en/2.2/ref/class-based-views/](https://docs.djangoproject.com/en/1.11/ref/class-based-views/)

These views can do a bunch of neat things to help us out but, in general, they are more helpful for administrators where a view needs to be functional, rather than customized.

That being said: play with a few of them and see how they behave and how they render data!

In addition, hopefully, it provides an idea of how we might build out a custom class based view that does more than just a few calculator like functions!

As we explore these different views, take a look at the MRO (the class inheritance trees) that generate these different classes!


