# DOM Review

## Objectives:

-   Review the DOM
-   Recall how to use JavaScript to interact with the DOM
-   Review jQuery event listeners and DOM manipulation

----------

Can you remember all the way back to Web Fundamentals when you learned about JavaScript, the DOM, and DOM manipulation with JavaScript and jQuery? Here's a brief review.

## Vanilla JavaScript

The DOM is short for  **Document Object Model**, simply meaning that a  _document_, like an HTML page, is made up of  _objects_. On this page, open your browser's console (right click and inspect) and use JavaScript to get an element from the DOM (there's a div element on this page with the id main_navigation):
```js
var nav = document.getElementById("main_navigation");
```
So what did we get? What is  `nav`? Use the  `typeof` operator to determine its type.
```js
console.log(typeof nav)
```
There it is! It's an object! It's an element from the HTML represented as an object! Hence, Document Object Model.

Since nav is an object, we should be able to iterate over its different keys.
```js
for(var key in nav) {
	console.log(key);
}
```
You should see a long output of all the different keys that make the  `nav`  object - properties and methods such as  `innerText`,  `style`, and  `click`. This gives us access to all the different things this element has and can do. The possibilities are endless! We can change whatever we'd like about the elements and make them do different things! In other words, we can  **manipulate the DOM**. Go ahead! Give it a try! If you're unsure of what to change, try this:
```js
nav.innerText = "I just manipulated the DOM!";
nav.style.backgroundColor = "yellow";
```
Neat, right?!

## jQuery

**jQuery**  is just a JavaScript library that simplifies writing scripts for DOM manipulation. To add jQuery to your page, grab the script link from  [Google Hosted Libraries](https://developers.google.com/speed/libraries/#jquery). Use  [jQuery's documentation](https://api.jquery.com/)  for a full list of all event listeners and methods available. The snippets below provide a quick review of the most common things we'll do with jQuery. Also go back to your  [jQuery Functions](http://learn.codingdojo.com/m/2/4655/28035)  assignment for your own examples!

### DOM Manipulation

The jQuery library provides lots of different methods, used like so:

<img src="https://i.ibb.co/gDm53Cz/jquery-methods.png" alt="jquery-methods" border="0">

For example, to do what we did above:

$("#main_navigation").text("I just manipulated the DOM!"); $("#main_navigation").css("backgroundColor", "yellow");

### Adding Event Listeners

A subset of important jQuery methods are those that allow us to control  _when_  DOM manipulation occurs. If we want to do something if the user performs a certain action, we can add an event listener to an element on the DOM and provide a handler, or a function that explains what we want to do when that action is taken.

<img src="https://i.ibb.co/4mnntZn/jquery-events.png" alt="jquery-events" border="0">

For example, given the following HTML, suppose we updated the div contents when it is clicked on, or the text color of xyz-classed elements change when p tags are hovered over.

#### jquery-review/example.html
```html
<head>
    // import jQuery
    <script src="script.js" defer>
    </script>
</head>   
    
<body>        
    <div id="container">
    	<p class="xyz">Coding</p>
    	<p class="xyz">Dojo</p>
    </div>
</body>    
```
#### jquery-review/script.js
```js
$("#container").click(function() {
    // add a new paragraph to the container div
 $("#container").append("<p>New paragraph!</p>");
});
    
$("p").hover(function() {
    	// change the text color of all elements with class 'xyz' to blue
    	$(".xyz").css("color", "blue");
    },
    function() {
    	// change the text color of all elements with class 'xyz' to black
    	$(".xyz").css("color", "black");
});
```

# Introduction to AJAX

## Objectives:

-   Learn what AJAX allows us to do
-   Understand its significance to the modern web

----------

Manipulating the DOM is cool, but up to this point, we've only done it with basically static content. What if we wanted to dynamically generate content based on information in our database or other backend logic? Enter AJAX.

Now that you're more comfortable with the traditional request-response cycle, it's time to learn about AJAX, a technique that allows us to make requests and receive responses that we can use to update, rather than completely re-render, the webpage. What does that mean? The video below is a demo of one way that AJAX can significantly improve the user experience.

Can you think of any other examples you have encountered on the web that might be using AJAX? Perhaps doing a Google search and being provided with similar search items? Or scrolling to the bottom of a page and having the page respond by revealing more content?

It was the introduction of AJAX that began a new era of web application which we call Web 2.0. It's crucial for you to know and understand AJAX to be a true modern web developer.

# Synchronous vs. Asynchronous Code

## Objectives:

-   Understand how our current code is synchronous
-   Learn about asynchronous code

----------

AJAX stands for  **asynchronous JavaScript And XML**. This probably doesn't help if we don't cover what asynchronous means. And in order to do that, we need to discuss what synchronous means first!

## Synchronous Code

This is what we've been doing up to this point, when code runs in the order in which it is written. For example, here is some synchronous code that we have seen before. This is taken from a project where a Flask server is querying a database:
```py
@app.route('/friends')
def index():
    mysql = connectToMySQL("friendsdb")                             # Step 1
    print("Connected to our database!")                             # Step 2
    all_friends = mysql.query_db("SELECT * FROM friends")           # Step 3
    print("Fetched all friends", all_friends)                       # Step 4
    return render_template('index.html', friends = all_friends)     # Step 5
```
The code is executed exactly as we see it written.

1.  Connect to the database
2.  Print to celebrate our connection to the database
3.  Make a query and store the result in a variable
4.  Print the result
5.  Render a template with the data from the result

This has been serving our purposes very well, but consider what would happen if the query is super complex with lots of joins. This would cause the query to take a long time to complete. How would that affect the output we see? We would experience a lag in between the two prints. In other words, we would see Step 2 printed, then wait for Step 3 to complete, and then finally, after a lag, see the print in Step 4.  **Our code would not be able to move on to step 4 until step 3 is completed.**

Most of the time we love synchronous code. After all, in the example above, we are relying on the fact that we are going to wait for each line of code to complete before moving on to the next. It would be awful if we proceed to Steps 4 and 5 before we get a response from Step 3 - we would be trying to render a template without any data!

## Asynchronous Code

While our synchronous code above is doing its job just fine, let's think beyond the server. What caused this function to run to begin with? To invoke this function, a client must have made a request to the /friends route. The server does not send a response until it has the necessary data, so what does that mean for the user experience on the client side?

<img src="https://i.ibb.co/cbzNmJL/waitingclient.png" alt="waitingclient" border="0">

Of course the client must wait for the response from the server, but in the meantime, we can keep the client busy with other tasks! With **asynchronous programming,**  our client's code does not actually have to run in the order it is written. Below is an example demonstrating how we may give the user a chance to play a game until the response from the server comes back.  
```py
$('#sendRequest').click(function(){         // Step 1 - a click happens
    $.ajax({                                // Step 2 - make an AJAX get request to /friends
        url: "/friends",
        method: "GET"
    })
    .done(function(res){                    // Step 4 - receive the response
        $('#game').hide();                  // Step 5 - hide the game   
        $('#result').html(res);             // Step 6 - manipulate the html to display the data from the server
    })
    $('#game').show();                      // Step 3 - show the game to occupy the user while waiting
})
```
Notice that the code is executed in an order **different from how it is written.**

1.  A click on the #sendRequest element triggers the code to run
2.  A get request is made to /friends
3.  Jump to the last line of code and the #game element is shown
4.  The response comes back
5.  The #game element is hidden
6.  The #result element is altered to show the response from the server

## A Roommate Analogy

If you're having trouble visualizing synchronous versus asynchronous programming, consider this analogy. Let's say you have a roommate (let's call her Python), and one day, you leave her a list of chores that need to be done:
```
Chores for Python:
1. Wash dishes
2. Sweep the floors
3. Sign for package delivery
4. Feed the cat
```
When you come home many hours later, you find Python sitting patiently on the porch, gazing down the street. Puzzled, you walk into the house and see the dishes have been done, the floors have been swept, but the cat is desperately trying to get your attention to feed her. For some reason, Python hasn't fed the cat yet! That's when you are hit with the realization: Python is outside waiting for the package to be delivered! It's not her fault, she's just being synchronous. She cannot move on to the fourth chore until the third chore is completed.

Fed up with your synchronous roommate, you decide to get a new one (let's call him JavaScript). JavaScript reads the same list of chores and washes the dishes, sweeps the floors, and then, being an absolute genius, very smartly moves on to feeding the cat. In the meantime, JavaScript listens for the doorbell so he can sign for the package at the appropriate time.

## So is JavaScript asynchronous?

**No, JavaScript is synchronous.**  However, we can use JavaScript to  **write asynchronous code**. To do this, we need to use **callbacks,** which are functions  _passed as arguments to other functions that will be invoked later_. Look again at this code snippet and identify the callbacks:
```py
$('#sendRequest').click(function(){         // the .click() method accepts a callback
    $.ajax({                                
        url: "/friends",
        method: "GET"
    })
    .done(function(res){                    // the .done() method accepts a callback
        $('#game').hide();                     
        $('#result').html(res);             
    })
    $('#game').show();                      
})
```
Notice that the callbacks are used to define the code that we want to be invoked _later._ The  `.click()`  method accepts a callback that defines what we want to do _after_ the click has occurred. The  `.done()`  method accepts a callback that defines what we want to do _after_ the response returns from the server.

Here's a simple example demonstrating this concept of asynchronicity:

# Partials

## Objectives:

-   Discuss rendering partial HTML
-   Understand how partials can be useful

----------

It's time to combine these concepts of DOM manipulation and making AJAX requests.

With AJAX, the  _browser's JavaScript interpreter_  sends an HTTP request. The response can then be used to manipulate the DOM. That means the server does not have to render the entire page of HTML again and the browser does not reload! So if the server is not rendering the entire page of HTML, then what is it sending as a response?

We will be covering two different responses that the server could send back:  **partials**  and  **JSON.** We'll begin with partials.

## Partials are snippets of HTML

A partial is a small snippet of HTML. When we make a partial, we won't even include the usual meta data we typically place at the top of an HTML document. We do not need any of this meta data because we are going to incorporate the HTML snippet into the document already on the client, which already has the meta data needed.

To understand why we would want a partial, consider the scenario where a user is filling out a registration form. The application expects a unique username. As the user is filling out the form, before it's even submitted, wouldn't it be nice if we could notify the user if the username typed in is taken already? It would save the user some time to know that right away, rather than having to wait until after the form is filled out and submitted.

<img src="https://i.ibb.co/hyz6rXr/username.png" alt="username" border="0">

Notice another benefit of having this error message pop up without having to reload the entire page: We could leave everything else on the page alone, including all the inputs that the user already filled out. If you were ever frustrated about losing user input when reloading a page with flash messages, this should be of great interest to you. We may manipulate the DOM just enough to include this one desired piece of HTML with our error message.

To make this happen, we could have our browser listen for every keystroke that takes place in the username field. With each keystroke, we'll have the JavaScript interpreter send a request to the server to query the database for the username that the user has typed so far. If we find the username in our database already, we'll have the server respond with just a  `<p>`  tag holding our error message. Otherwise, we may respond with a  `<p>`  tag containing a message that the username is available. Once the  `<p>`  tag arrives on the client side, we'll manipulate the DOM to include this  `<p>`  tag.

<img src="https://i.ibb.co/5GXtQD0/username3.png" alt="username3" border="0">

Here's the code to make this happen! Some basics, such as stylesheets and importing jQuery, are removed for brevity.  

**templates/wall.html**
```html
<html>
    <head>
        <script src="{{ url_for('static', filename='wall.js') }}"></script>
    </head>
    <form action="/register" method="post" id="regForm">
        <div id="usernameMsg"></div>   <!-- notice the empty div reserved for our message -->
        <input id="username" type="text">
        <button type="submit">Submit</button>
    </form>
</html>
```
**static/wall.js**
```js
$(document).ready(function(){
    $('#username').keyup(function(){
        var data = $("#regForm").serialize()   // capture all the data in the form in the variable data
        $.ajax({
            method: "POST",   // we are using a post request here, but this could also be done with a get
            url: "/username",
            data: data
        })
        .done(function(res){
             $('#usernameMsg').html(res)  // manipulate the dom when the response comes back
        })
    })
})
```
**server.py**
```py
@app.route("/username", methods=['POST'])
def username():
    found = False
    mysql = connectToMySQL('ajaxWall')        # connect to the database
    query = "SELECT username from users WHERE users.username = %(user)s;"
    data = { 'user': request.form['username'] }
    result = mysql.query_db(query, data)
    if result:
        found = True
    return render_template('partials/username.html', found=found)  # render a partial and return it
    # Notice that we are rendering on a post! Why is it okay to render on a post in this scenario?
    # Consider what would happen if the user clicks refresh. Would the form be resubmitted?
```
Our partial, shown below, is kept in a partials folder nested inside our templates folder. For this code snippet,  _we did not remove anything!_  What you see is the entire file. Notice the lack of any meta data - it is not needed because it will become part of wall.html.  

**templates/partials/username.html**
```html
{% if found == True %}
<p class="error">Username has been taken.</p>
{% endif %}
{% if found == False %}
<p class="success"> This username is available</p>
{% endif %}
```
Here's a review of the different pieces we've talked about so far:

# Assignment: Username Availability

## Objectives:

-   Gain familiarity with having your server respond with partials
-   Use AJAX to make requests to the server in the background
-   Manipulate the DOM to change something about the HTML without refreshing the entire page

----------

Building off any project you currently have that includes login and registration, implement the check on the availability of the username as discussed in the previous module.

<img src="https://i.ibb.co/PWftx0Z/username-YN.png" alt="username-YN" border="0">  

Remember to include the jQuery library. The easiest way to do this is to use the CDN provided by  [Google Hosted Libraries](https://developers.google.com/speed/libraries/#jquery)  .

# Disabling Form Submission

## Objectives:

-   Understand when it is necessary to disable forms
-   Understand how to disable forms

----------

Forms typically come with submit buttons. Submit buttons, however, cause the browser to make a request to the url in the  `action`  attribute. In other words, the browser redirects to that url, which we don't want if we are using AJAX to submit the form. For example, consider the code below:
```html
<form action='/new_destination' id='myForm' method='post'>
    Name: <input type='text' name='name'>
    <input type='submit' id='submit_btn' value='Submit'>
</form>
   
<script>
    $('#submit_btn').click(function(){
       $.ajax({
          url: '/new_destination',
          method: 'POST',
          data: $('#myForm').serialize()
        })
        .done(function(response){
             console.log(response);
        })
     });
</script>
```
When the submit button is clicked, it will send an AJAX request _and_ submit the form normally. This means the browser will redirect to "/new_destination". To prevent the browser from going to that page directly, you need to add  `return false`  so that it does not submit the form normally.

In other words, your script would now look like this
```js
$('#submit_btn').click(function(){   // listen for when the #submit_btn element is clicked
     $.ajax({
          url: '/new_destination',
          method: 'POST',
          data: $('#myForm').serialize()
     })
     .done(function(response){
         console.log(response);
     })
    return false;                     // return false to disable the normal submission of the form
});
```
Another way to disable the form submission is to listen for when the form is submitted, and then return false:
```js
$('#myForm').submit(function(){     // listen for when the #myForm element is submitted
      $.ajax({
         url: '/new_destination',
         method: 'POST',
         data: $('#myForm').serialize()
       })
       .done(function(response){
            console.log(response);
       })
       return false;                // return false to disable the normal submission of the form
});
```
Either approach is okay.

# Helpful Tips

## Objectives:

-   Establish good developer/debugging habits

----------

As you proceed with the rest of the AJAX assignments, keep the following tips in mind:

1.  **Put all the key information in a <form>.**  For any AJAX request done internally (meaning, to your own server), you're almost always sending several pieces of information to another url. Therefore, instead of having your data scattered across your web application in different elements, have it all contained in a form. This will save you countless hours of debugging in the future.
2.  **Make the <form> submit manually  without AJAX first  and make sure the HTTP response is valid and generates no errors.**  Debugging AJAX can be tricky, so break the process into smaller pieces. First, make sure the HTTP request generates the result you want. In a lot of cases, for internal AJAX calls, the HTTP response will be in the form of html (although sometimes you may want to pass back JSON, which we will discuss later). Make sure you are able to generate the desired response before adding AJAX to your list of concerns.
3.  **Carefully consider whether you should use GET or POST.**  You already know how to post data to your server. However, if you use a GET request, the data will be in the url as a  **query string**. Query strings are easily recognized by the question mark in the url. Different key-value pairs are separated by ampersands. For example, if we use a get request to submit a form to /users with two inputs, name and color, we may produce the url  `localhost:5000/users?name=kermit&color=green`. On the server side, our logic for the /users route will pull the information out of the url with the  `request.args.get(key)`  method.
    ```py
    @app.route('/users')
    def data_from_query_string():
        print(request.args.get('name'))     # outputs kermit
        print(request.args.get('color'))    # outputs green
        # any other logic goes here
    ```
4.  **Once the HTTP request is working the way you expect, use the  `.ajax()`  method to have the JavaScript interpreter send that request.**
    
    1.  Use  `.serialize()`  to group all the key information in the form.
    2.  Since the form should also contain the url where it should be submitted, your AJAX call should often follow the format shown below. If your AJAX call doesn't look simple like this, you're not doing AJAX the right way (in our opinion).
    ```js
    $('#form1').submit(function(){
      $.ajax({ 
        method: "POST",     // using a GET request would put your form data in the url as query strings
        url: $(this).attr('action'), // 'this' refers to #form1, the element that triggered the function
        data: $(this).serialize()
      })
      .done(function(response) {
        // your code on what to do once the http response is received
      })
      .fail(function(response) {
        // optional code on what to do if the http request fails
      })
      .always(function(data){
        // optional code on what should be done regardless of whether the http request is successful or not
      })
      return false; // return false so the form is not submitted normally
    });
    ```
5.  **Use jQuery to update part of the HTML DOM using the  `.html()`  method**. This is straight forward if the response consists of HTML. If the http response returns JSON, you will most likely need to create a new HTML string from the data (using loops, if/else statements, etc).
6.  **Use your browser's (Google Chrome, of course) inspector heavily.**  The very first thing to check when debugging JavaScript is the console tab. Any errors in your JavaScript syntax will be displayed in the console, so  if you read them,  you may save hours of time hunting for a missing curly bracket. To produce your own messages in the console, remember to use  `console.log()` and use it frequently! It is easy to lose track of the order of operations when working with asynchronous code. To get started, be sure to include logging to the console in the following places:
    
    1.  First thing in  `document.ready()`  to make sure jQuery is loading properly
    2.  Right after the  `.submit()`  handler for your form to be sure the event listener is working
    3.  Within the  `.done()`,  `.fail()`, and  `.always()`  methods chained after  `.ajax()`
    4.  Whenever creating variables within your JavaScript code to make sure you have what you think you have. Check the data type as well. Often we think we have a number when we actually have a string, or we think we have an object when we actually have null.
7.  **Check the network tab.**  The network tab in your browser's inspector allows us to monitor the http requests and responses sent and received by our web page. Make sure your page is connecting to the file where you are submitting your form, and make sure there are no errors. Click on the response/preview tab to check whether the URL is returning data. If your JavaScript/jQuery code is working correctly, but your Python code is awry, using the network tab will allow you to see your Python errors without turning AJAX off. This is a great way to lessen the scope of potential errors!
8.  **Understanding AJAX is essential to master frontend frameworks.**  Later on, in the MEAN stack, we will be covering Angular. Many students also choose to learn React, AngularJS, and/or Vue.js. Developers skilled with frontend frameworks are in high demand, and frontend frameworks revolve around asynchronous programming.

# Assignment: Search Bar

## Objectives:

-   Practice building functionality first, then incorporating AJAX after
-   Practice AJAX by adding auto-complete functionality to our application

----------

For this assignment, we are going to implement a search bar. Since we already have a project set up with users and their usernames from the last assignment, let's add a feature to it so that users may search for their friends by username. We'll display all the users whose usernames start with what they have submitted.

<img src="https://i.ibb.co/M2Fx5Kt/username-search.png" alt="username-search" border="0">

## Start Without AJAX

Whenever using AJAX, we will have an easier time if we first implement our features without AJAX first. That will clarify any questions about the backend logic, so that later on we can just focus on implementing AJAX correctly. To get you started, here is how we may make a search bar without AJAX. We're going to use a form to submit the search term. For this example, our form will make a GET request, so the search term will appear in the url as a  **query string.**

<img src="https://i.ibb.co/4JZxfYg/username-search-noajax.png" alt="username-search-noajax" border="0">

#### wall.html
```html
<form method="GET" action="/usersearch">  <!-- using GET will place the form inputs in the url as query strings-->
     <input type="text" name="name">
     <button type="submit">Search</button>
</form>
```
Submitting the search term "mo" will produce the url  `localhost:5000/usersearch?name=mo`. This will take us to the /usersearch route in our server, where we can pull any data from the query string that follows the question mark in the url.

#### server.py
```py
@app.route("/usersearch")
def search():
    mysql = connectToMySQL("friendsdb")
    query = "SELECT * FROM users WHERE name LIKE %%(name)s;"
    data = {
        "name" : request.args.get('name') + "%"  # get our data from the query string in the url
    }
    results = mysql.query_db(query, data)
    return render_template("success.html", users = results) # render a template which uses the results
```
If the code above is implemented correctly, when the form is submitted, the user input will appear in the url and be sent to the route /usersearch. From there, the server will pull the information needed out of the url, query the database, pass the returned data to a template, render, and pass the html to the client. The client will reload the page, and we should see our newly rendered HTML replace our previous HTML.

Once you have that implemented, add AJAX! Take away the submit button and have the request made with each keystroke. Instead of replacing the HTML already displayed by the client, return a partial that displays the results. Manipulate the DOM to add the partial into the existing HTML.

# Assignment: Private Wall 2.0

## Objectives:

-   Update the Private Wall assignment with AJAX to improve the user experience

----------

Imagine scrolling through a social media application or internet forum of your choice - let's say Facebook or Reddit. After you've been scrolling, scrolling, scrolling, scrolling, you finally find something that deserves your enlightened comment. You carefully type in your comment and hit the submit button. What happens next?

If you're thinking in the context of the applications we've built, you might be thinking, "Never render on a post! Redirect!" And that would be great... but.... the page would get reloaded, and then we would be right back at the top of the page. All that scrolling you did? It's completely undone! Your user experience has been ruined! Have fun scrolling through posts you've seen before to get back to where you were.

If you're instead thinking in the context of the way applications actually function, you would be expecting your comment to appear right where you are without affecting your scrolling progress. So how do these other applications do it? What secrets do they have that we are yet to share with you? You guessed it, the secret is no secret at all: it's AJAX.  

Let's revisit the Private Wall. Imagine if we had hundreds of users in the database, or if we had received hundreds of messages. We would have to scroll through all those users and messages to find the one we are looking for. And once we do something, such as delete a message or post a message to a user, we will be right back at the top of the page.

Let's fix it with AJAX!

  

<img src="https://i.ibb.co/99wKd3Z/private-wall-2-0-with-aj.png" alt="private-wall-2-0-with-aj" border="0">

  

First, have the messages submitted with AJAX. The user should see the text field clear out and should the page should not refresh.

Second, delete the messages with AJAX. The message should be removed from the DOM and the page should not refresh.

**Ninja bonus:**  Include validation messages. Messages should contain at least 5 characters, so if the user does not submit a valid message, show the error message above the form being submitted. Leave the message written so far in the text field so the user does not have to retype it. If the user successfully submits a message, show a success message.

<img src="https://i.ibb.co/0DtXC78/privatewallerror.png" alt="privatewallerror" border="0">

**Ninja bonus:** If you did the Ninja Bonuses to display the number of messages sent and received, update these displayed numbers when a message is successfully submitted or deleted.


