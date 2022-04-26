


# Introduction to Django

## Objectives:

-   Learn about MVC
-   Understand the benefits of an MVC/MTV framework
-   Our strategy for covering Django
-   Create a virtual environment for our Django projects

----------

## Separating Concerns

Some web development frameworks combine everything into one large, potentially monstrous file. Imagine you're on a team with a dozen other developers—how easy will it be to collaborate in one giant file? Yikes! Django's MTV structure allows us to outsource the different kinds of tasks to specific file locations. When we begin a Django project, files will be created to play all of the necessary roles in a web application:

-   Routes (expected requests)
-   Functions associated with those routes (how our server responds)
-   Database interaction (storing, retrieving data from database)
-   Templates (what the user interacts with)

Django further divides an application into individual  **_apps_**  that work together as part of one whole  **_project_**.

### MTV (or MVC)

Developers who design frameworks have to make decisions about organizing code. One of the most popular patterns for organizing code is one known as MVC: Model-View-Controller. Django's pattern, MTV: Model-Template-View, is very similar. Here's a basic breakdown of responsibilities:

|Django Component|MVC Component| Purpose |
|----|----|----|
|**Model**| **Model** |-   May build database tables <br> -   Handles logic that relies on data <br> -   Interfaces with the database|
|**Template**|**View**|-   HTML page that gets served to the client <br>-   May contain some logic to be handled by a template engine|
|**View**|**Controller**|-   Receives incoming requests<br>-   Minimal logic<br>-   Calls on models to aggregate/process data<br>-   Determines appropriate response|

## A Django Virtual Environment

Let's create a new virtual environment for our Django projects. We'll need to do this just once. Create and navigate to a folder named  _my_environments_  and run the appropriate commands to create a virtual environment and then install Django:

**Create your environment:**  
```shell
------------------------------------------------------------------
| Mac/Linux: | python3 -m venv djangoPy3Env 
-------------+----------------------------------------------------
| Windows (command prompt): | python -m venv djangoPy3Env
>------------------------------------------------------------------
```
**Activate your environment:**  
```shell
------------------------------------------------------------------
| Mac/Linux: | source djangoPy3Env/bin/activate                         
------------------------------------------------------------------
| Windows (command prompt): | call djangoPy3Env\Scripts\activate       
------------------------------------------------------------------
| Windows (git bash) : | source djangoPy3Env/Scripts/activate         
------------------------------------------------------------------
```
**Install Django:**  
```shell
(djangoPy3Env) Windows/Mac:| pip install Django==2.2.4
```

#   
Creating a Django Project

## Objectives:

-   Practice the steps for creating a Django project with a single app
-   Familiarize ourselves with the role of each file

----------

So we've talked about modularization and MTV (and MVC), but what does that really mean? Let's go ahead and build a Django project, and then we'll review the folder structure to really see what modularization is all about.

Remember that a single application in Django (in our case, every assignment) is called a  **_project_**, which contains one or more **_apps_**.

1.  With our Django virtual environment activated, create a new Django project. First navigate to where you want the project to be saved (for these first few assignments, that will be the  _python_stack/django/django_intro_  folder). Then run this command, specifying a project name of our choosing:
    ```
    > cd python_stack/django/django_intro
    django_intro> django-admin startproject your_project_name_here
    ```
    -   Let's test this out:
        
        Navigate into the folder that was just created. A new Django project has just been created--let's run it!
        
		```
		django_intro> cd your_project_name_here
		your_project_name_here> python manage.py runserver
		```
        Open  `localhost:8000`  in a browser window. Hooray for CLIs (command-line interfaces)!
        
        (Don't worry about the warning about unapplied migrations. It won't affect us for now, and we'll address it soon enough.)
        
    
    Press `ctrl-c`  to stop the server. Open up the project folder in your text editor. (Take note of the folder structure so far!) We'll be updating some of these files shortly.
    
2.  For every app we want to add to our project, we'll do the following:
    1.  ```your_project_name_here> python manage.py startapp your_app_name_here```
        
        **The apps in a project CANNOT have the same name as the project.**
        
    2.  In the text editor, find the  `settings.py`  file. It should be in a folder with the same name as our project. Find the variable  _INSTALLED_APPS_, and let's add our newly created app:
        
        #### your_project_name_here/your_project_name_here/settings.py
        ```py
           INSTALLED_APPS = [
               'your_app_name_here', # added this line. Don't forget the comma!!
               'django.contrib.admin',
               'django.contrib.auth',
               'django.contrib.contenttypes',
               'django.contrib.sessions',
               'django.contrib.messages',
               'django.contrib.staticfiles',
           ]    # the trailing comma after the last item in a list, tuple, or dictionary is commonly accepted in Python
        ```
    3.  For these next few steps, we are creating the route "/" to be associated with a specific function. Trust for now--we'll break this down in greater detail in the next tab. In the urls.py file, add a URL pattern for your new app. (You can delete the current admin pattern, or just ignore it for now). You will need to add an import for your views file.
        
        #### your_project_name_here/your_project_name_here/urls.py
        ```py
        from django.urls import path, include           # import include
        # from django.contrib import admin              # comment out, or just delete
        urlpatterns = [
            path('', include('your_app_name_here.urls')),	   
            # path('admin/', admin.sites.urls)         # comment out, or just delete
        ]
        ```
    4.  Next, let's create a new urls.py file in the your_app_name_here folder. Put the following code
        
        #### your_project_name_here/your_app_name_here/urls.py
        ```py
        from django.urls import path     
        from . import views
        urlpatterns = [
            path('', views.index),	   
        ]
        ```
    
    1.  And then actually put a function called index in our app's views.py file:
        
        #### your_project_name_here/your_app_name_here/views.py
        ```py
        from django.shortcuts import render, HttpResponse
        def index(request):
            return HttpResponse("this is the equivalent of @app.route('/')!")
        ```
    
3.  Let's run our app again and check it out at  `localhost:8000/`. Whew. We've done it!
    ```
    your_project_name_here> python manage.py runserver
    ```

  

**Note: Do not manually change the name of any of your folders after creation!**

For a quick summary/visual overview, here's the structure we should have after all these steps, inside the project folder.

<img src="https://i.ibb.co/C73S5hr/project-structure.png" border="0">

  

### Video Overview

# Django Routing

## Objectives:

-   Understand how routes are divided between project and app level urls.py files
-   Understand how requests are resolved from the urls.py files to the views.py file

----------

We have a new Django project running, but what was all that code we added there at the end?

#### project_name/project_name/urls.py
```py
from django.urls import path, include
    
urlpatterns = [
    path('', include('app_name.urls')),
]
```
The  `urlpatterns`  is simply a variable that holds a list of urls that this project recognizes. Notice there are 2 arguments being passed to the url function:

1.  a raw string representing a route pattern (in our example:  `''`)
2.  what to do if the pattern matches (in our example:  `include('app_name.urls')`)

The second argument,  `include('app_name.urls')`  will resolve the rest of the route. So let's go there:

#### project_name/app_name/urls.py
```
from django.urls import path
from . import views	# the . indicates that the views file can be found in the same directory as this file
                    
urlpatterns = [
    path('', views.index),
]
```
This is the same url function, but this time our arguments indicate that:

1.  `''`  - the rest of the route both starts and ends with nothing (i.e. "/" is the full route), and
2.  `views.index`  - if the requested route matches this pattern, then the function with the name "index" from this app's views.py file will be invoked.

If the route wants a views.index function, then we'd better have one:

#### project_name/app_name/views.py
```py
from django.shortcuts import render, HttpResponse
def index(request):
    return HttpResponse("response from index method from root route, localhost:8000!")
```
A couple of important things to notice here:

1.  _Every function's first argument will be the **request** object._
2.  We don't distinguish in our routes anywhere between GET vs POST requests. This will be done _within_  a given function.
3.  If we are returning a string, we cannot simply return a string, but must send the string via HttpResponse (which must be imported. We'll be returning rendered templates again soon enough!)

Here's a visual of how routes get resolved in a Django project:

<img src="https://i.ibb.co/4F2SZt3/django-routing.png" border="0">

#### Video Overview

#   
Routing with Parameters

## Objectives:

-   Learn how to capture variables from the url

----------

In this module, we will look into how Django interprets a request with varying values.

Learn more from the  [documentation](https://docs.djangoproject.com/en/2.2/topics/http/urls/#how-django-processes-a-request).

Here are a few examples, to demonstrate the syntax:

#### some_project/some_app/urls.py
```py
urlpatterns = [
        path('bears', views.one_method),                        # would only match localhost:8000/bears
        path('bears/<int:my_val>', views.another_method),       # would match localhost:8000/bears/23
        path('bears/<str:name>/poke', views.yet_another),       # would match localhost:8000/bears/pooh/poke
    	path('<int:id>/<str:color>', views.one_more),           # would match localhost:8000/17/brown
]
```
The corresponding functions would then look like this:

#### some_project/some_app/views.py
```py
def one_method(request):                # no values passed via URL
    pass                                
    
def another_method(request, my_val):	# my_val would be a number from the URL
    pass                                # given the example above, my_val would be 23
    
def yet_another(request, name):	        # name would be a string from the URL
    pass                                # given the example above, name would be 'pooh'
    
def one_more(request, id, color): 	# id would be a number, and color a string from the URL
    pass                                # given the example above, id would be 17 and color would be 'brown'
```
# Response Types

In Django, there are many different ways we can return a response. We will look into returning a HTML template in the next lesson, for now let's focus on these.

-   HttpResponse: Can be used to pass a string as a response.
-   Redirect: Used to navigate to a different view method, before a final response is sent to the client. ***Note*** Even though we don't include the first / in our project urls.py file, when redirecting, you should provide the whole path, starting with the first /.
-   JsonResponse: Used to return a JSON object

urls.py

```py
from django.urls import path
from . import views
urlpatterns = [
    path('', views.root_method),
    path('another_route', views.another_method),
    path('redirected_route', views.redirected_method
]
```

views.py

```py
from django.shortcuts import HttpResponse, redirect # add redirect to import statement
from django.http import JsonResponse
def root_method(request):
    return HttpResponse("String response from root_method")
def another_method(request):
    return redirect("/redirected_route")
def redirected_method(request):
    return JsonResponse({"response": "JSON response from redirected_method", "status": True})
```
# First Django Project

## Objectives:

-   Practice setting up a new Django project
-   Practice setting up a new Django app
-   Practice routing in Django
-   Familiarity with views and how to return a response

----------

It's time to practice routing! Use the checklist below to add routes to your project.

***Note*** for the assignment, the show, edit, and delete methods will require the use of Route Parameters.

***Bonus*** result:

<img src="https://i.ibb.co/cLJ5r9k/Screen-Shot-2020-06-23-at-4-06-38-PM.png" border="0">

- [ ]  Create a new project with a single app
    
- [ ]  / - redirects to the "/blogs" route with a method called "root"
    
- [ ]  /blogs - display the string "placeholder to later display a list of all blogs" with a method named "index"
    
- [ ]  /blogs/new - display the string "placeholder to display a new form to create a new blog" with a method named "new"
    
- [ ]  /blogs/create - redirect to the "/" route with a method called "create"
    
- [ ]  /blogs/< number > - display the string "placeholder to display blog number: {number}" with a method named "show" (eg. localhost:8000/blogs/15 should display the message: 'placeholder to display blog number 15')
    
- [ ]  /blogs/< number >/edit - display the string "placeholder to edit blog {number}" with a method named "edit"
    
- [ ]  /blogs/< number >/delete - redirect to the "/blogs" route with a method called "destroy"
    
- [ ]  (**Bonus**) /blogs/json - return a JsonResponse with title and content keys.

# Templates

## Objectives:

-   Organize template files properly within a Django project
-   Learn the syntax for rendering a template in Django
-   Practice passing data to the template

----------

Django requires each app to have its own templates folder. Within that folder, store all your HTML templates.  

<img src="https://i.ibb.co/zRRgVpb/Screen-Shot-2019-11-14-at-4-01-08-PM.png" border="0">

Assuming we've got the folder structure set up properly, we can then render templates in our views.py file like so:

#### project_name/app_name/views.py

from django.shortcuts import render	# notice the import!
def index(request):
    return render(request, "index.html")

When we call the render function, our first argument will always be request, and the second argument will be a string indicating which html file to render.

## Passing Data to the Template

With Django, we are able to pass data to the template via the render method. We do this by passing a single dictionary  **_whose keys will be the variable names available on the template_**. For example:

#### project_name/app_name/views.py
```py
from django.shortcuts import render
    
def index(request):
    context = {
    	"name": "Noelle",
    	"favorite_color": "turquoise",
    	"pets": ["Bruce", "Fitz", "Georgie"]
    }
    return render(request, "index.html", context)
```
**project_name/app_name/templates/index.html  
**
```html
<h1>Info From Server:</h1>
<p>Name: {{name}}</p>
<p>Color: {{favorite_color}}</p>
<p>Pets</p>
<ul>
{% for pet in pets %}
   <li>{{pet}}</li>
{% endfor %}
</ul>
```
**Note: You cannot use square brackets with Django's template engine! Instead, use dot notation.**

**For example, array[0] becomes {{ array.0 }}**

**Reminder: You cannot comment out template engine syntax with regular HTML comments (<!-- -->).**  [(Check the documentation if you want to be able to comment it out properly)](https://docs.djangoproject.com/en/2.2/topics/templates/#comments)

**Video Overview:**

# Static Files

## Objectives:

-   Organize static files properly within a Django project
-   Learn the syntax for referencing static content in templates

----------

The organization and behavior of static files is very similar to templates. Within each app, at the same level as our templates folder, we also need a folder called static. Then within  _that_  folder, we can save all of our static content (and further subdivide into js, css, and images folders as desired).

In our templates, when we want to reference our static files, we'll first need to add a line indicating we want to use our static files:
```html
<!DOCTYPE html>
  <html>
    <head>
      <meta charset="utf-8">
      <title>Index</title>
      {% load static %}		<!-- added this line -->
```
<img src="https://i.ibb.co/KWGwbmV/Screen-Shot-2019-11-14-at-3-59-05-PM.png" border="0">

Then we can reference any static files relative to their location within the folder called static:
```html
<!DOCTYPE html>
  <html>
    <head>
      <meta charset="utf-8">
      <title>Index</title>
      {% load static %}
      <link rel="stylesheet" href="{% static 'css/style.css' %}">    
      <script src="{% static 'js/script.js' %}"></script>
    </head>
    <body>
    	<img src="{% static 'images/image.jpg' %}" />
    </body>
```
## References

[https://docs.djangoproject.com/en/2.2/howto/static-files/](https://docs.djangoproject.com/en/2.2/howto/static-files/)

**Video Overview:**

# Putting Everything Together

## Objectives:

-   Understanding how data gets passed from View -> Template and Template -> View

### Video Overview

# Assignment: Time Display

## Objectives:

-   Practice setting up a Django project
-   Familiarity with passing data to a template
-   Practice connecting to static files

----------

Create a Django project with a single app called time_display. When you go to  `localhost:8000`  or  `localhost:8000/time_display`, this should run a method in your controller file (views.py) that renders a template displaying the current date and time.

<img src="https://i.ibb.co/wJ08DbR/chapter3832-6613-time.png"  border="0">

There are many ways to get the current time in Python. For example, you could have views.py import  `gmtime, strftime`  from 'time' and pass the appropriate string to the render method. For example, your views.py might look something like this:

from django.shortcuts import render
from time import gmtime, strftime
```py
def index(request):
    context = {
        "time": strftime("%Y-%m-%d %H:%M %p", gmtime())
    }
    return render(request,'index.html', context)
```
To learn more about strftime, see [https://docs.python.org/3.3/library/time.html?highlight=time.strftime#time.strftime](https://docs.python.org/3.6/library/time.html?highlight=time.strftime#time.strftime)

Please also see [https://stackoverflow.com/questions/466345/converting-string-into-datetime](https://stackoverflow.com/questions/466345/converting-string-into-datetime)

Recognize that working with time -  [especially timezones](https://docs.djangoproject.com/en/2.2/topics/i18n/timezones/)  - is among the more frustrating parts of computer programming. Do not spend more than 15 minutes exploring timezones. We will have numerous opportunities to discuss the challenges of timezones. Essentially, we want to store any timestamps in our database in UTC, and eventually use JavaScript to get the time from the user's browser to customize how times are displayed. For now, the easy fix is to set your Django settings to the timezone that works for you and move on. You have more important things to cover at this part of your career as a developer than timezones.

- [ ]  Create a new project with a single app
    
- [ ]  Have the root route display the current date and time
    
- [ ]  Incorporate your own custom stylesheet   
- [ ]  NINJA BONUS: Come up with a different way to retrieve the datetime

# GET vs. POST Requests

## Objectives:

-   Learn how to handle GET requests in Django
-   Learn how to handle POST requests in Django
-   Learn about CSRF tokens and why we use them

----------

A Django view method will be called regardless of the type of HTTP Request method that was made. We can check the request method type being received, like so:
```py
from django.shortcuts import render, redirect
def some_function(request):
    if request.method == "GET":
    	print("a GET request is being made to this route")
    	return render(request, "some_template.html")
    if request.method == "POST":
        print("a POST request is being made to this route")
    	return redirect("/")
```
### Submitting Form Data

As you've already seen, getting information from a user via forms is an extremely important part of web development. While forms can be submitted as GET or POST requests, we'll typically use them to submit POST requests. In Django we will utilize the `request.POST`  to access any form data that is submitted. (If the form is a GET request, that data can be accessed with  `request.GET`.)
```py
from django.shortcuts import render, redirect
def some_function(request):
    if request.method == "GET":
    	print(request.GET)
    if request.method == "POST":
        print(request.POST)
```
One more important thing to note is that any forms being submitted as POST requests must include a CSRF token. This token is used to prevent cross-site request forgery, a malicious kind of attack where a hacker can pretend to be another user and submit data to a site that recognizes that user. Adding a CSRF token to our forms allows Django to add a hidden input field and value that helps our server recognize genuine requests. If you forget to add this, Django will kindly provide a clear error message if you attempt to submit a form without a token. Add a token to each form with this line:
```html
<form action="/some_route" method="post">
  {% csrf_token %}
  <p>Field One: <input name="one" type="text"></p>
  <p>Field Two: <input name="two" type="text"></p>
  <button type="submit">Submit</button>
</form>
```
Remember that the names of the input fields from our form will be the keys we use to access the data in our server. So given the above form, we should be able to retrieve these values:
```py
from django.shortcuts import render, redirect
def some_function(request):
    if request.method == "POST":
        val_from_field_one = request.POST["one"]
    	val_from_field_two = request.POST["two"]
```
#### External Resources

-   [Django documentation on CSRF tokens](https://docs.djangoproject.com/en/2.2/ref/csrf/)
-   [Wikipedia on cross-site request forgery](https://en.wikipedia.org/wiki/Cross-site_request_forgery)

# POST Form Submission

## Objectives:

-   Learn the purpose of HTML forms
-   Understand the action and method attributes of HTML forms
-   Learn how to handle POST requests in our methods
-   Learn how to access the form submission data in our server

----------

Up to this point, we have just been working with requests that display information  _from_  the server  _to_  the user. What if a request involves the client sending information  _to_  the server? The modern internet is user-driven; much of the actual content of a website is generated by the users of a website. How does a user provide content to a website? One word:  **forms**. HTML forms are the way in which users are able to pass data to the back end of a website, where the data can then be processed and stored. Processing form data correctly is a huge part of what it takes to become a back-end developer.

Let's create a new project called  **form_test**  with an app called  **form_app**. We'll use this in the next few sections. Don't forget to add your app to settings.py!

1.  The first thing to do is to create a route and a method that will show a page with a form on it. Use the following snippets to get set up quickly:
    

#### form_test/form_test/urls.py
```py
from django.urls import path, include
    
urlpatterns = [
    path('', include('form_app.urls')),
]
```
#### form_test/form_app/urls.py
```py
from django.urls import path
from . import views
                    
urlpatterns = [
    path('', views.index),
]
```
#### form_test/form_app/views.py
```py
from django.shortcuts import render
def index(request):
    return render(request,"index.html")
```
8.  Set up your template folder structure and create an index.html with the following form in the body:
    
    #### form_test/form_app/templates/index.html
    ```html
    <h1>Index Page</h1>
    <h3>Create a User</h3>
    <form action='/users' method='post'>
        {% csrf_token %}
        Name: <input type='text' name='name'>
        Email: <input type='text' name='email'>
        <button type='submit'>Create User</button>
    </form>
    ```
    Once you've done the above, start up your server and visit  _localhost:8000/_. you should see the index page with a form on it. Let's break down the critical parts of this form:
    
    -   #### action attribute
        
        This is the route that will  _process_  the form (not the one that shows the form--that's "/"). We'll set this up shortly.
        
    -   #### method attribute
        
        Our options are GET and POST; most likely, we'll want this to be a POST request (but if you don't set it, the default is GET)
        
    -   #### CSRF token
        
        This token is used to prevent cross-site request forgery, a malicious kind of attack where a hacker can pretend to be another user and submit data to a site that recognizes that user. Adding a CSRF token to our forms allows Django to add a hidden input field and value that helps our server recognize genuine requests. If you forget to add this, Django will kindly provide a clear error message if you attempt to submit a form without a token.
        
    -   #### input elements
        
        These are the parts of the form that actually gather data from the user. Check  [here](http://www.w3schools.com/tags/att_input_type.asp)  for type options. Also check here for other  [form elements](https://www.w3schools.com/html/html_form_elements.asp)  like select (dropdowns) and textarea.  _Each element should have a unique value for its  **name**  attribute._
        
    -   #### a way to submit the form
        
        This can either be  `<input type='submit'>`  or  `<button type='submit'>Submit</button>`, but NOT  `<input type='button'>`.
        
9.  Let's determine what should happen when the form is actually submitted. We indicated above, with the  **action**  attribute, that this POST request would be handled with the route  `/users`, so let's add this to route to our app urls.py:
    
    #### form_test/form_app/urls.py
    ```py
    from django.urls import path
    from . import views
                        
    urlpatterns = [
        path('', views.index),
        path('users',views.create_user)
    ]
    ```
    Now that we have the route, let's set up the method:
    
    #### form_test/form_app/views.py
    ```py
    from django.shortcuts import render
    def index(request):
        return render(request,"index.html")
            
    def create_user(request):
        print("Got Post Info....................")
        print(request.POST)
        return render(request,"index.html")
    ```
    The above method will print out a message and the form data to the terminal. Run your server and try submitting a form. What do you see in the terminal? You should see something like this:
    
    **<QueryDict: {'csrfmiddlewaretoken': ['Yh5hBKVirURud5syD3nrsRdEoME766Cml3Z2ED1M9z5sIi7gxeak0LJzSCalfX9v'], 'name': ['John'], 'email': ['john@doe.com']}>**
    
    Notice that the form data is being sent to our server in a dictionary. We see both the name and the email values that were input by the user. Let's modify our method to grab these values individually:
    ```py
    from django.shortcuts import render
    def index(request):
        return render(request,"index.html")
            
    def create_user(request):
        print("Got Post Info....................")
        name_from_form = request.POST['name']
        email_from_form = request.POST['email']
        print(name_from_form)
        print(email_from_form)
        return render(request,"index.html")
    ```
    Restart your server and try submitting the form again. What do you see in the terminal now? Notice how we were able to extract just the name and the email.
    
    -   ##### Accessing Data:  `request.POST['name_of_input']`
        
        **The name we gave to each HTML input was significant**. On the server-side, we can access data that was input into a field from a user through the  **request.post**  dictionary by providing the name of the input as the key. To see the entire form, you can print request.post.
        
        Lastly,  **note that the  _type_  of anything that comes in through request.post will be a "string" no matter what**. If you want that value to be identified as an actual number you'll have to  _type cast_  it.
        
10.  Finally, let's display this data on a new HTML page! We'll soon learn why it's not a great idea to render immediately as a response to a POST request, but more on that later.
    
     Make a new html file in your templates called show.html and add this code to the body:
    
		#### form_test/form_app/templates/show.html
		```html 
			<h1>Show Page</h1>
			<h3>Info Submitted:</h3>
			    <p>Name: {{ name_on_template }}</p>
			    <p>Email: {{ email_on_template }}</p>
		```
		   
		Next, modify your method in views.py:
    
		#### form_test/form_app/views.py
		```py
		    from django.shortcuts import render
		    def index(request):
		        return render(request,"index.html")
		            
		    def create_user(request):
		        print("Got Post Info....................")
		        name_from_form = request.POST['name']
		        email_from_form = request.POST['email']
		        context = {
		        	"name_on_template" : name_from_form,
		        	"email_on_template" : email_from_form
		        }
		        return render(request,"show.html",context)
		```
		Restart your server and submit the form! Do you see the data on the next page? Try adding more inputs and sending them over. It is important to become comfortable processing forms, so spend some time practicing.
		    

#### External Resources

-   [Django documentation on CSRF tokens](https://docs.djangoproject.com/en/2.1/ref/csrf/)
-   [Wikipedia on cross-site request forgery](https://en.wikipedia.org/wiki/Cross-site_request_forgery)

# More on Redirecting

## Objectives:

-   Understand when to use a redirect
-   Understand how to implement a redirect

----------

In the last reading, our form data was used right away on the next page, but this is not the best practice. We have to add a step between showing the form and displaying the form data. But why?

Let's go back to our form_test project. Our create_user method is the one processing the POST request. Run the project and submit the form. Hit the refresh button in your browser--you should see a pop up like the one below. The warning explains that we are sending the same form data to be processed again.

<img src="https://i.ibb.co/YyrxDTG/form-resubmit.png" border="0">

While it's not a big deal yet, imagine our method was inserting a user into the database, or processing a payment. Clicking  _continue_  would add that user to the database again, or process a payment twice. That would be no good!

To avoid this, we need to change the way we process forms from being a two-step process to the three-step process. The flow will end up looking like this:

1.  Set up a route and method that will render a template to show the form
2.  Set up a route and method to process the form data that will redirect
3.  Set up a route and method that will render a template indicating the form was successfully processed

Try changing your form_test project to follow the three steps. In addition to the following changes, make a success.html file that will display a success message to the user.

#### form_test/form_app/urls.py
```py
from django.urls import path
from . import views
                    
urlpatterns = [
    path('', views.index),
    path('create_user', views.create_user),
    path('success', views.success)
]
```
#### form_test/form_app/views.py
```py
from django.shortcuts import render, redirect # don't forget to import redirect!
def index(request):
    # this is the route that shows the form
    return render(request,"index.html")
def create_user(request):
    # this is the route that processes the form
    name_from_form = request.POST['name']
    email_from_form = request.POST['email']
    context = {
    	"name_on_template" : name_from_form,
    	"email_on_template" : email_from_form
    }
    return redirect("/success")
def success(request):
    # this is the success route
    return render(request,"success.html")
```
Now when we submit a form and hit refresh, we no longer receive the warning. Now, however, we've run into a new problem: we cannot send context over in a redirect, and once we redirect the form data is lost! Read on to learn one way we are able to hold on to, or persist data, across multiple requests!

# Assignment: Dojo Survey

## Objectives:

-   Practice creating a server with Django from scratch
-   Practice adding routes to a Django app
-   Practice having the client send data to the server with a form
-   Practice having the server render a template using data provided by the client

----------

Build a new Django application that accepts a form submission and presents the submitted data on a results page.

The goal is to help you get familiar with sending POST requests through a form and displaying that information. Consider the below example as a guide.

<img src="https://i.ibb.co/5K6wd0h/chapter2982-3795-survey-form.png" border="0">

When you build this, please make sure that your program meets the following criteria:

-   http://localhost:8000 - have this display a nice looking HTML form. The form should be submitted to '/result'
-   http://localhost:8000/result - have this display an HTML page with the information that was submitted by POST

**Don't forget that any inputs we want to be able to access from the form submission need to have a name!**

It's always a good idea to print request.POST to see if the form is delivering all the information you need in your routing method.

- [ ]  Create a new Django application
    
- [ ]  Have the root route ("/") show a page with the form
    
- [ ]  Have the "/result" route display the information from the form on a new HTML page
    
- [ ]  NINJA BONUS: Use a CSS framework to style your form
    
- [ ]  NINJA BONUS: Include a set of radio buttons on your form
    
- [ ]  SENSEI BONUS: Include a set of checkboxes on your form

# Session

## Objectives:

-   Introduce the concept of state
-   Introduce the need for persistence
-   Learn about sessions in the context of web development
-   Learn how Django handles session

----------

What are your thoughts on why our form data is gone after we redirect?

Remember back to algorithms and the Python Fundamentals chapter--when we had several functions in the same file, did they know anything about each other? Nope! It is no different here--each method that is handling a route doesn't know anything about any of the other routes.

Here's the thing about the HTTP request/response cycle: it is  **stateless**. That means that each request/response cycle is independent and ignorant of all other requests, before or after. Because we made a second request (by redirecting) after the client posted data in the form, the browser only knows about the second request we made (in our case, the GET request to the "/success" route). Because the form data was part of the first request, the second request has no access to it.

But certainly this is not our experience in the real world--when we go shopping online, the site seems to remember who we are, what items are in our shopping cart, etc. (Even other sites know what we've been shopping for! Creepy, right?) This is because many sites make use of  **persistent data storage!**  One form of persistence is  **session**.

## What is Session?

With session, we can establish a relationship with the client by saving, or writing, certain valuable pieces of data for use in future cycles. By reading that data we've stored in previous cycles, this opens up a new world of user experience. With session, the user can have a conversation of sorts with a website, where a user makes decisions that can be tracked so the server can create a more cohesive user experience.

In a given process (HTTP request/response), we can manage data (search terms and search results for instance) that  **outlives**  the process that generated it. This data is called  **state**. State allows our site to "know" a lot of useful information, like:

-   Whether there is a user logged in
-   Who the current user is
-   What links a user has viewed previously

We get to decide what to save about our clients--session is a tool for us, as developers, to use to our advantage. In the same way we create variables in our functions to help us solve problems, we keep state data in session to help us solve problems down the line, i.e. in subsequent HTTP requests.

Persistent data storage helps us bridge the gap between a stateless protocol like HTTP with the stateful data generated through it. This is at the heart of the modern web and is heavily used by web developers around the world.

Very shortly, we'll also discuss  **databases**  as another tool for persistent data storage. When we start incorporating a database into our projects, we'll consider what distinct roles each of these tools serve. We should not abuse the amount of information we store in session--store only what you need. Once we incorporate a database, we should be limiting what we store in session.

#### A Note on Cookies

You've probably heard of the term  **cookies**  before. Some frameworks, including Django, use cookies to store session data. Django uses secure hashing of session data to send a packet of information from server to client. This packet is known as a cookie. Once a client's browser has received this cookie, it writes the information contained in it to a small file on their hard drive.

While hashed, cookies are not incredibly secure, so don't save anything private in them.

## Using Session in Django

You may be itching to dismiss that warning about unapplied migrations. It's time! We'll talk about migrations more in depth when we integrate the database, but basically migrations help manage the state of our database, including creating and updating any tables. Django utilizes the database to manage sessions, so we'll need to update our database to allow for it to start maintaining session data for us. To do this, we'll run the following command from our terminal:
```
(djangoPy3Env) project_name> python manage.py migrate
```
Excellent. Not only does that annoying warning disappear, but now session is available to us as well (as seen in that last line:  `Applying sessions.0001_initial... OK`).

To use session, we can refer to it in our views.py file. Session is a dictionary to which we can add and retrieve values via keys, like so:

#### some_project/some_app/views.py
```py
def some_function(request):
    request.session['name'] = request.POST['name']
    request.session['counter'] = 100
```
We can also access session directly in our Django templates. Remember, though, that Django templates do not process square brackets, so we'll use dot notation instead:
```html
<p>Name in session is: {{request.session.name}}</p>
```
### Useful session methods:

-   `request.session['key']`
    -   This will retrieve (get) the value associated with `'key'`
-   `request.session['key'] = 'value'`
    -   Set the value that will be stored by  `'key'`  to 'value'
-   `'key' in request.session`
    -   Returns a  `boolean`  of whether a  `key`  is in  `session`  or not
-   `{{ request.session.name }}`
    -   Use dot notation (`.`) to access  `request.session`  keys from templates since square brackets (`[]`) aren’t allowed there
-   `del request.session['key']`
    -   Deletes a session key if it exists, throws a  `KeyError`  if it doesn’t. Use along with  `try`  and  `except`  since it's better to ask for forgiveness than permission
-   **Note**: If you are storing a list in session that is being modified (such as an append), you will need to save the session after the append, like so:
    -   `request.session['my_list'] = []`
    -   `request.session['my_list'].append("new item")`
    -   `request.session.save()`

# Assignment: Counter

## Objectives:

-   Practice using session to store data about a particular client's history with the app
-   Be able to check whether a session exists
-   Be able to initialize a session
-   Be able to modify a session

----------

Build a Django application that counts the number of times the root route ('/') has been viewed.

This assignment is to test your understanding of session.

<img src="https://i.ibb.co/nsKrfJF/chapter2982-3823-Screen-Shot-2015-08-18-at-2-34-59-PM.png" border="0">

As part of this assignment, please start with the following features first:

-   **localhost:8000**  - have the template render the number of times the client has visited this site
-   **localhost:8000/destroy_session**  - Clear the session. Once cleared, redirect to the root.

#### Some Helpful Tips

We can't increment something that doesn't exist! Here's how to check if a key exists in session yet:
```py
if 'key_name' in request.session:
    print('key exists!')
else:
    print("key 'key_name' does NOT exist")
```
If we want to get rid of what is currently stored in session:
```py
del request.session['key_name']	# clears a specific key
```
- [ ]  Create a new Django project called counter
    
- [ ]  Have the root route render a template that displays the number of times the client has visited this site. Refresh the page several times to ensure the counter is working.
    
- [ ]  Add a "/destroy_session" route that clears the session and redirects to the root route. Test it.
    
- [ ]  NINJA BONUS: Add a Reset button that uses the "/destroy_session" route
    
- [ ]  NINJA BONUS: Add a +2 button underneath the counter and a new route that will increment the counter by 2
    
- [ ]  SENSEI BONUS: Add a form that allows the user to specify the increment of the counter and have the counter increment accordingly
    
- [ ]  SENSEI BONUS: Adjust your code to display both how many times the user has actually visited the page, as well as the value of the counter, given the above functionality

# Assignment: Great Number Game

## Objectives:

-   Practice using session to store data about a client's history with the web app
-   Practice clearing a session
-   Practice having the server use data submitted by a client with a form

----------

I'm thinking of a number between 1 and 100...

Create a site that allows a user to play this guessing game. Upon loading, the server should "pick" a random number between 1-100; store the number in session. Allow the user to guess the number--tell them when they are too high or too low. If they guess the correct number, notify them and offer to play again.

There are many different ways to do this assignment. When you finish the basic functionality, find a peer and compare your code!

#### Reminder

In order to generate a random number you can use the  `[random](https://docs.python.org/3/library/random.html)`  Python module:

import random 	                # import the random module
random.randint(1, 100) 		# random number between 1-100

<img src="https://i.ibb.co/C55nKPb/chapter2240-3241-great-number-game.png"  border="0">

- [ ]  Create a new Django project called great_number_game
    
- [ ]  In the root route, save a random number between 1 and 100 and display a form for the user to guess the number
    
- [ ]  Create a route that determines whether the number submitted is too high, too low, or correct. Show this status on the HTML page.
    
- [ ]  NINJA BONUS: Display the results as shown in the wireframe above (i.e. with appropriate colors and positioning)
    
- [ ]  NINJA BONUS: Allow the user to keep guessing until they get it correct
    
- [ ]  NINJA BONUS: Let the user know how many attempts they took before guessing the correct number
    
- [ ]  SENSEI BONUS: Only allow the user to guess up to 5 times. If they don't guess it on their 5th attempt, display a "You Lose" message and allow them to try again.
    
- [ ]  SENSEI BONUS: If they win, allow the user to submit their name. Have a link to a leaderboard page that shows winners' names and how many attempts they took to guess correctly.

# Hidden Inputs

## Objectives:

-   Learn about hidden inputs
-   Learn how to add hidden inputs to a form

----------

Hidden input fields are  _form fields_ that are hidden from the user. Hidden input is used, along with other input elements, to transfer information between different pages.

A hidden input is just an ordinary input element, but has no visual representation in the rendered HTML.
```html
<input type="hidden" name="action" value="register">
```
There are multiple ways we can make use of the hidden input field. In this tab, we are going to look at just one example. Suppose we have two forms within our  **index** page:
```html
<form method="post" action="/process">
    {% csrf_token %}
    <input type="hidden" name="which_form" value="register">
    <input type="text" name="first_name">
    <input type="text" name="last_name">
    <input type="text" name="email">
    <input type="password" name="password">
    <input type="submit" value="Register">
</form>
<form method="post" action="/process">
    {% csrf_token %}
    <input type="hidden" name="which_form" value="login">
    <input type="text" name="email">
    <input type="password" name="password">
    <input type="submit" value="Login">
</form>
```
Notice that both forms submit their data to the POST /process route. How will we know which form was submitted? Each of the forms also has a hidden input with the same name, but different values. In this example, we are using the name "which_form".

In the  **POST** **/process route,** we could do something like this to process appropriately depending on which form was submitted:
```py
if request.POST['which_form'] == 'register':
  //do registration process
elif request.POST['which_form'] == 'login':
  //do login process
```
But know that,  **even though hidden inputs are invisible to the user, it is actually very visible in the page's source.**  That means other users can still see and change the values you set in the hidden input. So be very careful in choosing what data you store in there as value, and set appropriate actions if a user tries to change or remove it.


# Assignment: Ninja Gold

-   Practice passing data to a template
-   Practice using forms
-   Practice using Django session

----------

Recreate the Ninja Gold game, but this time with Django.

As a reminder, you're going to create a mini-game that helps a ninja make some money! When you start the game, your ninja should have 0 gold. The ninja can go to different places (farm, cave, house, casino) and earn different amounts of gold. In the case of a casino, your ninja can earn or lose up to 50 gold. Your job is to create a web app that allows this ninja to earn gold and to display past activities of this ninja.

### Guidelines

-   Refer to the wireframe below.
-   Have the four forms appear when the user goes to http://localhost:8000
-   Use a hidden input tag in each form to pass the relevant location to the server
-   Have  `/process_money`  determine how much gold the user should have
-   For now, save the activity log in session

<img src="https://i.ibb.co/gRNZ7Cn/chapter3832-6611-ninja-gold-ci.png"  border="0">

- [ ]  Create a new project/app
    
- [ ]  Have the root route render the main Ninja Gold page
    
- [ ]  Have the "/process_money" POST route increase/decrease the user's gold by an appropriate amount and redirect to the root route
    
- [ ]  NINJA BONUS: Refactor your code so the location is being passed in the URL rather than via a form
    
- [ ]  SENSEI BONUS: Have the user specify the win conditions before starting, and then implement them in the game (# of moves, goal for gold)

# Named Routes

## Objectives:

-   Learn about namespaces
-   Learn how to route using named routes

----------

**Named routes**  make referencing our Django routes pretty easy. All we need to do is pass a keyword variable (`name`) to the  `url`  method we use inside our app's `urls.py`  file. For example:

#### some_project/apps/some_app/urls.py
```py
from django.urls import path
from . import views
        
urlpatterns = [
    path('', views.toindex, name='my_index'),
    path('this_app/new', views.new, name='my_new'),
    path('this_app/<int:id>/edit', views.edit, name='my_edit'),
    path('this_app/<int:id>/delete', views.delete, name='my_delete'),
    path('this_app/<int:id>', views.show, name='my_show'),
]
```
Now we can more easily reference those routes from inside our app’s templates:

_NOTE_:  `target/`  in the examples below is what gets caught by our main project’s  `urls.py`
```html
<!-- Inside your app's index.html file -->
<a href="/target/this_app/new"></a>
<!-- is the equivalent of:  -->
<a href="{% url 'my_new' %}"></a>
<!-- This form's action attribute -->
<form class="" action="/target/this_app/5/delete" method="post">
  <input type="submit" value="Submit">
</form>
<!-- is the equivalent of: -->
<form class="" action="{% url 'my_delete' id=5 %}" method="post">
  <input type="submit" value="Submit">
</form>
```
Notice that in our form, the argument being passed will replace the named variable in the URL – pretty nifty. Thanks Django!

Now, one of the coolest things about Django is how we can mix, match and reuse all the different apps we (and others) create. But what if we're using routes with the same names in different apps? How can our project tell the difference? The answer is to add an app_name to your urls.py ([documentation](https://docs.djangoproject.com/en/2.2/topics/http/urls/#introduction)  here) argument to the routes you  **include** in your project's  **urls.py**  file. For example:

#### some_project/apps/courses_app/urls.py
```py
app_name = 'courses'
...
urlpatterns = [    
...
```
and

#### some_project/apps/login_reg_app/urls.py
```py
app_name = 'users'
...
urlpatterns = [    
...
```
Now it doesn't matter if the hypothetical **login_reg_app** and  **courses_app** each have named routes such as  **index**,  **create**, and  **show**. You can reference each one in any template like so:

#### some_project/apps/some_app/templates/some_app/some_template.html
```html
<a href="{% url 'courses:index' %}">This link will hit the index route in your courses_app</a>
<a href="{% url 'users:index' %}">And this link will hit the index route in your login_reg_app</a>
```
At this point, you've already completed a few Django assignments. Go back and refactor your code to take advantage of  **named routes.**


  
  
  

# Multiple Apps

## Objectives:

-   Practice creating Django apps
-   Get familiar with a Django project with multiple apps

----------

With Django, it's easy to create multiple apps that can be used across multiple projects. Let's say that you're a freelancer and have worked with many clients in the past. Say that almost every single project you've worked on, the client/project wants their own blogs, surveys, and user management system. Instead of having to re-create these modules each time from scratch, you decide to create three independent  _apps_  that you can utilize across all of these projects.

Add 2 additional apps,  **surveys**  and  **users**  to your project from the First Django Project assignment. (If you've forgotten how to create just an app, refer to all of step 5 (a-e) in the Creating a Django Project module.)

-   **blogs**  - update the routes as follows (content is the same):

-   /blogs - display the string "placeholder to later display a list of all blogs" with a method named "index"
-   /blogs/new - display the string "placeholder to display a new form to create a new blog" with a method named "new"
-   /blogs/create - redirect to the "/blogs" route with a method called "create"
-   /blogs/<number> - display the string "placeholder to display blog number: {{number}}" with a method named "show"
-   /blogs/<number>/edit - display the string "placeholder to edit blog {{number}}" with a method named "edit"
-   /blogs/<number>/delete - redirect to the "/blogs" route with a method called "destroy"

-   **surveys**

-   /surveys - display the string "placeholder to display all the surveys created"
-   /surveys/new - display "placeholder for users to add a new survey"

-   **users**

-   /register - display the string "placeholder for users to create a new user record"
-   /login - display the string "placeholder for users to log in"
-   /users/new - have the same method that handles /register also handle the url request of /users/new
-   /users - display the string "placeholder to later display all the list of users"

#### Hint:

Notice how the blogs and surveys routes all begin with the same pattern, but the users app routes do not. This means our project urls.py file should look something like this:

#### project_name/project_name/urls.py
```py
urlpatterns = [
    path('/blogs', include('blog_app.urls')),
    path('/surveys', include('survey_app.urls')),
    path('', include('users_app.urls')),
]
```
Then, in the respective blogs and surveys app urls.py files, we only need to include the remainder of the route to match!

**A reminder about redirecting: you should always provide the whole path, starting with the first /.**

  
  
  

- [ ]  Add a surveys app and a users app to your first Django project
    
- [ ]  Complete the /blogs route
    
- [ ]  Complete the /blogs/new route
    
- [ ]  Complete the /blogs/create route
    
- [ ]  Complete the /blogs/<number> route
    
- [ ]  Complete the /blogs/<number>/edit route
    
- [ ]  Complete the /blogs/<number>/delete route
    
- [ ]  Complete the /surveys route
    
- [ ]  Complete the /surveys/new route
    
- [ ]  Complete the /register route
    
- [ ]  Complete the /login route
    
- [ ]  Complete the /users/new route
    
- [ ]  Complete the /users route
    
- [ ]  NINJA BONUS: Have the root route utilize the same method as the /blogs route


