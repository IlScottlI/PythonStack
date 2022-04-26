# Overview

## Objectives:

-   Get pumped for full-stack practice!

----------

You've been doing full-stack applications in Django now for a couple of days! Can you believe it? Congratulations on making it this far! While in the grand scheme of things, our applications are still relatively small, hopefully you're beginning to appreciate why we might want to modularize our code and how an architecture like MTV or MVC helps guide how we split up our code.

Even though it's only been a few days, some of you might already be wondering why we learned Flask in the first place! Hopefully you can appreciate that you were able to pick up Django this quickly because you first established a solid foundation of web development basics like routing, rendering, redirecting. Hang onto these basics! While the frameworks may change, you'll revisit these concepts again when you learn any other web development framework.

In this chapter, we'll start by practicing all the basic CRUD commands, and then we're just adding  _validations_ into the mix, as well as  _bcrypt_  and  _session_  for registration and login. These assignments will give you great practice as you prepare for the belt exam! Don't stress--you've got this. Have fun!

# Assignment: Semi-Restful TV Shows

## Objectives:

-   Practice ORM queries from the controller
-   Practice RESTful routing
-   Practice rendering query results to templates
-   Practice using form input to create table data

----------

Now that we've got a basic understanding of the flow between models, views, and templates, let's make sure we know how to implement all 4 CRUD commands!

Remember that restful routing is simply a guideline of generally accepted routing naming conventions so other consumers of our routes can easily navigate our application and anticipate what the response will be for any given route. Since many web applications perform CRUD operations, you can imagine how confusing this could get if everyone followed different conventions for creating routing and method names for these operations.

Restful routing also gives us a chance to practice being methodical in our approach to building an application. For each step of CRUD, we start with the HTML, then build the routes to show that page. We can then build out the routes that will process any form submissions.

Ultimately, it's up to you (or maybe your boss) whether you also follow these rules/conventions, but we strongly encourage you to get familiar with the following rules for RESTful routing, as you may be making requests to, or someday creating your own, API.

Create a new Django project following the specifications provided in this wireframe:

<img src="https://i.ibb.co/wKw5zrk/crud-tvshows-django.png" border="0">

- [ ]  Complete each of the following routes:
    
- [ ]  /shows/new- GET - method should return a template containing the form for adding a new TV show
    
- [ ]  /shows/create - POST - method should add the show to the database, then redirect to /shows/<id>
    
- [ ]  /shows/<id> - GET - method should return a template that displays the specific show's information
    
- [ ]  /shows - GET - method should return a template that displays all the shows in a table
    
- [ ]  /shows/<id>/edit - GET - method should return a template that displays a form for editing the TV show with the id specified in the url
    
- [ ]  /shows/<id>/update - POST - method should update the specific show in the database, then redirect to /shows/<id>
    
- [ ]  /shows/<id>/destroy - POST - method should delete the show with the specified id from the database, then redirect to /shows
    
- [ ]  Have your root route redirect to /shows


#   Adding Validations

## Objectives:

-   Learn how to add our own validation logic into the models
-   Learn more about .objects (Django's model manager)

----------

Form validation is a key component of any back-end developer's arsenal. **Validation** is more of a logical challenge than a whole bunch of new code to learn. Common validation rules include:

-   Checking that the data is present
-   Making sure the data is in the correct format

Now that we can insert data, it's time to validate the user's input before inserting those values into the database. Since we're modularizing now, this code will be part of our models, since models should be doing everything database-related. Some of you may have been wondering about that  `objects`  attribute we've been using in every ORM query. We're about to find out what it is!

Consider the following Blog model:
```py
# Inside your app's models.py file
# imports
class Blog(models.Model):
    name = models.CharField(max_length=255)
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
"""
models come with a hidden property:
      objects = models.Manager()
we are going to override this!
"""
```
Without any additional work on our end, this  `objects`  property, or Manager in Django terms, has been making available to us the ORM queries like  `.all()`,  `.get()`, etc. We are going to extend the functionality of the Manager class and add some of our own methods to it.

Let's create a new class  `BlogManager`  and add it to our previous code. Be sure to add the  `BlogManager`  class in before the declaration of the  `Blog`  class.

**Notice that  `Blog`  and  `BlogManager`  are inheriting from entirely different models.**  By inheriting from  `models.Model`,  `Blog`  is made into a database table. By inheriting from  `models.Manager`, however, our  `BlogManager`  will inherit from the ORM-building class. This Manager class is another built-in Django class used to extend our models' functionality. This means BlogManager still contains all the methods it did before, but we are now able to add our own methods. Here we are making one called  `basic_validator`, that expects a dictionary of data from the views:
```py
# Inside your app's models.py file
from django.db import models
# Our custom manager!
# No methods in our new manager should ever receive the whole request object as an argument! 
# (just parts, like request.POST)
class BlogManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['name']) < 5:
            errors["name"] = "Blog name should be at least 5 characters"
        if len(postData['desc']) < 10:
            errors["desc"] = "Blog description should be at least 10 characters"
        return errors
```
You'll notice that we are doing one of the types of validations mentioned above here. By checking the length of the input, we can make sure that the user entered something in that field. We also put some strings into a dictionary called **errors**. These are the error messages that the user is going to see on their page once we get everything set up.

Now to link our BlogManager to our Blog class, we are going to override the  `objects`  property and have it reference our newly created manager, like so:
```py
class Blog(models.Model):
    name = models.CharField(max_length=255)
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BlogManager()    # add this line!
```
Now in our  `views.py`  file, we can use  `Blog.objects.basic_validator(postData)`:
```py
# Inside your app's views.py file
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
   
from .models import Blog
def update(request, id):
    # pass the post data to the method we wrote and save the response in a variable called errors
    errors = Blog.objects.basic_validator(request.POST)
        # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/blog/edit/'+id)
    else:
        # if the errors object is empty, that means there were no errors!
        # retrieve the blog to be updated, make the changes, and save
        blog = Blog.objects.get(id = id)
        blog.name = request.POST['name']
        blog.desc = request.POST['desc']
        blog.save()
        messages.success(request, "Blog successfully updated")
        # redirect to a success route
        return redirect('/blogs')
```
Notice in the code above we are using Django's messages framework.

There is one more step to get these messages to display on our page. Somewhere in our HTML template (the same template that contains the form!), place the following lines of HTML. The errors will display wherever you put this, so putting it just above the form is probably a good idea.
```py
{% if messages %}
<ul class="messages">    
    {% for message in messages %}    
        <li {% if message.tags %} class="{{ message.tags }}"{% endif %}>{{ message }}</li>    
    {% endfor %}
</ul>
{% endif %}
```
  

There's a lot more we can do with the messages to make them look pretty. For some ideas, check out the documentation [here](https://docs.djangoproject.com/en/1.11/ref/contrib/messages/#displaying-messages).

Feel free to experiment with the  `BlogManager`  methods – any change you make to that class  _does not_  need to be migrated since it's not a database table.

#### Video Overview


#### Want to learn more?

1.  More about managers:  [https://docs.djangoproject.com/en/2.2/topics/db/managers/](https://docs.djangoproject.com/en/2.2/topics/db/managers/)
2.  For more on Flash messages (being used above):  [https://docs.djangoproject.com/en/2.2/ref/contrib/messages/](https://docs.djangoproject.com/en/2.2/ref/contrib/messages/)  (if you do this, please make sure you add "**from django.contrib import messages**"
3.  Alternative way of doing some form validations:  [https://docs.djangoproject.com/en/2.2/topics/forms/](https://docs.djangoproject.com/en/2.2/topics/forms/)

You may have noticed that we're sending you to the primary literature a bit more frequently in this chapter. This is intentional and important: the ability to parse official documentation is an essential skill for a self-sufficient developer. But that doesn't mean you have to figure it out all on your own! If you're having trouble understanding the documentation, get help. Learning to read the docs isn't always as easy as it might seem.

# Pattern Validation

## Objectives:

-   Learn how to use regex to validate
-   Learn how to validate an email address
-   Review other methods that can be useful for validating

Another common validation that needs to be performed is checking whether an input matches a certain pattern. For example, email addresses have a particular pattern; passwords are often required to have a certain number of different types of characters. We can achieve this by using something known as a **regular expression** or **regex**. We've already been using regular expressions in our routes, so let's now see how we can match a pattern in our own code.

A regex is a sequence of characters that defines a search pattern. It can be used to match a string that follows a pattern. For example, every email has a series of alphanumeric characters followed by an @ symbol followed by another series of alphanumeric characters followed by a "." and finally another series of alphanumeric characters. You don't need to know how to create regex at this point, but understanding what they are and what they are used for is definitely important. The Python regex for matching an email address based on the above criteria looks something like this (the preceding r indicates the string is a raw string, i.e. all characters should be taken literally):
```
r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$'
```
The snippets below show the important additions to our models file:

#### some_project/some_app/models.py
```py
import re	# the regex module
class BlogManager(models.Manager):
    def basic_validator(self, postData):    
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern 
            errors['email'] = "Invalid email address!"
        return errors
```
The EMAIL_REGEX object has a method called .match() that will return _None_ if no match can be found. If the argument matches the regular expression, a match object instance is returned.

### Other Useful Validation Tools:

-   [str.isalpha()](https://docs.python.org/3.6/library/stdtypes.html#str.isalpha) -- returns a boolean that shows whether a string contains only alphabetic characters
-   [other string methods](https://docs.python.org/3.6/library/stdtypes.html#string-methods)
-   [time.strptime(string, format)](https://docs.python.org/3.6/library/time.html#time.strptime) -- changes a string to a time using the given format

# Assignment: Semi-Restful TV Shows Validated

## Objectives:

-   Practice validating data before entering it into the database

----------

Let's add validations to your existing Semi-Restful TV Shows assignment! Building off of your existing assignment, implement the validations indicated on the green sticky notes to prevent dirty data from getting into your database. If a submission is invalid, display errors on the appropriate page.

<img src="https://i.ibb.co/qM384qw/crud-tvshows-django-valid.png" border="0">

- [ ]  Validate the Add a TV Show form to ensure all fields are populated appropriately before adding to the database.
    
- [ ]  Display errors on the Add a TV Show form if the information is invalid.
    
- [ ]  Validate the Edit Show form with the same validations as creation.
    
- [ ]  Display errors on the Edit Show form if the information is invalid.
    
- [ ]  NINJA BONUS: Ensure the Release Date is in the past.
    
- [ ]  NINJA BONUS: Allow the description to be optional. If a description is provided, though, it should still be at least 10 characters.
    
- [ ]  SENSEI BONUS: Validate that a TV show with that title does not already exist in the database before creating or updating.
    
- [ ]  SENSEI BONUS: Do uniqueness validations (including displaying errors) for creating and updating using AJAX!

# Assignment: Courses

## Objectives:

-   More practice with full-stack creating, reading, and deleting from a database
-   More practice with model validations
-   Learn how to implement one-to-one relationships with Django's ORM

----------

Make a new Django project and application, and complete the functionality of the wireframe below. Require the course name to be more than 5 characters and the description to be more than 15 characters.

### Bonus Features (Optional)

1.  Make  `description`  a one-to-one relationship with the  `Course`  table rather than a column in the course table (_intermediate_).
2.  Add an action  comment  to each course that takes you to a page where you can add comments about that course and view all comments that have been entered (_advanced_)

<img src="https://i.ibb.co/7QMSgPD/chapter3834-6619-mvc-courses.png" border="0">

- [ ]  Make a new Django project and app
    
- [ ]  Have the root route render the main wireframe above
    
- [ ]  Create the POST method to add new courses to the database
    
- [ ]  Ensure that the name entered is more than 5 characters, and the description is more than 15 characters
    
- [ ]  Display all the courses in a table beneath the form
    
- [ ]  For each course, have a link to remove that renders a page as shown in the second wireframe
    
- [ ]  If the user selects "No," redirect to the root route. If the user selects "Yes," delete the course and redirect to the root route
    
- [ ]  NINJA BONUS: Make the description a separate class and have the description field of the Course class be a one-to-one relationship with Description
    
- [ ]  NINJA BONUS: For each course, have a link to comment that renders a page with a form to make comments and a list of all comments for that course
    
- [ ]  SENSEI BONUS: Use AJAX for the remove functionality, prompting with a modal and processing the remove accordingly (No--close the modal without deleting, Yes--close the modal and delete the entry)

# Amadon

## Objectives:

-   Practice handling POST data
-   Avoid rendering after a POST request
-   Be careful about what you put inside  `<form>`tags

----------

We've decided to start building our own e-commerce site called Amadon.

The goal of this assignment is not to build a full-fledged e-commerce site (i.e. no login, validation, etc.). Rather, we want to point out some important things to consider when building forms:

1.  Why we don't want to render after a POST request (you may recall going over this when we were learning Flask)
2.  What we should put in our forms versus what should be handled by the server in the backend

<img src="https://i.ibb.co/sVKs4VB/amadon2.png" border="0">

### IMPORTANT LESSON 1

Say the customer reloads the checkout page after purchasing an item. How happy would your customer be if they were charged again and received double their original order? Probably not very happy!

A good developer should not have a method handle both the POST data  _and_  render HTML. This is a very common mistake made by developers--we should always double-check that we haven't made this mistake ourselves!

Instead have the http POST request sent to one route, have that route handle the POST data, and then  _redirect_  to a new GET route which displays the thank you html. This way, even when the user reloads the thank you page, it will not re-process the submitted order.

### IMPORTANT LESSON 2

Another reason we designed this assignment like this is for you to see how easy it is to manipulate the form. For example, say that the form for ordering a Dojo T-shirt looked like this.
```html
<form action='/amadon/buy' method='post'>
  {% csrf_token %}
  <select name='quantity'>
     <option>1</option>
     <option>2</option>
     <option>3</option>
  </select>
  <input type='hidden' name='price' value='19.99' />
  <button type='submit'>Buy!</button>
</form>
```
A somewhat sophisticated user could, for example, use the browser's Inspect Element tool to change the price to '0.01' and order lots of t-shirts for very cheap! A better way to handle this would be to have, for example,  _product_id_  as a hidden variable. This way, if they change the product_id using inspect element, they would just get a different item for their order.

In other words, have the form look more like below:
```html
<form action='/amadon/buy' method='post'>
  {% csrf_token %}
  <select name='quantity'>
     <option>1</option>
     <option>2</option>
     <option>3</option>
  </select>
  <input type='hidden' name='product_id' value='1015' />
  <button type='submit'>Buy!</button>
</form>
```
Surprisingly, a lot of e-commerce sites are built where you could easily change the price. What if you built a web crawler/scraper to go through lots of e-commerce sites to specifically look for sites where price is part of the shopping cart form? You could reach out to them and tell them about the security flaw in their site. Maybe they'll hire you to make their site more secure? :)

Now it's your turn to go through this exercise and experience these issues for yourself. Follow the steps below to first experience these issues yourself, and then fix them. Follow the checklist below using  [this GitHub repository](https://github.com/TheCodingDojo/amadon)  to get started. These same instructions are also provided in the GitHub repository's README file. In this code, we're not worrying about individual users, so we'll assume that all orders are being submitted by one user in order to calculate totals.

- [ ]  Clone the repository and peruse the code
    
- [ ]  Run makemigrations and migrate to create the necessary database tables
    
- [ ]  Seed the database with a few products (i.e. go into the shell and create 3-4 products)
    
- [ ]  Run the server and make a purchase
    
- [ ]  Add some basic styling (use Bootstrap or another CSS framework)
    
- [ ]  On the checkout page, calculate and display the total charge for the most recent order
    
- [ ]  On the checkout page, calculate and display the total quantity of all orders combined
    
- [ ]  On the checkout page, calculate and display the total amount charged for all orders combined
    
- [ ]  After making an order, hit the refresh button while on the checkout page and say yes/confirm. What do you notice?
    
- [ ]  Fix this issue so that users don't inadvertently make another order by mistake
    
- [ ]  Go back to the order form and use your browser's inspect element tool. Change the price of an item and then place an order. What do you notice?
    
- [ ]  Fix this issue so that users don't get to set the price of their items!


# Securing Passwords

## Objectives:

-   Understand what hashing is
-   Understand what encryption is
-   Learn techniques for protecting users' passwords
-   Understand what a salt is
-   Discuss the vulnerabilities that hackers might exploit to access our users' passwords

As we've seen, hackers can find ways to gain access to your database. Web developers are responsible for keeping users' data safe. No one should know our users' passwords - **not even us!** This can be very difficult to do correctly and is largely why we see so many websites offering us the option to sign up via Facebook or Google - they're passing the job of user authentication off to the experts (how you may feel about their expertise is a different matter). This may be an option you would like to explore in the future, but you should still know how to store - and how not to store - users' passwords.

## BAD idea: Directly store passwords in the database

<img src="https://i.ibb.co/XFx7TYt/Screen-Shot-2018-03-19-at-4-24-11-PM.png" border="0">

It should be pretty obvious why we would never want to put our users' passwords straight into our database. As we saw when we discussed SQL injection, it may be very easy for malicious users to access data that wasn't meant for them to see. So obviously we would never just store passwords in plain text! (It's obvious now, but unfortunately, many developers have had to learn that lesson the hard way.)

Instead, we'll want to mask the data somehow, so even if hackers got into our database, they wouldn't know what to do with it.

## Good idea, but not good enough #1: Hash the passwords before storing them

<img src="https://i.ibb.co/JdbPS5k/Screen-Shot-2018-03-19-at-4-35-58-PM.png" border="0">

In order to mask our users' passwords, we will use a technique called _hashing_. Hashing scrambles data in such a way that cannot be reversed. This is different from another technique you may have heard of called e_ncryption,_ which scrambles data with the use of an encryption key so that it is reversible. With encryption, anyone with the encryption key may decrypt the data. Ideally, only the sender and the receiver of the data should know the encryption key. Credit card data, for example, should be encrypted. Passwords, however, should be hashed, and we'll only store hashed passwords in our database.

We said that hashing is not reversible, so how can we match passwords? The answer is that a hashing algorithm will always produce the same output for a particular input. Therefore, we'll take the password input when a user logs in, hash it, and compare the hash to the value stored in the database.

Sadly, hashing is supposed to be irreversible, but many of the common hashing algorithms, such as `md5()` and `sha1()`, have been hacked and are no longer reliable. Besides, this technique leaves us vulnerable to brute force attacks. Hackers have even made _rainbow tables,_ which are tables of common passwords (we're looking at you, "password123") and their hashes. Rainbow tables aren't even necessary anymore, though, because modern computers and the hashing algorithms are so fast, it doesn't take long for a hacker's program to test thousands of passwords. Imagine all the harm that could quickly be done with a for-loop like the one below:
```py
for password in my_list_of_passwords_to_test:      # loop through every password we want to test 
    if md5(password) in table:                     # find out if the md5 hash of the password is in the table 
        print("I guessed a password!", password)   # print any passwords that belong to a user 
```
### Good idea, but not good enough #2: Hash the passwords with a salt before storing them

A salt is a random long string that we add to a user's password before hashing it and storing it in the database. We'll keep the salt stored in our server. When the user comes back and logs in, we'll concatenate the salt to the password input, hash it, and see if it matches the value in the database. This will greatly reduce a hacker's ability to test common passwords because all the passwords are essentially random strings. However, if a hacker successfully breaks into our server and finds our salt, then we're no better off than we were with our previous idea, because the for-loop is easily adjusted:
```py
for password in my_list_of_passwords_to_test:     # loop through every password we want to test
    if md5(password + salt) in table:             # see if the salt is concatenated to the password
        print("I guessed a password!", password)
```
### Good enough #3: Give each user a unique salt

<img src="https://i.ibb.co/9bwGjcy/Screen-Shot-2018-03-19-at-5-14-05-PM.png" border="0">

If we give each user a unique salt, we can just store that salt in the database as user data. It may seem silly, because now anyone who gets into our database will have all the salts. However, the point is not to keep the salts secret, but to slow down hackers' ability to test thousands of passwords. Notice our hacker's program now has a nested for-loop, which will take _much_ longer to run:
```py
for user in users:                                       # loop through all the users                    for password in my_list_of_passwords_to_test:        # loop through every password we want to test
        if md5(password + user['salt']) in table:        # see if the user's salt is concatenated to the password            print("I guessed a password!", password)
```
So far, this is our best option, and the big benefit it has is slowing down hackers' attempts to brute force their way to finding passwords. Since this strategy of slowing down hackers is the best we have, that leads us to the solution we should use, Bcrypt.

## Bcrypt, the best we've got

Bcrypt is a hashing algorithm that is purposefully designed to be slow. It is not so slow to affect a particular user's experience, but hackers who are trying to brute force their way through thousands of passwords will not bother. Other than that, it uses the same ideas as we already listed above. Since it is slow, hackers may resort to rainbow tables again, so Bcrypt generates a salt. Bcrypt adds the salt to the user's password and hashes the result, which we store in the database.

An important thing to note is that, as developers, we have to do all we can to protect our users' data. However, if a user decides to use a weak password, there is nothing we can do. Take this lesson into your own practice. Keep your passwords secure, keep them unusual enough so they will never appear on a rainbow table, never give your password to a site you do not trust, consider using a trusted password manager, and do not reuse passwords for different accounts.

The next module will go over how to implement Bcrypt with your app.


# Bcrypt

## Objectives:

-   Review why/when hashing is important
-   Learn how to hash passwords with bcrypt before saving them in the database

----------

## Review Bcrypt

In an extremely simplified sense, Bcrypt implements an algorithm that takes longer to generate a hashed string, in addition to generating a random, unique salt per password. Why is this better? Any malicious user who wants to generate every possible hashed output would be stuck trying to create a rainbow table for years instead of days. Bcrypt also has the ability to scale the time it takes to hash a string, meaning as computers get faster, Bcrypt can become more complex and time-consuming in return.

## Installation

First, we will need to install bcrypt for the virtual environment we are using with our Django projects.
```
(djangoPy3Env) pip install bcrypt
```
The documentation for the pip module can be found at [https://pypi.python.org/pypi/bcrypt/3.1.4](https://pypi.python.org/pypi/bcrypt/3.1.4)

Once installed in your virtual environment, it can be imported like any other pip module into your project.

## Usage

#### Hashing a Password

The password must be hashed with a salt  **before**  being inserted into the database. Try it out in your shell:
```py
>>> import bcrypt
>>> hash1 = bcrypt.hashpw('test'.encode(), bcrypt.gensalt()).decode()
>>> print(hash1)
$2b$12$Wdc2qwiP6u0WdQdKwmer7.DMIcY6q76GxvrJgaodnpRDmpP8mwkDa
```
In this example, the value stored in the variable  `hash1`  would be the value we store in the database for the user's password.

We will store this string in our database, and there is a lot of information contained in it! Within the first set of $ signs, we have the Bcrypt ID (in this case, 2b). Between the next set of $ signs, the number 12 tells us how many rounds of hashing we did - this is what slows Bcrypt down. If you want it to take even longer, you may pass a larger value as a second argument - just for fun, try asking it to run 17 rounds! The next 22 characters is the salt (128 bits), and the rest is our 184-bit hash.

#### Encode() vs Decode()

By default, all strings in Python 3 are unicode strings. All cryptographic functions only work on byte strings. So:

-   str.encode(): coverts unicode -> byte
-   str.decode(): converts byte -> unicode

#### Validating a Password

To compare passwords to verify a user, the user input must be hashed with the same salt and compared. If the hashed passwords match, then the user is logged in. To do this, we can use the  `checkpw`  method. Try it in the shell as shown below:
```py
>>> bcrypt.checkpw('test'.encode(), hash1.encode())
True
```
In an application, however, hash1 would be fetched from the database and would need to be encoded again, such as in the following snippet:
```py
def validate_login(request):
    user = User.objects.get(email=request.POST['email'])  # hm...is it really a good idea to use the get method here?
    if bcrypt.checkpw(request.POST['password'].encode(), user.pw_hash.encode()):
        print("password match")
    else:
        print("failed password")
```
**Note**: the order of the 2 arguments matters--the first should be the input being tested, and the second is the value that has already been hashed.

## Password Hashing: Login vs. Registration

### Hashing on Registration

Let's see how some of our code may look when we are creating a user. In the example below, we did not include validations, but of course you would validate the user input before adding it to the database.
```py
def register():    
    # include some logic to validate user input before adding them to the database!
    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()  # create the hash 
    print(pw_hash)      # prints something like b'$2b$12$sqjyok5RQccl9S6eFLhEPuaRaJCcH3Esl2RWLm/cimMIEnhnLb7iC' 
    # be sure you set up your database so it can store password hashes this long (60 characters)
    # make sure you put the hashed password in the database, not the one from the form!
    User.objects.create(username=request.POST['username'], password=pw_hash) 
    return redirect("/") # never render on a post, always redirect! 
```
### Compare on Login

Here's how our code may look when a user logs in. We'll need to check the provided password with the hash in the database:  
```py
def login():
    # see if the username provided exists in the database
    user = User.objects.filter(username=request.POST['username']) # why are we using filter here instead of get?
    if user: # note that we take advantage of truthiness here: an empty list will return false
        logged_user = user[0] 
        # assuming we only have one user with this username, the user would be first in the list we get back
        # of course, we should have some logic to prevent duplicates of usernames when we create users
        # use bcrypt's check_password_hash method, passing the hash from our database and the password from the form
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            # if we get True after checking the password, we may put the user id in session
            request.session['userid'] = logged_user.id
            # never render on a post, always redirect!
            return redirect('/success')
    # if we didn't find anything in the database by searching by username or if the passwords don't match, 
    # redirect back to a safe route
    return redirect("/")
```
  

#### References

-   [https://stackoverflow.com/questions/6832445/how-can-bcrypt-have-built-in-salts](https://stackoverflow.com/questions/6832445/how-can-bcrypt-have-built-in-salts)


# Assignment: Login and Registration

## Objectives:

-   Build a login and registration page with validations
-   Practice Flash messages
-   Practice session

----------

It's time to build Login and Registration again, this time using Django.

We’ve learned how to integrate models, validations, and controllers to our projects. Our next goal is to create a fully functional login and registration app! This will combine your knowledge of MVC patterns, validations, and password encryption.

Registration should adhere to the following guidelines:

-   First Name - required; at least 2 characters; letters only
-   Last Name - required; at least 2 characters; letters only
-   Email - required; valid format
-   Password - required; at least 8 characters; matches password confirmation

<img src="https://i.ibb.co/Cz54NLP/Login-Reg-Django.png" border="0">

#### Something to Consider

**User.objects.get(email = email)**

If there is not a matching email for a .get(), Django throws an error (try and except could come in handy), otherwise it returns the User object associated with the matching user. e.g. Userobject.

**User.objects.filter(email = email)**

Filter, on the other hand, returns a list, so if there is no user that matches, it returns an empty list. If there is a single matching user the list will contain a single User object: e.g. [Userobject].

- [ ]  Create a new Django project with a login app
    
- [ ]  Have the root route render a page where users can register or log in
    
- [ ]  Complete the registration method, including showing errors if the input is invalid
    
- [ ]  Complete the login method, including showing errors if the input is invalid
    
- [ ]  Upon successful registration or login, redirect to a success page, displaying the user's name and a message as shown above
    
- [ ]  Have the logout link clear the session and redirect to the login/reg page
    
- [ ]  Don't allow a user who is not logged in to reach the /success route (i.e. by making a GET request in the address bar)
    
- [ ]  NINJA BONUS: Add a birthday field and validate that the user's birthday is in the past
    
- [ ]  NINJA BONUS: Validate that the email provided for registration is unique
    
- [ ]  SENSEI BONUS: Add a birthday field and validate that the user is at least 13 years old (COPPA compliant!)
    
- [ ]  SENSEI BONUS: Validate the email uniqueness with AJAX
    
- [ ]  SENSEI BONUS: Use JavaScript to perform client-side validations
    
- [ ]  SENSEI BONUS: In addition to server side validations, use JavaScript to perform client-side validations on required fields. Don't allow the form to be submitted unless fields are valid.

#### Files

[login_reg_proj (Nov 30-Dec 23, 2020 Schedule)](https://github.com/IlScottlI/PythonStack/tree/master/django/django_fullstack/login_reg_proj)

# Assignment: The Wall

## Objectives:

-   Practice connecting a Django application to a database
-   Integrate the login app with another app
-   Practice one-to-many relationships
-   Practice validating user input and using flash messages

----------

Create a wall page (think Facebook news feed) where users will be able to post messages and see the messages posted by other users. Follow the below wireframe.

This app will be integrated with our login app. After successfully logging in or registering, a user should be redirected to  `localhost:8000/wall`, where the wall is displayed.

Download the  [handout](https://s3.amazonaws.com/General_V88/boomyeah2015/codingdojo/curriculum/content/chapter/flask_wall.png)  for the wireframe/ERD:

<img src="https://i.ibb.co/h88VYSh/flask-wall.png" border="0">

Once you get the messages functionality working, allow users to post comments for any message. Comments should be in a separate database table from messages.

### Helpful Tip

## Helpful Tip

In Jinja, say that you made available a variable called 'messages' where 'messages' contained all the messages in the Wall. For some reason, the following code would not work:
```py
{% for comment in message.comments.all() %}
   <p>{{comment.comment}}</p>
{% endfor %}
```
This however does work.
```py
{% for comment in message.comments.all %}    # no parentheses!
   <p>{{comment.comment}}</p>
{% endfor %}
```
### Extra Credit I (optional but highly recommended)

Allow the user to delete his/her own messages.

### Extra Credit II (optional but highly recommended)

Allow the user to delete his/her own message but only if the message was made in the last 30 minutes.

  
  

- [ ]  Create a new Django project and bring in your login app (or recreate it) and create a new wall app
    
- [ ]  Set up the necessary models
    
- [ ]  Allow users to post messages
    
- [ ]  Display all messages on the main page
    
- [ ]  Allow users to comment on each message
    
- [ ]  Display all comments per message
    
- [ ]  NINJA BONUS: Allow users to delete only their own messages
    
- [ ]  SENSEI BONUS: Allow the user to delete their own messages only if the message was written within the last 30 minutes
    
- [ ]  SENSEI BONUS: Use AJAX for adding comments, deleting messages, and deleting comments
    

#### Files

[wall_project (Nov 30-Dec 23, 2020 Schedule)](https://github.com/IlScottlI/PythonStack/tree/master/django/django_fullstack/wall_project)

# Assignment: Favorite Books

## Objectives:

-   Practice one-to-many and many-to-many relationships

----------

Say we wanted to create a website where users can upload their favorite books and other users on the website can indicate whether that book is also one of their favorites. For the database diagram, we come up with the following, realizing that there can be more than one relationship between two tables:

<img src="https://i.ibb.co/Bs8q01x/favorite-books-ERD.png" alt="favorite-books-ERD" border="0">

Let's review the two distinct relationships between the users and books tables.

-   One is a one-to-many relationship because a user can  _upload_  many books, and a book can be  _uploaded by_  one user. In our database, the uploaded_by_id field (in the books table) stores this relationship.
-   The second relationship is a many-to-many relationship, where a given user can  _like_  many books, and a given book can be  _liked by_  many users. This relationship is stored in the third table. (In the diagram, this is the likes table.)

If we retrieve a book from the database and want the associated user(s), how do we distinguish between these two different relationships? We may want the user who uploaded the book, or the users who like this book. Wouldn't it be nice if each class had some attributes like this:
```py
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
  # liked_books = a list of books a given user likes
  # books_uploaded = a list of books uploaded by a given user
    
class Book(models.Model):
    title = models.CharField(max_length=255)
  # uploaded_by = user who uploaded a given book
  # users_who_like = a list of users who like a given book
```
This is exactly what related_name provides!

<img src="https://i.ibb.co/HPTKyFN/related-name-MM.png" border="0">

According to this,

-   To get the user who uploaded a book: Book.objects.first().uploaded_by
-   To get the list of books uploaded by a user: User.objects.first().books_uploaded.all()
-   To get the list of users who like a book: Book.objects.first().users_who_like.all()
-   To get the list of books a user likes: User.objects.first().liked_books.all()

Create an application that performs the following:

<img src="https://i.ibb.co/9q0Fcr4/Favorite-Books-Django.png" border="0">

- [ ]  Create the User and Book models with all appropriate relationships
    
- [ ]  Incorporate a validated login/registration page
    
- [ ]  On the main page, allow the user to add a new book, with validations. Added books should automatically be favorited by the logged in user.
    
- [ ]  Have a list of all the books on the main page displaying the title and the user who uploaded the book
    
- [ ]  When the title is clicked, display a page with the book's information, including a list of all users who have favorited that book
    
- [ ]  If the logged in user has favorited the book, they should be able to "un-favorite" the book
    
- [ ]  If the logged in user has not yet favorited the book, there should be a link to add this book to their favorites
    
- [ ]  If the logged in user is the uploader of the book, allow them to edit (same validations apply) or delete the book
    
- [ ]  NINJA BONUS: On the main page, if the logged in user has not favorited the book, there should be a link so the user can add it to their favorites. Otherwise, display a message indicating the book has already been favorited.
    
- [ ]  SENSEI BONUS: Add a user page that allows the user to view a list of all their favorite books

# Conceptual Review

Before continuing, let's take some time to reflect on what we've learned to this point. Can you answer the following questions? Try to go through these questions with someone else in your cohort.

## Conceptual Questions

Make sure you can answer the following questions (some of these questions may be asked during the belt exam):

1.  What is the flow of information in a typical request, from when we type an address on our browser, to when we receive the response in our browser?
2.  What are MVC and OOP? Why would we use each?
3.  What is jQuery and why do we use it?
4.  Consider a database with the following tables: users, friendships, where users includes id, name, and email, and friendships includes id, user_id, friend_id; If our friendships table includes a single association to confirm a friendship between two users, what is the QUERY to pull all of your non-friends?
5.  What are some ways to make your website uniform across multiple browsers?
6.  What are the differences between submitting a form via method="post" vs method="get"?
7.  What are the advantages/disadvantages of sending data to the server in the url vs making a post request?
8.  Why should we never render a page on a post request?
9.  You notice that when you click submit on a form, your app breaks. Describe how you would approach debugging this problem.
10.  What are a couple of security threats and how do we defend against them?
11.  What is the difference between session, post, and cookies?
12.  Explain why and when we use session.
13.  What is an ORM and why do we use it? What are its advantages and disadvantages?
14.  In your models, you may make a class User with the following code:  `class User(models.Model):`. Why do we have models.Model inside the parentheses?
15.  In your models, you may make a class UserManager with the following code:  `class UserManager(models.Manager):`. Why do we have models.Manager inside the parentheses?
16.  What is self and why does it appear in methods that we define in a class?
17.  What is the __init__ method in a class?
18.  Name 2 HTTP verbs and when would we use each.
19.  What is RegEx and what do we use it for?
20.  On large web applications, what are the benefits of using a framework?
21.  What does a templating engine do for us?
22.  What are 3 different type of database table relationships?
23.  Why do we use routes and how do they work?
24.  What is a virtual environment and why do we use it?
25.  Explain what this code does:  `from flask import Flask`
26.  What is the importance of normalizing your database?
27.  What is an API?
28.  What is AJAX and why do we use it?
29.  What is the difference between an HTTP request/response and an AJAX request/response?
30.  What is the difference between client-side and server-side validations, and when do we use either or both?
31.  What are the major differences between Flask and Django?
32.  What are the differences between tuples, lists, and dictionaries?

# High Level: Career Opportunities (please spend no more than 20 minutes reviewing this)

For more detailed information on different career opportunities in tech, please see: [https://goo.gl/hEDqSf](https://goo.gl/hEDqSf). All of these information will be provided once you graduate and as you attend the career workshop, so please do not spend more than 15 minutes going through the document. The goal of this is just to give you a high level overview of what type of job opportunities are available for you and also how these technologies that you've learned (as well as what you'll learn in the next few months) relate with these opportunities.

  
<img src="https://i.ibb.co/gFQZ7sY/Career-Opportunities.png" border="0">


# Assignment: DojoReads (Belt Reviewer)

This assignment is optional and if you haven't already finished all the mandatory assignments, you should finish them first before working on this assignment. Most likely if you were able to build the wall and felt comfortable with the assignments, you'll do fine with the belt exam. If you do want additional preparation, please feel free to work on this assignment but be aware that as soon as you take your belt exam, you're expected to immediately start working on your project.

Using the below wireframe, create a Django application where logged in users can view and add book reviews. A user should also be able to delete his/her own reviews.

<img src="https://i.ibb.co/80wdhkc/chapter3834-6666-sample1-books.png" alt="chapter3834-6666-sample1-books" border="0">

## Belt Exam Notes

Your belt exam consists of two parts.

The first part will be a 10-minute short-answer portion to cover some key concepts of web development in Python. After the short-answer portion, you will proceed to the second part.

The second part consists of 4.5 hours with another 30 minutes for any interruptions that you may encounter (phone calls, bathroom breaks, etc). You’ll be given a wireframe of a web application and asked to both create it (from database to front-end) and deploy it.

The exam will be conducted during class if you’re part of the on-site bootcamp. Generally, you take the exam through [learn.codingdojo.com/exams](http://learn.codingdojo.com/exams).

For the sample exam above, you can take as much time as you want. Here are helpful tips to help you earn your belt:

-   Know that many of our black belt students had to take the belt exam two or even three times. These exams are _NOT_ easy. We give these exams to those that apply to join Coding Dojo staff as an instructor/consultant, many of whom have 5-7+ years of experience, and 70-80% of them fail the exam. Do NOT get discouraged, and even if you fail the first time, take it again until you can earn your red/black belt. We believe that all of our students _can_ get belts. It’s just a matter of time and perseverance.
-   Make sure you understand how to pass parameters via URL (e.g. http://localhost/users/show/5).
-   Make sure you really understand how to do login and registration. You will need that functionality for the exam.

  

After you complete the belt reviewer above, we strongly encourage that you talk to other members of your cohort to see how they’ve done the assignment. Seeing how others have done the sample exam will help you to appreciate different ways of doing things and will help you to become a better developer.


## (but highly recommended) Assignment: User Dashboard

Complete the below wireframe using Django.

<img src="https://i.ibb.co/d7b67xg/chapter3834-6665-user-dashboard.png" border="0">

Download the image here:  [user-dashboard.pdf](https://s3.amazonaws.com/General_V88/boomyeah/company_209/chapter_3834/handouts/chapter3834_6841_user-dashboard.pdf)

This is one of the best assignments you can do to prepare for the qualifying belt exam, as well as to improve your coding skills. It’s designed to ensure you’ve internalized the fundamentals of web programming, and many of our students have made this a part of their portfolio.

We encourage you to finish this assignment if you have time. Also,  _make sure_  you use Git to back up your code along the way.

Send the link to your Github repo to your instructor when you’ve completed the assignment.


