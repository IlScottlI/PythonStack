# Django Level III

#### Welcome!

By this point you know how to make a robust, multi-app project.  
You can take advantage of Django's MTV structure to split your app into conceptual chunks. You have skinny controllers. You can build a database using Models and forward engineer it with migrations. You know how to use sessions and Django Template Engine.

You're a full stack web developer!

Still, Django has plenty more to offer. In Level III, we'll be covering four major topics.

-   Forms
-   The built-in Auth model
-   AJAX with Django
-   Class Based Views

Forms allow us to generate forms once and insert them into our html files in a single line of code! We can also auto-generate forms based on our Models.

The built-in Auth model takes care of user authentication in its entirety -- registration, login, logout, password changes, and validations. Its downside is that it is somewhat inflexible in terms of what fields it has, so in the second part of this section we'll go over how to customize the Auth model with your own fields, keeping all the work that Django is doing for us.

Next we will incorporate AJAX, allowing us to make super responsive webpages on which we can make database queries and updates without needing to refresh or change the page, and our page's content can update dynamically too!

Finally, we'll look into Class Based Views. This is a way of taking DRY to the next level, so we can leverage the power of inheritance and set up default variables with RESTful syntax.

Make sense? Let's dive in!

# What is the ORM doing?

For many of us, we are just figuring out SQL so coupling Object Relational Mapping on top creates all sorts of confusion. Let’s talk a bit more about the ORM and objects.

This might not seem germane, but let’s start with a linked list with different node types:
```py
  class ListNode(object):
    def __init__(self,val):
      self.val = val
      self.next = None
  class CustomNode(object):
    def __init__(self,val,*bonus):
      self.val = val
      self.next = None
      self.bonus = bonus
  class LinkedList(object):
    def __init__(self):
      self.head = None
    def addNode(self, val, *extras):
      if not self.head:
        if extras:
          self.head = CustomNode(val,extras)
        else:
          self.head = ListNode(val)
        return self
      current = self.head
      while current.next:
        current = current.next
      if extras:
        current.next = CustomNode(val,extras)
      else:
        current.next = ListNode(val)
      return self
  myList = LinkedList()
  myList.addNode(72,"hello world", "banana").addNode(45).addNode(21, "Yay")
  print(myList)
  print(myList.head)
  print(myList.head.next)
  print(myList.head.next.next.bonus)
```
In this example myList.head is just a pointer. It starts out pointing to None, and then we set it to point to an object when we add a node. The object it is pointing at has its own properties. In this case, all objects have two properties in common: val and next and one of the object types (CustomNode) has an additional property, named bonus.

We can access each of the properties in each node, as we move from node to node!

## Parts of the ORM work in a very similar way! Let’s look!
```py
  class User(models.Model):
      first_name = models.CharField(max_length=200)
      last_name = models.CharField(max_length=200)
      email = models.EmailField()
      password = models.CharField(max_length=200)
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True)
  class Message(models.Model):
      message = models.TextField()
      user = models.ForeignKey(User, on_delete=models.CASCADE)
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True)
  class Comment(models.Model):
      comment = models.TextField()
      user = models.ForeignKey(User)
      message = models.ForeignKey(Message, on_delete=models.CASCADE)
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True)
```
Let’s look at the Comment class. An instance of the Comment class has two pointers to other objects. The pointers’ names are user which points to a User object instance, and message which points to a Message object instance. So just like in the linked list example, we could say something like: CommentInstance.message.message. The first message is the pointer to the message object. The second message is the actual message property of the message object. (To slightly clarify this if we changed the property ‘message’ in our Message class to “donutflavor” to get the donutflavor associated with a specific comment we’d go CommentInstance.message.donutflavor). In plainer English, this says we have an instance of a comment, that has a pointer to a message object. That message object has a number of properties/pointers, one of which is this donut flavor, which we are then accessing. This logic works great when a pointer is pointing at a specific object (like we discussed above, but what if we want to get all of specific message’s comments). A Message instance doesn’t have a pointer to all the comments… ENTER DJANGO!

Django has 3 major relationship types and deals with these things for us!

### One to one

This makes an imaginary property IN THE OBJECT THAT THE ONE_TO_ONE relationship is not defined in, in addition to the real property in the object that the relationship IS defined in. So if we had a one_to_one relationship in an object e.g.
```py
  class User(models.Model):
    first_name = models.CharField(max_length=45)
  class CustomUserId(models.Model):
    newId = models.IntegerField()
    specificUser = models.OneToOneField(User)
```
Here a userObject has a customUserId as well as a customUserId having a specificUser property. If we want to change the way we reference that artificially generated key, we could change our model like this:
```py
  class User(models.Model):
    first_name = models.CharField(max_length=45)
  class CustomUserId(models.Model):
    newId = models.IntegerField()
    specificUser = models.OneToOneField(User, related_name="myId", on_delete=models.CASCADE)
```
Now the User object would reference the CustomUserId objects by userObject.myId (and then maybe .newId if you wanted to get that integer stored in newId)

### One to many

One side of the one to many behaves just like the one_to_one relationship, and we described it above. But how does django deal with the opposite direction relationship, e.g. going from a User object to the  **set**  of messages or comments? Well Django has provided us a tool: Lower_case class name followed by _set = access to the set of objects of the related key.
```py
User.objects.message_set.all()
```
The above code would retrieve all of the messages associated with that particular user object. Much like with a OneToOneField, we can set a related name. If we do, the message_set piece of code would be replaced with related name.
```py
  class User(models.Model):
      first_name = models.CharField(max_length=200)
      last_name = models.CharField(max_length=200)
      email = models.EmailField()
      password = models.CharField(max_length=200)
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True)
  class Message(models.Model):
      message = models.TextField()
      user = models.ForeignKey(User, related_name="messages", on_delete=models.CASCADE)
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True)
  class Comment(models.Model):
      comment = models.TextField()
      user = models.ForeignKey(User)
      message = models.ForeignKey(Message, on_delete=models.CASCADE)
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True)
```
This is of particular use when you have Class that joins to the same class more than once. (Since classname_set would not know which of the associations you are talking about!) Given the above model, note the related_name (‘messages’) now in our Message class? Now a user object can reference messages not through message_set, but through that related name: messages.
```py
User.objects.messages.all()
```
### Many to many

Our last common relationship in Django: The many to many relationship. In this relationship both directions of the relationship are sets! The example that Django uses is Pizzas and Toppings. Any pizza can have many toppings, and any topping can be on many pizzas. We strive to place the many to many where it makes the most sense. In this case we’d set the relationship in pizzas, such that we could do
```py
pizzaObject.toppings.all()
```
versus
```py
pizzaObject.toppings_set.all()
```
but either direction requires the secondary call.

This is one of those topics that can take a bit to wrap our heads around. Making projects that have these relationships in them can really help!

# debug_toolbar

Debug toolbar provides a convenient way to look under the hood of your Django application. This toolbar, once installed, provides some detailed information about your application which can be super useful when troubleshooting and debugging your Django application.

Let’s install the toolbar and start checking out the information it provides!

### Installation

The recommended way to install Debug Toolbar is via pip:
```
  $ pip install django-debug-toolbar
```
Add  `'debug_toolbar'`  to your `INSTALLED_APPS in your  _settings.py_ folder.
```py
INSTALLED_APPS = [
    ...
    'django.contrib.staticfiles',
    'debug_toolbar',
    ...
]
```
Start up your Django app and you should see a little tab sticking out in your browser labeled `DjDT`, click on that and check out your cool new debugging toolbar.

### Documentation!

Read more about debug toolbar here:
```
 https://django-debug-toolbar.readthedocs.io/en/stable/installation.html
 https://github.com/django-debug-toolbar/django-debug-toolbar
```


# Django Admin

Well done making it this far! We’ve already covered everything you’ll need to pass the belt exam!

Now we’re going to start implementing some more advanced functionality that really makes Django awesome.

### Let’s first create a new project
```py
  > django-admin startproject initialAdmin
  > cd initialAdmin
```
_Now make sure you make your migrations!_
```py
  # Once we run migrate, we can create superuser
  > python manage.py createsuperuser
  # Follow prompts to fill in:
  # Username
  # Email address
  # Password
  # Password (again)
  # Afterward you should see "Superuser created successfully."
  > python manage.py runserver
```
Let’s navigate to  `localhost:8000/admin`  in our browser and enter the information you just provided to the  `createsuperuser`  prompts.

If you see this:

<img src="https://i.ibb.co/2NpVjFK/chapter3843-6993-Screen-Shot-2016-08-16-at-1-43-45-PM.png" border="0">

Congratulations!

You’ve reached the  **admin portal**  in Django, a fantastic tool to modify and play with things like your database data. (We avoided using this functionality earlier to prevent confusion with the routing and terminal commands.)

Now pretend we had an app  `awesomeApp`  with a bunch of models, and we want to add those models to the manager.

We’re going to add some code to our  `urls.py`  file that will link our app’s models to Django’s admin utility. In general, Django recommends you keep this code in the auto-generated  `admin.py`  file of your app, but we’re going to stick it in  `urls.py`  for now just to keep our code in fewer places.

Let’s update our project’s  `urls.py`  file to the following:
```py
  # From inside your project's urls.py file
  from django.urls import path, include
  from django.contrib import admin
  # THIS SECTION IS NEW!
  # ********************
  from awesomeApp.models import User as U, Fruit, Donut, Group
  class UAdmin(admin.ModelAdmin):
      pass
  admin.site.register(U, UAdmin)
  class FruitAdmin(admin.ModelAdmin):
      pass
  admin.site.register(Fruit, FruitAdmin)
  class DonutAdmin(admin.ModelAdmin):
      pass
  admin.site.register(Donut, DonutAdmin)
  class GroupAdmin(admin.ModelAdmin):
      pass
  admin.site.register(Group, GroupAdmin)
  # ****************
  urlpatterns = [
  # Your app's urls is lined to the project
      path('admin/',admin.site.urls),
      path('awesomeApp/', include('awesomeApp.urls')),
  ]
```
Now refresh the admin page in your browser – all your models/data should be viewable!

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
    return render(request, "ourApp/show.html")
```
If a user isn’t logged in, we redirect the user to the root route (’/’), otherwise the normal login_success function runs!

For more fun, we can give specific users permissions, and give certain groups permission to access specific pages (and add specific users to groups) to further refine user experience on our Django sites!

[https://docs.djangoproject.com/en/2.2/ref/contrib/auth/#django-contrib-auth](https://docs.djangoproject.com/en/2.2/ref/contrib/auth/#django-contrib-auth)

# Multiple Apps

Raise your hand if re-writing code that you've already written stinks.

Thought so. One of the exceptional things about Django is the ability to reference apps that you've already written. This is what people are referring to when they say how nice and  `modular`  the Django framework is.

That's what we're about to do! (Just remember this works only if you use the  **named routes**  strategy that we talked about earlier. You can even be more specific with  **namespaces** ( since you're on your way to becoming a professional developer, you won't mind a little  [documentation](https://docs.djangoproject.com/en/2.2/topics/http/urls/)  to learn about it.)

Let's say we wanted to have a single project containing  _all_  of the awesome mini-apps that we've built so far.

First, we need to add the relevant apps to your  `settings.py`  file (and potentially put them in your  `apps`  folder).  _Plenty of people forget this step when they're first starting out!_

Next, we need some way to direct HTTP requests from the browser to the correct routing file:

> This is what our main  `urls.py`  file has looked like up till now
```py
  # Inside your main project's urls.py file
  urlpatterns = [
    path('', include('current_project.urls'))
  ]
```
> But there's nothing stopping us from transforming our main  `urls.py`  to something like this:
```py
  urlpatterns = [
      path('', include('first_app.urls')),
      path('time-display/', include('time_display.urls')),
      path('rand-word/', include('random_word.urls')),
      path('ninjas/', include('disappearing_ninja.urls')),
      path('ninja-gold/', include('ninja_gold.urls')),
      path('courses/', include('courses.urls'))
  ]
```
_Some things to note_:  **All**  of the routes, except the first one, have a match with  `'/'`  at the end of the pattern.

That means that by traveling to  `localhost:8000/ninjas/`, our  `disappearing_ninja`  app's  `urls.py`  file would take over (receiving an empty string) and potentially load all of your ninjas!

One last thing to note: You can pull in an app and use a model from that app in another app! This is extremely cool.

Let's say I added an `mh_user`  app, which is my fully customized login and registration, to my project. In my  `quotes`  app, I could go into my model (or anywhere in my project for that matter) and add:
```py
  # From inside one of your app's models.py file
  from '''Relative Path to ourOtherApps models.py file''' import User
```
This relative path is often ..  **nameofapp**.models. The .. says go up one folder from where you are currently sitting.

(  `User`  is accessible because we added the app generating User to our main project's  `settings.py`  file. Told you that step was important!)

## Assignment: Multiple Apps

Next, you'll be creating a new project called  `integration_project`. In this project you'll bring together several apps you've already created into one big project

-   Pick three of your level-one assignments and add their respective apps to your new project.
-   Now add the  `courses`  and  `login_reg`  apps
    -   Make a  _new model_  in one of the apps that uses a  `ForeignKey`  field to link to the other app
    -   Build the following additional template for  `courses`:

<img src="https://i.ibb.co/bFTz6Zx/chapter3834-6626-user-courses.png" border="0">





