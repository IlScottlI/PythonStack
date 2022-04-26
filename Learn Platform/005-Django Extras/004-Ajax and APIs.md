# Django w/ Ajax

By now we’ve gotten fairly comfortable building full-fledged Django applications. Well done!

There is, however, an issue we haven’t yet addressed – one that’s  **essential**  to building modern web applications. Here’s the problem: In all our applications to date, we’ve needed to refresh the browser each time we emit an HTTP request. Every time we’ve clicked a link to view a specific user’s profile; every time we’ve submitted a form – it’s all gone hand in hand with a page reload.

To illustrate this issue, build a simple Django project/app according to the wireframe below. Don't worry about AJAX yet, just build a Django web app with the tools you've learned so far:

### Note:

> At this point, just ignore the yellow Post-It note – We’ll deal with that feature soon enough.

<img src="https://i.ibb.co/tZNq2D2/chapter3844-6677-ajax-posts.png" border="0">

# Introducing JavaScript

In the previous tab, you built (probably pretty quickly!) an app to create and view posts. That activity was meant to get you to notice a problem we’ve already mentioned:

> Every time we add a post, the page refreshes in order to display the most up-to-date posts.

That’s generally considered poor user experience, so let’s step in with some JavaScript.

We’ll use  `jQuery`/`$`  for its super easy syntax – either download a local copy or link to CDN – and stop our  `<form>`  from issuing an HTTP request when submitted.

All we really need to do is update the code in our  `template`  file:
```html
{% load staticfiles %}
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Ajax Posts</title>
    <!-- GRAB jQUERY -->
    <script src="LOCAL JQUERY FILE OR CDN LINK"></script>
    <!-- ******************* -->
    <link rel="stylesheet" href="{% static 'css/styles.css' %}">
  </head>
  <body>
    <h1>Posts</h1>
    <div class="posts">
      <!-- posts is fed to the template via a context dictionary (see app's views.py file for details) -->
      {% for post in posts %}
      <div class="post">
        <p>{{post.description}}</p>
      </div>
      {% endfor %}
    </div>
    <form action="{%url 'posts' %}" method="post">
      {% csrf_token %}
      {{new_post_form.as_p}}
    <input type="submit" value="Add New Post">
  </form>
  </body>
  <!-- NOW LET'S ADD SOME JAVASCRIPT TO STOP FORM SUBMISSION! -->
  <script>
    // You could also put this code in another JavaScript file... Remember to user $(document).ready() if the script tag is included before the DOM nodes you care about...
    $('form').submit(function(e){
      // preventDefault stops the default action of the event (e) from being triggered.
      e.preventDefault();
      console.log("Form submitted but no HTTP request sent to server!");
    });
  </script>
  <!-- ********************************* -->
</html>
```
OK, we’ve severed the default tie between HTML  `<form>`  and our server. Just one problem: How do we get our JavaScript code to send off the request instead?

### Enter  **Ajax**

One of the most important techniques for building modern web apps, Ajax requests allow us to communicate with the server  _in the background_  of other activity. That means our users can submit a form, for example, and still be able to do things like scroll up and down the page and interact with other parts of our website.

We could create these requests with  [vanilla JavaScript](https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest), but it’s relatively tedious compared to a build-in  `ajax`  method that jQuery gives us:

Let’s invoke that method (attached to the  `$`  object) and pass it an object describing the type of request we’d like it to initialize.

Take a look at the incomplete code below and see if you can fill in the missing pieces before moving to the next tab. This  [documentation](http://api.jquery.com/jquery.ajax/)  might be helpful.
```js
$('form').submit(function(e){
  e.preventDefault()
  $.ajax({
    url: /* Where should this go? */,
    method: /* Which HTTP verb? */,
    data: /* Any data to send along? */,
    success: /* What code should we run when the server responds? */
  })
})
```

# Connecting Ajax

If you came up with something like the following code, nice job!
```js
$('form').submit(function(e){
  e.preventDefault()
  $.ajax({
    url: '/posts/',
    method: 'post',
    data: $(this).serialize(),
    success: function(serverResponse){
      console.log("Received this from server: ", serverResponse)
      console.log("I should probably put that in the DOM...")
    }
  })
})
```
> If you haven’t seen the  `.serialize()`  method, it’s just a helpful way to create a text string that our server can easily parse.

Pause for a moment to really think about the following: You just added some JavaScript to take care of an HTTP request/response on the front-end; at this point  _you haven’t changed a single line of code on the server-side_. Remember: The server  **doesn’t care**  whether a request is initiated via your browser’s address bar, an HTML  `<form>`  submission or an Ajax method.

Likewise, we didn’t change any of the HTML that our server rendered! The  `<form>`  is still created the same as before (the example repo uses Django’s  `forms.ModelForm`  feature).

### Acronym break

This is probably as good a time as any to mention what Ajax stands for:  **Asynchronous Javascript And XML**. That’s a bit of a mouthful; the important thing to remember about this technique is that we’re running code  _asynchronously_, i.e. the  `function`  we attached to the  `success`  key only runs when the server responds. That’s why they’re known as  **callback**  functions – it’s code the JavaScript engine can call back to at the right time.

Now back to business. If you logged the server’s response, you’ll notice we’re responding with the HTML that our server generates from rendering a template.

The problem with the current state of things is that we don’t need the entire HTML file! All we really care about is the section with the posts, and one strategy to deal with this is to make a partial template that holds only that code:
```html
<!-- Inside a new template that we'll call posts_index.html -->
<div class="posts">
  {% for post in posts %}
  <div class="post">
    <p>{{post.description}}</p>
  </div>
  {% endfor %}
</div>
```
Now let’s refactor our  `views`  so that a GET request to  `/posts`  renders the new template. Let’s also make a root route that will render the full  `index.html`  page and update our  `urls.py`  files accordingly.

Here are our views:
```py
def index(request):
  """
  Fetch all posts and render full index page with form
  """
  context = {
      'posts': Post.objects.all(),
      'new_post_form' : PostForm()
  }
  return render(request, 'ajax_posts_app/index.html', context)
def post(request):
if request.method == 'POST':
  """
  Create new post and redirect to posts_index route
  """
  bound_form = PostForm(request.POST)
  """
  Check valid description
  """
  if bound_form.is_valid():
      Post.objects.create(description=request.POST['description'])
"""
We do this on both GET and POST requests
Fetch all posts and render only the partial posts_index.html
"""
context = {
		'posts': Post.objects.all()
}
return render(request, 'ajax_posts_app/posts_index.html', context)
```
And here are our urls:

#### App-level urls
```py
# Inside the app's urls.py file
urlpatterns = [
    path('', views.index, name='index'),
    path('posts', views.post, name='posts'),
]
```
#### Project-level urls
```py
# Inside the app's urls.py file
urlpatterns = [
    # The admin url came with our project -- we haven't used it yet
    path('admin/', admin.site.urls),
    path('', include('ajax_posts_app.urls')),
]
```
### Update the DOM

The only thing left to do is have our JavaScript put the actual response into the DOM:
```js
// Inside the $.ajax() call
success: function(serverResponse){
          // Replace the html inside a div with the class "posts" with the server response
          $('.posts').html(serverResponse)
        }
```
That’s all it takes! Hopefully, you can see the power of using Ajax requests to give your app a sleeker feel. Here’s a diagram that tracks the data flow of an Ajax request:

1.  Form submitted by user
2.  Ajax request sent to server w/ form data
3.  Server catches  `POST`  route to  `/posts`  and runs  `post`  method
4.  `post`  method creates new post and returns a rendered partial to the browser

Finally, the callback function pinned to the  `success`  key runs with the server response passed in as an argument and updates DOM.

<img src="https://i.ibb.co/vwLRcr2/chapter3844-6675-ajax-process.png" border="0">

# Assignment: Ajax Notes

Create a Django Note Manager Application where you can add, edit and delete a note. When you’re building applications, understanding how many forms you need can be a huge help:

Look at the image below and ask yourself how many forms you might need for the assignment…

<img src="https://i.ibb.co/HzshxnL/chapter3844-6676-ajax-notes.png" border="0">

If you said 3, we’re on the same page:

1.  Form for creating a note
2.  For every note, a form for creating/updating that note’s description

-   Extra challenge: implement this feature without showing a submit  `button`

3.  For every note, a form for deleting that note

One piece of advice that students generally find  **extremely**  helpful:

Build this app without using  _any_  JavaScript/Ajax calls initially. Once everything is working, refactor your code with Ajax calls.

#### Extra

-   Implement database validations and flash messaging

# Returning JSON

Up to this point, we’ve cut off a default browser action (i.e. stop a  `<form>`  from shooting off an HTTP request and page-reload) with JavaScript and used it (via  `jQuery`) to manage the request/response with an Ajax request.

Besides adding a new template and refactoring our  `urls.py`  files, we didn’t touch our server-side code. That means it’s returning the same thing to the browser that it always has: A  **string**  that our browser understands can be interpreted as HTML tags and content.

Basically, we’re sending HTML back to the JavaScript that’s handling the response, and that can be annoying in certain situations:

1.  We’re expecting other applications to send our server HTTP requests to get information
2.  We want to generate the HTML on the front-end, perhaps using client-side frameworks like Angular or React

Returning a string of HTML code is annoying because it’s hard to parse, unlike, say a JavaScript object.

Go ahead and paste the following url into your browser’s address bar:

-   [https://api.github.com/users/MikeHannon/repos](https://api.github.com/users/MikeHannon/repos)

We just hit one of Github’s servers with a  `GET`  request. How’d we know the correct pattern to use when asking for Mike Hannon’s repositories? By  [reading the docs](https://developer.github.com/v3/repos/)! Github  _could have_  chosen to respond with HTML tags that our browser could read, but they – thankfully – instead gave us something that our JavaScript can parse as an object!
```js
// Response from https://api.github.com/users/M...
[
  {
    id: 56562824,
    name: "4.PHP_MVP",
    full_name: "MikeHannon/4.PHP_MVP",
    owner: {
    login: "MikeHannon",
    id: 7180431,
    avatar_url: "https://avatars.githubusercontent.com/u/7180431?v=3",
    // ...More stuff...
  },
// ...More stuff...
]
```
The name for this type of data formatting is called  **JSON**  (JavaScript Object Notation), and it easily allows us to iterate through a server response (notice we received an  `array`  from Github) and pick and choose the key/value pairs that we want to access.

There are plenty of free public APIs that you can reach out to via Ajax requests to enhance your own applications. While every URL pattern will be different – requiring you to read documentation to figure out how to get the information you want – adhering to a RESTful URL pattern is super helpful.

Take some time to explore the following external APIs:

-   [Open Weather Map](http://openweathermap.org/api)
-   [GitHub API](https://developer.github.com/v3/)
-   [Google Maps Directions API](https://developers.google.com/maps/documentation/directions/)
-   [Twitter API](https://dev.twitter.com/rest/public)
-   [Flickr API](https://www.flickr.com/services/api/)

The benefits of pulling an external API into your app are enormous. You can stand on the shoulders of giants to leverage what’s already been built to make your app even better.

It’s up to you to decide which type of data you’d like your server to respond with.

In general:

-   Respond with HTML templates when there aren’t too many pieces of data to track and no other domains will be querying your server.
-   Respond with JSON if you’ll be accepting HTTP requests from other domains or if you’re using a front-end framework like Angular or React.

Most importantly: Experiment with different strategies!


# Building HTML

What if we wanted to display the JSON data onto our website instead of just logging it to our console?

We are going to be using the pokemon api to get our JSON objects:

[https://pokeapi.co/](https://pokeapi.co/)

# In this example:

We can include the data from JSON object into our HTML so that the users of our website can see that Bulbasaur’s types are poison and grass.
```html
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Gotta Catch'em All</title>
        <script src="https://code.jquery.com/jquery-2.1.3.min.js"></script>
        <script>
            $(document).ready(function(){
                $.ajax({
                  url:"http://pokeapi.co/api/v2/pokemon/1",
                  method:"get",
                  success:function(response){
                      var html_str = "";
                      html_str += "<h4>Types</h4>";
                      html_str += "<ul>";
                      for(var i = 0; i < response.types.length; i++) {
                          html_str += "<li>" + response.types[i].type.name + "</li>";
                      }
                      html_str += "</ul>";
                      $("#bulbasaur").html(html_str);
                  }
                },
                "json");
            })
        </script>
    </head>
    <body>
        <div id="bulbasaur">
        </div>
    </body>
</html>
```
Parsing through JSON objects can be a bit tedious. A good starting strategy is to console.log the whole object, and then parse through using console.log. In the example above, we might start by console.logging the whole response, and then response.types and then response.types[0] and then response.types[0].type…

### Note:

When we are making a call to an external server, the AJAX side is almost all JavaScript (no python needed); however, some external servers check to see whether the call is made from another server (e.g. a template that is served by a server) versus just a file. This can lead to Cross Origin Request Errors (CORS) (The Pokemon API is not restrictive in this sense, but other sites can be!)

### Note 2:

Because AJAX GETs and POSTs are very common, jQuery has made a short hand method for calling them - here’s a link to explore! Feel free to refactor the above code, using the  `$.get`  syntax.

[https://api.jquery.com/jquery.get/](https://api.jquery.com/jquery.get/)  [https://api.jquery.com/jquery.post/](https://api.jquery.com/jquery.post/)


# Pokemon Basics

Now that we have a basic understanding of AJAX requests, let’s use it to make a Django pokemon app (We know that you could do this without even making an Django app, but make it an app anyways).

The simple version of this app is below (it just shows all of the first 500 pokemon, and allows you to click on them - showing their attributes in the red box (the box can be populated through an AJAX call)):

#### Note:

Pokemon image links can be found in the sprite attribute of the pokemon object.

<img src="https://i.ibb.co/jzgsN1G/chapter3844-6720-3025n48.png" border="0">

<img src="https://i.ibb.co/HCyXVMM/chapter3844-6719-35cgzgm.png" border="0">

<img src="https://i.ibb.co/ctrXrhf/chapter3844-6721-ajax-pikachu.png" border="0">

How do you know which Pokemon was clicked? Maybe we can give each Pokemon a unique id that corresponds with their number in the URL?

When the image is clicked, we get its id and add it to the end of the url, then we make the AJAX request with that URL that we constructed.

The above app is a great start!

For an advanced version, add in one of your many login and registration apps, have a user be able to capture Pokemon (maybe a many to many relationship that stores pokemon ids). You could then randomly spawn Pokemon somewhere on your page (random number, random x,y and use the random number to make an ajax call to the Pokemon API), and when you click on them, they disappear, get added to the collection of Pokemon the user currently has… You could have 2 pages (that are loaded through AJAX - no page refreshes) if you want: one for spawning and one for showing each user's Pokemon collection.

I wonder if there's an API for geolocation? And weather? Maybe you want to spawn pokemon based on your geolocation, or the weather outside? Hmm... so many possibilities... What about overlapping the Pokemon spawns with a google map?

# Ajax Pagination

Create using Ajax the application shown below. As the name gets changed, or as you update the from/to date, or as you update the page number, your application should update the table with the appropriate lead information

This is a GREAT assignment where you’ll learn a lot and this assignment could be added to your portfolio.

Some of our students have showed this assignment to potential employers and they were genuinely impressed by the fact that the students could build something like this all from scratch.

<img src="https://i.ibb.co/C1tkpKT/chapter3844-6722-leads-ajax-example.png" border="0">

Figuring out the ORM calls to make this work is great practice. Filtering, excluding and limits, oh yay, all combined with AJAX!

When you see this, do you see any form? You don’t because there is no submit button? Well. In Ajax, you don’t need to submit the form just with the submit button and in fact, a lot of Ajax forms do NOT have a submit button. So looking at the wireframe above, what information should be captured inside the form which you will be sending to another URL? Spend a few minutes and think about this.

Answer: basically, you want to include all information necessary for generating that table.

Now you may be thinking but page numbers are links not drop-down or input type text. Well. Looks can be deceiving. You could still make the page numbers look like links but may be you can use jQuery to update the value of the page number in the form when those links are clicked, ultimately resulting in the form having a hidden page number that can be submitted via AJAX.
