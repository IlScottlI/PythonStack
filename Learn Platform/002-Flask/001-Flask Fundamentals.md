# Overview

## Objectives:

-   Recap the past few days
-   Provide an outline of the concepts we'll be learning in Flask

----------

Congratulations on making it this far! Let's review the fundamental building blocks we have learned so far.

-   The syntax of  **Python**
-   The basic building blocks --  **variables, loops, lists, conditionals**
-   **Functions**  and how to use them
-   **OOP classes**  -- attributes, methods, and how to use them

In this chapter, we will use a micro-framework called Flask to teach you the main components of web applications. Here are the concepts we'll focus on in this chapter:

-   **Rendering Templates**
-   **Redirecting**
-   **Form data**
-   **GET & POST requests**
-   **Session**

# Flask Installation

## Objectives:

-   Install Flask in a virtual environment

----------

Let's install Flask. Flask is a micro-framework that we'll use to introduce and learn the main components of building web applications.

**With your virtual environment activated**, run this command in your terminal:

(py3Env) $ pip install Flask

After running this command, let's make sure we have successfully installed Flask by checking its version. In your terminal run the command  `flask --version`. Your terminal should output something like:

<img src="https://i.ibb.co/gzKwv7N/Screen-Shot-2018-03-23-at-11-04-58-AM.png" alt="Screen-Shot-2018-03-23-at-11-04-58-AM" border="0">

If you see something like the above, Flask is installed and you're ready to go! If not, consult your instructor.

# Hello, Flask!

## Objectives:

-   Build your first web server with Flask

----------

Let's start by building a basic "hello world" app in Flask:

1.  Make sure that the correct virtual environment is active, in which Flask is installed (see the installation chapter).
2.  Create an empty folder inside python_stack/flask/flask_fundamentals/ called "hello_flask".

-   This will be our project folder and the root directory for all of the files that we use to create the project.

4.  Inside the "hello_flask" folder, create a file called hello.py

-   This will be our "server" file where we will set up all of our routes to handle requests.
-   _You'll want to create a new folder  **for each assignment**  moving forward. It will seem tedious at first, but as we add additional files to each project, we'll want to keep everything organized by assignment/project!_

6.  Finally, put the following code inside of hello.py:

from flask import Flask  # Import Flask to allow us to create our app
app = Flask(__name__)    # Create a new instance of the Flask class called "app"
@app.route('/')          # The "@" decorator associates this route with the function immediately following
def hello_world():
    return 'Hello World!'  # Return the string 'Hello World!' as a response
if __name__=="__main__":   # Ensure this file is being run directly and not from a different module 
    app.run(debug=True)    # Run the app in debug mode.

Notice how we are accessing the app object and running the  _route_ method, passing in a string that is the route that we want to add to our application. You must do this for every route that you want to add to our application.

**Note:**  _Moving forward, you may see some red squiggly lines under your import statements because your text editor's linter doesn't recognize packages in your virtual environment. You can ignore them unless running the file actually gives you errors!_

<img src="https://i.ibb.co/RbhJCvR/red-squigglies.png" alt="red-squigglies" border="0">

Now run the application by navigating to your project directory and running the following command.  **Be sure the virtual environment is activated.**

(py3Env) $ python hello.py

Now if you navigate to localhost:5000/ in your browser, you should see the message "Hello World!"

You just created your first  **web server**!

Why are we going to localhost:5000? The Flask web server you created listens for an HTTP request on port 5000 (notice in your terminal that your code is constantly running). Whenever a request is sent to localhost:5000, the server looks at the URL being requested and sends the appropriate response. If we go to route "/", the hello_world() function will run. Since we (or the client) called the function, we receive what the function returns!

We also did a couple of important things in the code above:

-   **We imported the Flask class**. You will need this line in every application you build with Flask.
-   **We made an instance of the Flask class called "app"**. You will need this line in every application you build with Flask.
-   **We set up a routing rule using the "@" decorator with the route method: @app.route("/route_string")**. The routing rule is associated with the function immediately following it.
-   **Finally, we ran the app!**  This takes all of our routing rules that we set up and actually starts up the server.

# Routes

## Objectives:

-   Understand the importance of routes in web development
-   Understand the different parts of a route
-   Identify how and when to use GET requests

----------

Routes are an essential part of any web application. A route is much like a variable name we assign to a request. The job of a route is to communicate to the server what kind of information the client needs. This route name is attached to a route on our server that points towards a specific set of instructions. These instructions contain information about how to interpret the data being sent, the operations that need to be completed, and the response that should be sent back. These instructions are the code we'll be creating!

Every route has two parts:

1.  HTTP method (GET, POST, PUT, PATCH, DELETE)
2.  URL

## Setting up your Routes

Let's add another route to our hello.py file:
```py
# import statements, maybe some other routes
    
@app.route('/success')
def success():
  return "success"
    
    # app.run(debug=True) should be the very last statement! 
```
Now we have 2 routes--if the client requests localhost:5000/, the hello_world function will run. But if the client requests localhost:5000/success, the success function will run.

What if we wanted to be able to say "Hello, Michael" or "Hello, Amy" or "Hello, Wes"? We could make three routes, but that feels pretty repetitive. Also, every time we want to include someone else, we would need to create a new route. This is a great opportunity to add  **variable rules**  to our routes. For the example above, we could make the name a variable, like so:
```py
@app.route('/hello/<name>') # for a route '/hello/____' anything after '/hello/' gets passed as a variable 'name'
def hello(name):
    print(name)
    return "Hello, " + name
```
We can add as many of these as we need, giving each variable a different name:
```py
@app.route('/users/<username>/<id>') # for a route '/users/____/____', two parameters in the url get passed as username and id
def show_user_profile(username, id):
    print(username)
    print(id)
    return "username: " + username + ", id: " + id
```
The  `localhost:5000`  part of the route determines which server to call upon. The rest of the route, including the "/", tells the server which function should be invoked.

Although the code we show above is brief, we're bringing together a lot of concepts you've never seen before. Test out all the code snippets we've given you to this point to make sure you understand how everything's working. While it doesn't do much, you've created your first web application! The next assignment will help you practice these concepts. If you're having trouble piecing everything together, watch the video below to see all this code in action.

# Assignment: Understanding Routing

## Objectives:

-   Practice building a server with Flask from scratch
-   Get comfortable with routes and passing information to the routes

----------

Create a server file that generates the specified responses for the following url requests:

1.  localhost:5000**/**  - have it say "Hello World!"
2.  localhost:5000**/dojo**  - have it say "Dojo!"
3.  Create one url pattern and function that can handle the following examples:

-   localhost:5000**/say/flask**  - have it say "Hi Flask!"
-   localhost:5000**/say/michael**  - have it say "Hi Michael!"
-   localhost:5000**/say/john**  - have it say "Hi John!"

5.  Create one url pattern and function that can handle the following examples (HINT: int() will come in handy! For example int("35") returns 35):

-   localhost:5000**/repeat/35/hello**  - have it say "hello" 35 times
-   localhost:5000**/repeat/80/bye**  - have it say "bye" 80 times
-   localhost:5000**/repeat/99/dogs**  - have it say "dogs" 99 times

We hope you are feeling more comfortable with routes now!

- [ ]  Create a root route ("/") that responds with "Hello World!"
    
- [ ]  Create a route that responds with "Dojo!"
    
- [ ]  Create a route that responds with "Hi" and whatever name is in the URL after /say/
    
- [ ]  Create a route that responds with the given word repeated as many times as specified in the URL
    
- [ ] NINJA BONUS: For the 4th task, ensure the 2nd element in the URL is an integer (hint: http://exploreflask.com/en/latest/views.html#url-converters)
    
- [ ]  SENSEI BONUS: Ensure that if the user types in any route other than the ones specified, they receive an error message saying "Sorry! No response. Try again."

# Rendering Views

## Objectives:

-   Understand what templates are in Flask
-   Know where to save HTML files for a Flask application

----------

In the last assignment, we just returned simple strings. But we spent all that time in Web Fundamentals learning HTML--isn't that really what we want to return? You bet. We just need a place to save them so that our Flask server file knows where to find them. In Flask, we must create a directory alongside our hello.py file called  **templates**  (exactly this word, plural). Inside the templates directory, we'll add our HTML files. Going back to our hello_flask project:

#### /hello_flask/templates/index.html
```html
<h1>Hello Flask!</h1>  
```
Then in our code, we refer to our HTML files like so:

#### /hello_flask/hello.py
```py
from flask import Flask, render_template  # added render_template!
app = Flask(__name__)                     
    
@app.route('/')                           
def hello_world():
    # Instead of returning a string, 
    # we'll return the result of the render_template method, passing in the name of our HTML file
    return render_template('index.html')  
    
if __name__=="__main__":
    app.run(debug=True)                   
```
note the addition of render_template -- that allows us to return the rendered HTML that we created above. Now when we run our hello.py file and go to localhost:5000/, we'll see our template!

Here you can see that we are handling the  **root route**, or '/', route with the hello_world function which renders the index.html template. Here the HTTP verb is "GET".

# Template Engines

## Objectives:

-   Understand what a template engine is
-   Learn how to pass data from the server to the HTML
-   Learn the Jinja2 syntax for displaying data from the server in the HTML
-   Learn how to use Jinja2 to perform Python logic in the HTML

----------

While sometimes we'll want to render static HTML, we'll often want to pass data to allow for dynamic content on a given HTML file. Enter template engines. Since our browser doesn't understand Python code, the render_template function sends our HTML file--along with any data passed--through the template engine to resolve any code into HTML. The final product is the response to the client.

### Passing Data to the HTML

Let's see this in action by building off of our hello_flask project directory. Notice that in our render_template function call, we are now passing  _three_  arguments! The first one is still the name of the HTML file, but the other two have names and values:

#### hello_flask/hello.py
```py
from flask import Flask, render_template
app = Flask(__name__)
@app.route('/')
def index():
    return render_template("index.html", phrase="hello", times=5)	# notice the 2 new named arguments!
if __name__=="__main__":
    app.run(debug=True)
```
### Rendering Data on a Template

Now how do we use that data on the HTML? There are 2 special inputs we can use to insert Python-like code into our Flask templates.

-   {{  _some variable_ }}
-   {%  _some expression_ %}

Let's update our index.html file:

#### hello_flask/templates/index.html
```html
<h3>My Flask Template</h3>
<p>Phrase: {{ phrase }}</p>
<p>Times: {{ times }}</p>
      
{% for x in range(0,times): %}
    <p>{{ phrase }}</p>
{% endfor %}
      
{% if phrase == "hello" %}
  <p>The phrase says hello</p>
{% endif %}
```
<img src="https://i.ibb.co/nRp3CBh/template-engine.png" alt="template-engine" border="0">

In the above code, we used the different embedding tags to output some of our variables, insert a for-loop, and do some conditional checking with an if statement in our HTML template. It's especially important to see how we used the values that we passed into our template from our server file in the embedding tags.

These tags allow us to control what gets rendered (if statements), how many times something gets rendered (for loop) and printing values to our rendered html.

Although you technically  _can_  do a lot of logic in your templates, you should try to limit that logic as much as possible. Do the bulk of your logic in your Python code. If you put too much logic in your templates, you may slow down your server response time.

As we mentioned previously, Flask uses a templating engine called Jinja2. Jinja2 has a lot of great built-in features that allow us to place dynamic information on HTML pages. Check out the Jinja2 documentation here:  [Jinja2 Template Docs](http://jinja.pocoo.org/docs/dev/templates/)

**IMPORTANT NOTE: Using HTML comments (<!-- -->) will NOT comment out Jinja. You must use  [Jinja commenting syntax](http://jinja.pocoo.org/docs/2.10/templates/#comments)  instead.**

# Assignment: Playground

## Objectives:

-   Get comfortable passing information from the route to the template
-   Understand how to display information passed from the route in the template file
-   Get comfortable using for loops in the template file
-   Get comfortable using if statements in the template file

----------

## Internal Styling

_Just for this assignment_, use an internal stylesheet or inline CSS ([review here](https://www.w3schools.com/css/css_howto.asp)).

## Level 1

When a user visits  **http://localhost:5000/play**, have it render three beautiful looking blue boxes. Please use a template to render this.

<img src="https://i.ibb.co/St3fpCV/playground1.png" alt="playground1" border="0">

## Level 2

When a user visits  **localhost:5000/play/(x)**, have it display the beautiful looking blue boxes x times. For example, localhost:5000/play/7 should display these blue boxes 7 times. Calling localhost:5000/play/35 would display these blue boxes 35 times. Please remember that x originally is a string, and if you want to use it as an integer, you must first convert it to integer using int(). For example int("7") returns 7.

<img src="https://i.ibb.co/PjxXQg8/playground2.png" alt="playground2" border="0">

## Level 3

When a user visits  **localhost:5000/play/(x)/(color)**, have it display beautiful looking boxes x times, but this time where the boxes appear in (color). For example, localhost:5000/play/5/green would display 5 beautiful green boxes. Calling localhost:5000/play/35/red would display 35 beautiful red boxes.

<img src="https://i.ibb.co/d4CVrPc/playground3.png" alt="playground3" border="0">

- [ ]  Create a new Flask project
    
- [ ]  Have the /play route render a template with 3 blue boxes
    
- [ ]  Have the /play/<x> route render a template with x number of blue boxes
    
- [ ]  Have the /play/<x>/<color> route render a template with x number of boxes the color of the provided value
    
- [ ]  NINJA BONUS: Use only one template for the whole project

# Static Files

## Objectives:

-   Know what  _static content_  is in the context of web development
-   Know where to put static files in a Flask web application
-   Learn how to access our static content in our HTML files

----------

Static content is any content that can be served up to the client without being modified, generated, or processed by the server. Every framework will have its own way of serving static content. Flask serves static content from a directory called  **static**. Much like our  **templates**  directory,  **the static directory  _must_  be called static**. This static folder will be used to serve all of your  **stylesheets, images, and JavaScript files**.

Now, say we placed a CSS file, a JavaScript file, and an image directly into our static folder. We can then access them in our HTML templates, like so:
```html
<!-- based on the folder structure on the right -->
<!-- linking a css style sheet -->
<link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='my_style.css') }}">
<!-- linking a javascript file -->
<script type="text/javascript" src="{{ url_for('static', filename='my_script.js') }}"></script>
<!-- linking an image -->
<img src="{{ url_for('static', filename='my_img.png') }}">
```
<img src="https://i.ibb.co/3kXsQT0/static-structure.png" alt="static-structure" border="0">

**Note:**  although Flask knows to look for static files in the static directory, we must tell it when and where to do so, as shown above.

## Organization

It is common to create a few more folders to organize our static files into categories according to document type. We can call them  **css**,  **js**, and  **img** and house the corresponding files in the different folders. We can reflect these changes in our previous tags with the following changes in the href/src attributes. Notice the way we change the file name in the url_for function:
```html
<!-- linking a css style sheet -->
<link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/my_style.css') }}">
<!-- linking a javascript file -->
<script type="text/javascript" src="{{ url_for('static', filename='js/my_script.js') }}"></script>
<!-- linking an image -->
<img src="{{ url_for('static', filename='img/my_img.png') }}">
```
<img src="https://i.ibb.co/KzbrMsx/static-structure-2.png" alt="static-structure-2" border="0">

**Note: When using static files, your browser will likely cache them. If you are making changes in static files and they don't appear to be updating, do a  _hard refresh_  of the page in your browser:  `ctrl + shift + r`  (Windows) or  `cmd + shift + r`  (Mac).**


# Assignment: Checkerboard

## Objectives:

-   Continue to learn how to pass information from the url to the route
-   Practice linking static files to templates
-   Get comfortable passing information from the route to the template
-   Understand how to use for loop properly in the template
-   Recognize the value of creating a html/css first and then adding logic/code

----------

Now let's practice linking static files to our template. For this project, we'll render a template that displays a checkerboard:

![](http://mathworld.wolfram.com/images/eps-gif/Checkerboard_1000.gif)

Your program should have the following output

1.  http://localhost:5000 - should display 8 by 8 checkerboard
2.  http://localhost:5000/4 - should display 8 by 4 checkerboard
3.  http://localhost:5000/(x)/(y) - should display x by y checkerboard. For example, http://localhost:5000/10/10 should display 10 by 10 checkerboard. Before you pass x or y to Jinja, please remember to convert it to integer first (so that you can use x or y in a for loop)

**HINT: Remember that values from urls come in as strings by default. If you want to use the value in a loop, you should convert it to an integer before passing it to Jinja.**

## After you've worked on this assignment for 45 minutes...

If you watch this video without first struggling on your own to do this assignment, this video won't add much value for you. Please first spend 45 minutes to complete the assignment on your own. After you've spent 45 minutes on your own, then please watch this video for some advice on approaching problems generally and some tips for this assignment particularly.

_Note: In the video, we mention using an internal stylesheet. You know how to link static files, so practice using an external stylesheet!_

- [ ]  Create a new Flask project
    
- [ ]  Have the root route render a template with a checkerboard on it
    
- [ ]  Have the css in a separate stylesheet and link this to the template
    
- [ ]  Have another route accept a single parameter (i.e. "/<x>") and render a checkerboard with x many rows, with alternating colors
    
- [ ]  NINJA BONUS: Have another route accept 2 parameters (i.e. "/<x>/<y>") and render a checkerboard with x rows and y columns, with alternating colors
    
- [ ]  SENSEI BONUS: Have another route accept 4 parameters (i.e. "/<x>/<y>/<color1>/<color2>") and render a checkerboard with x rows and y columns, with alternating colors, color1 and color2

# More Template Rendering

## Objectives:

-   More practice rendering data on templates
-   Learn how to iterate through collections of data

----------

## Passing Lists to Jinja

So far we have just passed simple variables to our template. Let's update our hello_flask assignment by adding a new route and template.

#### hello_flask/hello.py
```py
@app.route('/lists')
def render_lists():
    # Soon enough, we'll get data from a database, but for now, we're hard coding data
    student_info = [
       {'name' : 'Michael', 'age' : 35},
       {'name' : 'John', 'age' : 30 },
       {'name' : 'Mark', 'age' : 25},
       {'name' : 'KB', 'age' : 27}
    ]
    return render_template("lists.html", random_numbers = [3,1,5], students = student_info)
```
Then in our template, let's loop through the list by doing something like this:
```html
#### hello_flask/templates/lists.html

    <h1>Random Numbers</h1>
    {% for number in random_numbers %}
        <p>{{ number }}</p>
    {% endfor %}
    <h1>Students</h1>
    {% for student in students %}
        <p>{{ student['name'] }} - {{ student['age'] }}</p>
    {% endfor %}
```
<img src="https://i.ibb.co/SKx51PZ/template-engine-lists.png" alt="template-engine-lists" border="0">


# Assignment: HTML Table

## Objectives:

-   Get comfortable passing information from the route to the template
-   Get very comfortable iterating through a list of dictionaries to generate a html output.

----------

Getting comfortable with iterating through a list of dictionaries is very important for all web development! Records returned from a database will almost always be in this format.

Create the following list of dictionaries and have it available for your route.
```js
users = [
   {'first_name' : 'Michael', 'last_name' : 'Choi'},
   {'first_name' : 'John', 'last_name' : 'Supsupin'},
   {'first_name' : 'Mark', 'last_name' : 'Guillen'},
   {'first_name' : 'KB', 'last_name' : 'Tonel'}
]
```
Pass users to your template and have your template output an HTML table like this:

| **First Name** | **Last Name** | **Full Name** |
|--|--|--|
| Michael | Choi |	Michael Choi |
| Scott | Johnson | Scott Johnson |
| John | Supsupin | John Supsupin |

As you need to get into the habit of making your assignment look nice, we challenge you to use either  [Bootstrap](https://getbootstrap.com/)  or  [Foundation](https://foundation.zurb.com/). If you haven't dabbled with these frameworks, start by learning just enough to do this assignment (creating a nice looking table).

-  [ ] Start a new Flask project
    
- [ ]  Create a route in which the data above is declared and then sent to the template engine to be rendered
    
- [ ]  Create the template that displays the data in a table
    
- [ ]  NINJA BONUS: Use a framework to format the table

# POST Form Submission

## Objectives:

-   Learn the purpose of HTML forms
-   Understand the action and method attributes of HTML forms
-   Learn how to allow POST requests in our Flask methods
-   Learn how to access the form submission data in our server

----------

Up to this point, we have just been working with requests that display information  _from_  the server  _to_  the user. What if a request involves the client sending information  _to_  the server? The modern internet is user-driven; much of the actual content of a website is generated by the users of a website. How does a user provide content to a website? One word:  **forms**. HTML forms are the way in which users are able to pass data to the back end of a website, where the data can then be processed and stored. Processing form data correctly is a huge part of what it takes to become a back-end developer.

Let's create a new project called  **form_test**. We'll use this in the next few sections. Go ahead and create the  `server.py`  file and a directory called  **templates**.

1.  The first thing to do is to write a function that will show a page with a form on it.
    
    #### form_test/server.py
    ```py
    from flask import Flask, render_template
    app = Flask(__name__)
    # our index route will handle rendering our form
    @app.route('/')
    def index():
        return render_template("index.html")
    if __name__ == "__main__":
        app.run(debug=True)
    ```
2.  That means our HTML page should have a form on it, so let's set that up:
    
    #### form_test/templates/index.html
	```html
    <h1>Index Page</h1>
    <h3>Create a User</h3>
        <form action='/users' method='post'>
        Name: <input type='text' name='name'>
        Email: <input type='text' name='email'>
        <input type='submit' value='create user'>
    </form>
	```
    Once you've done the above, start up your server and visit  _localhost:5000/_. you should see the index page with a form on it. Let's break down the critical parts of this form:
    
    -   #### action attribute
        
        This is the route that will  _process_  the form (not the one that shows the form--that's "/"). We'll set this up shortly.
        
    -   #### method attribute
        
        Our options are GET and POST; most likely, we'll want this to be a POST request (but if you don't set it, the default is GET)
        
    -   #### input elements
        
        These are the parts of the form that actually gather data from the user. Check  [here](http://www.w3schools.com/tags/att_input_type.asp)  for type options. Also check here for other  [form elements](https://www.w3schools.com/html/html_form_elements.asp)  like select (dropdowns) and textarea.  _Each element should have a unique value for its  **name**  attribute._
        
    -   #### a way to submit the form
        
        This can either be  `<input type='submit'>`  or  `<button>Submit</button>`, but NOT  `<input type='button'>`.
        
3.  Finally, let's determine what should happen when the form is actually submitted. We indicated above, with the  **action**  attribute, that this POST request would be handled with the route  `/users`, so let's add this to our server:
    
    #### form_test/server.py
    ```py
    from flask import Flask, render_template, request, redirect # added request
                
    @app.route('/users', methods=['POST'])
    def create_user():
        print("Got Post Info")
        print(request.form)
        name_from_form = request.form['name']
        email_from_form = request.form['email']
        return render_template("show.html", name_on_template=name_from_form, email_on_template=email_from_form)
    ```
    -   ##### Specifying Allowed Methods:  `methods=['POST']`
        
        If we don't provide a value for  `methods`, only GET requests are allowed. Everything we've done up to this point have been GET requests, so it has been okay, but since we want this method to handle POST requests, we must specify that. Notice it is a list--it's possible to provide more than one value.
        
    -   ##### Accessing Data:  `request.form['name_of_input']`
        
        **The name we gave to each HTML input was significant**. On the server-side, we can access data that was input into a field from a user through the  **request.form**  dictionary by providing the name of the input as the key. To see what's in your request object, try printing request.form.
        
        Lastly,  **note that the  _type_  of anything that comes in through request.form will be a "string" no matter what**. If you want that value to be identified as an actual number you'll have to  _type cast_  it.
        
4.  Let's display this data on a new HTML page! We'll soon learn why it's not a great idea to render immediately as a response to a POST request, but more on that later.
    
    #### form_test/templates/show.html
    ```html
    <h1>Show Page</h1>
    <h3>Info Submitted:</h3>
        <p>Name: {{ name_on_template }}</p>
        <p>Email: {{ email_on_template }}</p>
	```
## Video: Post Requests Conceptually


# Assignment: Dojo Survey

## Objectives:

-   Practice creating a server with Flask from scratch
-   Practice adding routes to a Flask app
-   Practice having the client send data to the server with a form
-   Practice having the server render a template using data provided by the client

----------

Build a new Flask application that accepts a form submission and presents the submitted data on a results page.

The goal is to help you get familiar with sending POST requests through a form and displaying that information. Consider the below example as a guide.

<img src="https://i.ibb.co/mDyVypK/chapter2982-3795-survey-form.png" alt="chapter2982-3795-survey-form" border="0">

When you build this, please make sure that your program meets the following criteria:

-   http://localhost:5000 - have this display a nice looking HTML form. The form should be submitted to '/result'
-   http://localhost:5000/result - have this display a html with the information that was submitted by POST

**Don't forget that any inputs we want to be able to access from the form submission need to have a name!**

It's always a good idea to print request.form to see if the form is delivering all the information you need in your routing method.

- [ ]  Create a new Flask application
    
- [ ]  Have the root route ("/") show a page with the form
    
- [ ]  Have the "/result" route display the information from the form on a new HTML page
    
- [ ]  NINJA BONUS: Use a CSS framework to style your form
    
- [ ]  NINJA BONUS: Include a set of radio buttons on your form
    
- [ ]  SENSEI BONUS: Include a set of checkboxes on your form

# Assignment: Dojo Fruit Store

## Objectives:

-   Practice using git (particularly git clone)
-   Get more comfortable with POST and passing information via a form
-   Understand how to reference static css or images
-   Note the importance of making your key assignments/projects look better
-   Understand why rendering HTML on a URL that received a POST is a bad idea

----------

Start by cloning the repo found here:  [https://github.com/mchoidojo/dojo_fruit_store](https://github.com/mchoidojo/dojo_fruit_store)

For this assignment, you'll be building a small web app as illustrated below:

<img src="https://i.ibb.co/9bs882y/dojo-fruit-store-wireframe.png" alt="dojo-fruit-store-wireframe" border="0">

## Overview Video

Note that the template allows you to use simple if statements and for loops, but is not really a place to do much more than that. If you're wanting to do any calculations, you would want to do this in the routing file (server.py).

Also, remember that all form inputs are received as strings. If you want to work with them as numbers, use the int() method to convert a string to an integer. For example:
```py
"1"+"2"+"3" # returns 123
int("1")+int("2")+int("3") # returns 6 
```
**Note for Mac Users:**

To get this code to run, you may have to add the following shebang to the top of your file to specify which version of Python to run on.

#!/usr/bin/env python3

You can read about shebangs and how they work [here](https://en.wikipedia.org/wiki/Shebang_(Unix)).

- [ ] Display all the provided images of fruit on the fruits.html page
    
- [ ]  When the Checkout button is clicked, have the correct information display on the checkout.html page
    
- [ ]  In the checkout method, add a print statement that says "Charging {{Customer name}} for {{count}} fruits"
    
- [ ]  While on the checkout screen, hit the refresh button in your browser. Then check your terminal--what do you notice?

# Redirecting

## Objectives:

-   Understand when to use a redirect
-   Understand how to implement a redirect

----------

The goal of the previous assignment was to give you a real example of why it is important to  _not_  render after a successful POST request. So what can we do instead? When we have finished processing the POST data, we can perform a GET request on behalf of the client, which will now be the request that is completed should the client refresh the page. This is called  _**redirecting**_.  **Always redirect after handling POST data to avoid data being handled more than once!**

Let's see how it works by going back to our form_test project. Our create_user method is the one processing the POST request. Run the project and submit the form. Hit the refresh button in your browser--you should see a pop up like the one on the right. The warning explains that we are sending the same form data to be processed again. While it's not a big deal yet, imagine our method was inserting a user into the database. Clicking  _continue_  would add that user to the database again. That would be no good!

<img src="https://i.ibb.co/F01bvVk/form-resubmit.png" alt="form-resubmit" border="0">

Let's add a separate method that will be solely responsible for rendering the show page, and then change the last line of our method handling the POST data from  `render_template`  to  `redirect`  to the route that will render the page:
```py
from flask import Flask, render_template, request, redirect # don't forget to import redirect!
    
@app.route('/users', methods=['POST'])
def create_user():
    print("Got Post Info")
    print(request.form)
    name = request.form['name']
    email = request.form['email']
    return redirect("/show")	# changed this line!
    
# adding this method
@app.route("/show")
def show_user():
    print("Showing the User Info From the Form")
    print(request.form)
    return render_template("show.html")
```
Now when we submit a form and hit refresh, we no longer receive the warning. Now, however, we've run into a new problem. Check the terminal to see what prints from our show_user method--the form data is empty! Why do you think this is?

Read on to learn one way we are able to hold on to, or  _persist_  data, across multiple requests!

### In Video Form:


# Session

## Objectives:

-   Introduce the concept of state
-   Introduce the need for persistence
-   Learn about sessions in the context of web development

----------

What were your thoughts on why  `request.form`  was empty after redirecting?

Remember back to algorithms and the Python Fundamentals chapter--when we had several functions in the same file, did they know anything about each other? Nope! It is no different here--each method that is handling a route doesn't know anything about any of the other routes.

Here's the thing about the HTTP request/response cycle: it is  **stateless**. That means that each request/response cycle is independent and ignorant of all other requests, before or after. Because we made a second request (by redirecting) after the client posted data in the form, the browser only knows about the second request we made (in our case, the GET request to the "/show" route). Because the form data was part of the first request, the second request has no access to it.

But certainly this is not our experience in the real world--when we go shopping online, the site seems to remember who we are, what items are in our shopping cart, etc. (Even other sites know what we've been shopping for! Creepy, right?) This is because many sites make use of  **persistent data storage!**  One form of persistence is  **session**.

## What is Session?

With session, we can establish a relationship with the client by saving, or writing, certain valuable pieces of data for use in future cycles, and by reading that data we've stored in previous cycles. This opens up a new world of user experience. With session, the user can have a conversation of sorts with a website, where a user makes decisions that can be tracked so the server can create a more cohesive user experience.

In a given process (HTTP request/response), we can manage data (search terms and search results for instance) that  **outlives**  the process that generated it. This data is called  **state**. State allows our site to "know" a lot of useful information, like:

-   Whether there is a user logged in
-   Who the current user is
-   What links a user has viewed previously

We get to decide what to save about our clients--session is a tool for us, as developers, to use to our advantage. In the same way we create variables in our functions to help us solve problems, we keep state data in session to help us solve problems down the line, i.e. in subsequent HTTP requests.

Persistent data storage helps us bridge the gap between a stateless protocol like HTTP with the stateful data generated through it. This is at the heart of the modern web and is heavily used by web developers around the world.

Very shortly, we'll also discuss  **databases**  as another tool for persistent data storage. When we start incorporating a database into our projects, we'll consider what distinct roles each of these tools serve. We should not abuse the amount of information we store in session--store only what you need. Once we incorporate a database, we should be limiting what we store in session.

#### A Note on Cookies

You've probably heard of the term  **cookies**  before. Some frameworks, including Flask, use cookies to store session data. Flask uses secure hashing of session data to send a packet of information from server to client. This packet is known as a cookie. Once a client's browser has received this cookie, it writes the information contained in it to a small file on their hard drive.

While hashed, cookies are not incredibly secure, so don't save anything private in them.

## Setting Up Session in Flask

With our form_test project open, let's import session:

#### form_test/server.py
```py
from flask import Flask, render_template, request, redirect, session
```
To use sessions in Flask, we are also required to give our app a  [secret key](http://flask.pocoo.org/docs/1.0/config/#SECRET_KEY):

#### form_test/server.py
```py
app = Flask(__name__)
app.secret_key = 'keep it secret, keep it safe' # set a secret key for security purposes
```
Because the create_user method is the method in which we receive the information from the POST request, let's write the information to session in this method:

#### form_test/server.py
```py
@app.route('/users', methods=['POST'])
def create_user():
    print("Got Post Info")
    # Here we add two properties to session to store the name and email
    session['username'] = request.form['name']
    session['useremail'] = request.form['email']
    return redirect('/show')
```
Previously in our show_user function, we didn't have access to the name and email from the form submission. Now, because of session, we have a way to access the name and email in a different function!

Let's modify our show_user function:

#### form_test/server.py
```py
@app.route('/show')
def show_user():
    return render_template('show.html', name_on_template=session['username'], email_on_template=session['useremail'])
```
Test out our application now!

#### Session in Templates

Right now we are passing the information stored in session to the templates using named arguments. Session data is also available directly in our templates. That means we can do this:

#### form_test/server.py
```py
@app.route('/show')
def show_user():
    return render_template('show.html')
```
#### form_test/templates/show.html
```html
    <h1>User:</h1>
    <h3>{{session['username']}}</h3>
    <h3>{{session['useremail']}}</h3>
```
#### Conceptual Session Overview


# Assignment: Counter

## Objectives:

-   Practice using session to store data about a particular client's history with the app
-   Be able to check whether a session exists
-   Be able to initialize a session
-   Be able to modify a session

----------

Build a flask application that counts the number of times the root route ('/') has been viewed.

This assignment is to test your understanding of session.

<img src="https://i.ibb.co/9ySMDrF/chapter2982-3823-Screen-Shot-2015-08-18-at-2-34-59-PM.png" alt="chapter2982-3823-Screen-Shot-2015-08-18-at-2-34-59-PM" border="0">

As part of this assignment, please start with the following features first:

-   **localhost:5000**  - have the template render the number of times the client has visited this site
-   **localhost:5000/destroy_session**  - Clear the session. Once cleared, redirect to the root.

#### Some Helpful Tips

We can't increment something that doesn't exist! Here's how to check if a key exists in session yet:
```py
if 'key_name' in session:
    print('key exists!')
else:
    print("key 'key_name' does NOT exist")
```
If we want to get rid of what is currently stored in session:
```py
session.clear()		# clears all keys
session.pop('key_name')		# clears a specific key
```
- [ ]  Create a new Flask project called counter
    
- [ ]  Have the root route render a template that displays the number of times the client has visited this site. Refresh the page several times to ensure the counter is working.
    
- [ ]  Add a "/destroy_session" route that clears the session and redirects to the root route. Test it.
    
- [ ]  NINJA BONUS: Add a +2 button underneath the counter and a new route that will increment the counter by 2
    
- [ ]  NINJA BONUS: Add a Reset button to reset the counter
    
- [ ]  SENSEI BONUS: Add a form that allows the user to specify the increment of the counter and have the counter increment accordingly
    
- [ ]  SENSEI BONUS: Adjust your code to display both how many times the user has actually visited the page, as well as the value of the counter, given the above functionality
    
- [ ]  SENSEI BONUS: Decode the cookie information as shown in the video

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

<img src="https://i.ibb.co/HNHBtSS/chapter2240-3241-great-number-game.png" alt="chapter2240-3241-great-number-game" border="0">

- [ ]  Create a new Flask project called great_number_game
    
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
    <input type="hidden" name="which_form" value="register">
    <input type="text" name="first_name">
    <input type="text" name="last_name">
    <input type="text" name="email">
    <input type="password" name="password">
    <input type="submit" value="Register">
</form>
<form method="post" action="/process">
    <input type="hidden" name="which_form" value="login">
    <input type="text" name="email">
    <input type="password" name="password">
    <input type="submit" value="Login">
</form>
```
Notice that both forms submit their data to the POST /process route. How will we know which form was submitted? Each of the forms also has a hidden input with the same name, but different values. In this example, we are using the name "which_form".

In the  **POST** **/process route,** we could do something like this to process appropriately depending on which form was submitted:
```py
if request.form['which_form'] == 'register':
  //do registration process
elif request.form['which_form'] == 'login':
  //do login process
```
But know that,  **even though hidden inputs are invisible to the user, it is actually very visible in the page's source.**  That means other users can still see and change the values you set in the hidden input. So be very careful in choosing what data you store in there as value, and set appropriate actions if a user tries to change or remove it.

# Assignment: Ninja Gold

## Objectives:

-   Practice using session
-   Practice having the server use data sent by the client in a form
-   Practice using hidden inputs

----------

Create a simple game to test your understanding of Flask, and implement the functionality below.

For this assignment, you're going to create a mini game that helps a ninja make some money! When you start the game, your ninja should have 0 gold. The ninja can go to different places (farm, cave, house, casino) and earn different amounts of gold. In the case of a casino, your ninja can earn  _or lose_  up to 50 gold. Your job is to create a web app that allows this ninja to earn gold and to display their past activities.

The root route should display the wireframe below. There should be 4 forms on the HTML page. As an example, the farm form might look something like this:
```py
<form action="/process_money" method="post">
  <input type="hidden" name="building" value="farm" />
  <input type="submit" value="Find Gold!"/>
</form>
```
There should be a method that handles the POST request, determining how much gold the user should now have depending on their visit.

Note: You should only have  **2 routes**  for this assignment -- '/' and '/process_money'

<a href="https://ibb.co/5Wvmz55"><img src="https://i.ibb.co/DDkh677/chapter3677-6302-ninja-gold-ci.png" alt="chapter3677-6302-ninja-gold-ci" border="0"></a>

## Watch this before you start the assignment

## A Helpful Tip

Consider the following code:

#### my_proj/server.py
```py
def index():
    message = "<ul><li>Hello</li></ul>"
    return render_template("index.html", message=message)
```
#### my_proj/templates/index.html
```html
{{ message }}

<a href="https://imgbb.com/"><img src="https://i.ibb.co/Snc6Ns0/unsafe.png" alt="unsafe" border="0"></a>

{{ message|safe }}
```
<img src="https://i.ibb.co/gTjFn3n/safe.png" alt="safe" border="0">

By default, Jinja will convert any  [html entities with character entities](https://www.w3schools.com/html/html_entities.asp). To prevent this from happening, we used the  `safe`  pipe, which you can read about  [in the Flask documentation](http://jinja.pocoo.org/docs/2.10/templates/#working-with-automatic-escaping)  and  [on StackOverflow](https://stackoverflow.com/questions/12341496/jinja-2-safe-keyword).

- [ ]  Create a new Flask project called ninja_gold
    
- [ ]  Create the template as shown in the wireframe above, with 4 separate forms
    
- [ ]  Have the root route render this page
    
- [ ]  Have the "/process_money" POST route increase/decrease the user's gold by an appropriate amount and redirect to the root route
    
- [ ]  NINJA BONUS: Display all the activities performed by the user in a log on the HTML, as shown in the wireframe
    
- [ ]  NINJA BONUS: Have the activities be color-coded as shown above (+ money is green, - money is red)
    
- [ ]  NINJA BONUS: Add a reset button to restart the game
    
- [ ]  SENSEI BONUS: Have the activities display in descending order, with the most recent activity first
    
- [ ]  SENSEI BONUS: Provide winning parameters to the game--for example, a user must obtain 500 gold in less than 15 moves. Only display the reset button once the user has won or lost.
    
- [ ]  SENSEI BONUS: Complete the "/process_money" route without 4 conditional statements (i.e. without doing if farm...elif cave...etc.)
