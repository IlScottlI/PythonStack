# Overview

## Objectives:

-   Get excited about going full stack
-   Install PyMySQL

----------

Adding a database to your application is very simple, but extremely powerful. We've seen how we can get information posted from a form and learned how to set session variables. Now we are going to learn how to put that information into our database and use session variables to log a user in! With the database in the mix, we can now start to make our content dynamically change based on a particular user or condition.

To be able to connect our Flask applications to a database, we're going to need a package to help us. We're going to use one called PyMySQL.  **With your virtual environment activated,**  run the following command in your command line:
```py
(py3Env) $ pip install PyMySQL
```
**Note**

If you use python3 on your OS, you may need to use the following:
```py
(py3Env) $ pip3 install PyMySQL
```
Let's go full stack!

# SQL Query Review (Quiz)

1. Which of the following would correctly retrieve all the pet information from our database?

- [X]   SELECT * FROM pets;
- [ ] GET * FROM pets;
- [ ]  SELECT name FROM pets;
- [ ]  RETRIEVE * FROM pets;

2. Which of the following would correctly add a pet to our database?

- [ ]  ADD TO pets name="Clifford", type="dog", created_at=NOW, updated_at=NOW;
- [ ]  INSERT INTO pets VALUES id=6, name="Clifford", type="dog", created_at=NOW(), updated_at=NOW();
- [X]  INSERT INTO pets (name, type, created_at, updated_at) VALUES ("Clifford", "dog", NOW(), NOW());
- [ ]  CREATE name="Clifford", type="dog", created_at=NOW(), updated_at=NOW() INTO pets;

3. Which of the following would correctly update an existing pet in our database?

- [ ]  CHANGE pets id=4 TO name="Arthur", type="aardvark", updated_at=NOW();
- [X]  UPDATE pets SET name="Arthur", type="aardvark", updated_at=NOW() WHERE id=4;
- [ ]  CHANGE pets TO name="Arthur", type="aardvark", updated_at=NOW() WHERE id=4;
- [ ]  UPDATE pets SET name="Arthur", type="aardvark", updated_at=NOW();

4. Which of the following would delete a specific row in our database?

- [ ]  DELETE id, name, type, updated_at, created_at FROM pets WHERE id=5;
- [ ]  REMOVE id from pets WHERE id=5;
- [ ]  DELETE FROM pets;
- [X]  DELETE FROM pets WHERE id=5;


# MySQL Workbench Review

## Objectives

-   Review how to create ER Diagrams in MySQL Workbench
-   Forward engineer schemas onto our MySQL server

----------

If you need a refresher for using MySQL Workbench, here are a few videos to review. We will be creating new schemas for each of the assignments in this chapter.

### ERDs

### MySQL Server

# Connecting to a Database

## Objectives:

-   Refresh our MySQL Workbench skills
-   Create a sample database
-   Use OOP to handle the connection and queries between a Flask app and a MySQL database

----------

For every project involving a database, we'll go through the following steps.

1.  We'll of course need a database to connect to. Let's create one in the workbench called  _first_flask_  with a single table (see the ERD on the right). If you need a reminder about how to create a database in MySQL Workbench, watch the second video in the previous tab. After creating it, let's go ahead and  _seed_  the database (put a few entries into the table manually).
    
    <img src="https://i.ibb.co/L66bgbd/chapter3011-3906-Screen-Shot-2015-08-24-at-3-20-17-PM.png" alt="chapter3011-3906-Screen-Shot-2015-08-24-at-3-20-17-PM" border="0">
    
2.  Next, create a new project called  _first_flask_mysql_. In addition to the server.py file we make in each project, we'll now also need the following file.  **If you are having trouble with copying and pasting the code below**, download the file  [here](https://s3.amazonaws.com/General_V88/boomyeah2015/codingdojo/curriculum/content/chapter/mysqlconnection.py), or type it from scratch :)
    
    #### first_flask_mysql/mysqlconnection.py
    ```py
    # a cursor is the object we use to interact with the database
    import pymysql.cursors
    # this class will give us an instance of a connection to our database
    class MySQLConnection:
        def __init__(self, db):
            connection = pymysql.connect(host = 'localhost',
                                        user = 'root', # change the user and password as needed
                                        password = 'root', 
                                        db = db,
                                        charset = 'utf8mb4',
                                        cursorclass = pymysql.cursors.DictCursor,
                                        autocommit = True)
            # establish the connection to the database
            self.connection = connection
        # the method to query the database
        def query_db(self, query, data=None):
            with self.connection.cursor() as cursor:
                try:
                    query = cursor.mogrify(query, data)
                    print("Running Query:", query)
         
                    executable = cursor.execute(query, data)
                    if query.lower().find("insert") >= 0:
                        # INSERT queries will return the ID NUMBER of the row inserted
                        self.connection.commit()
                        return cursor.lastrowid
                    elif query.lower().find("select") >= 0:
                        # SELECT queries will return the data from the database as a LIST OF DICTIONARIES
                        result = cursor.fetchall()
                        return result
                    else:
                        # UPDATE and DELETE queries will return nothing
                        self.connection.commit()
                except Exception as e:
                    # if the query fails the method will return FALSE
                    print("Something went wrong", e)
                    return False
                finally:
                    # close the connection
                    self.connection.close() 
    # connectToMySQL receives the database we're using and uses it to create an instance of MySQLConnection
    def connectToMySQL(db):
        return MySQLConnection(db)
    ```
    At this time, you do not need to know how to create one of these files. By the end of the bootcamp, you will be experienced enough to create your own connection files!
    
    Read all of the comments in the mysqlconnection.py file to understand how it works. While you don't have to understand everything 100%, you should know how to use the file and recognize the principles of OOP at work.
    
    -   SELECT queries will return a  _list of dictionaries_
    -   INSERT queries will return the  _auto-generated id_  of the inserted row
    -   UPDATE and DELETE queries will return  _nothing_
    -   If the query goes wrong, it will return  _False_
    
3.  Now let's update our server.py file to connect to the database through the class we just created above.
    
    #### first_flask_mysql/server.py
    ```py
    from flask import Flask, render_template
    from mysqlconnection import connectToMySQL    # import the function that will return an instance of a connection
    app = Flask(__name__)
    @app.route("/")
    def index():
        mysql = connectToMySQL('first_flask')	        # call the function, passing in the name of our db
        friends = mysql.query_db('SELECT * FROM friends;')  # call the query_db function, pass in the query as a string
        print(friends)
        return render_template("index.html")
                
    if __name__ == "__main__":
        app.run(debug=True)
    ```
    **Note: We will need to call on the  `connectToMySQL`  function  _every time_  we want to execute a query**  because our connection closes as soon as the query finishes executing.
    
4.  Run the server and see what gets printed in the terminal when you go to localhost:5000!
    

#### Video Overview


# MySQL Connection Errors

## Objectives:

-   Gain familiarity with how the connection from Flask to MySQL works

----------

This may seem like an odd assignment, but getting errors is one of the best ways to start uncovering how things work, and what different parts of our code do.

Using the project you made in the previous tab, go into the mysqlconnection.py file and produce as many PyMySQL errors as possible  **in twenty minutes**. Try using mistyped strings, an incorrect username, remove values, etc.

Copy and paste those errors in a .txt file and explain how you got to that error.

- [ ]  Spend 20 minutes generating errors
    
- [ ]  Record the errors in a text file
    
- [ ]  Upload your text file

# Retrieving and Displaying Data

## Objectives:

-   Practice interacting with a MySQL database from a Flask application
-   Fetch data from your database and display it on the webpage

----------

Let's continue what we started in the last module and create a very simple webpage where we can track all of our friends! We will implement the functionality to add friends and view friends through the website. All friends will be stored in the database.

When the user visits the root route, we want to display all the friends, so our logic will include fetching all the friends from the database, and then rendering that data onto our template.

**first_flask_mysql/server.py**  
```py
@app.route('/')
def index():
    mysql = connectToMySQL("first_flask")
    friends = mysql.query_db("SELECT * FROM friends;")
    print(friends)
    return render_template("index.html", all_friends = friends)
```
Then in our template:

#### first_flask_mysql/templates/index.html
```html
<h1>All My Friends</h1>
{% for one_friend in all_friends %}
    <p>First Name: {{one_friend["first_name"]}}</p>
    <p>Last Name: {{one_friend["last_name"]}}</p>
    <p>Occupation: {{one_friend["occupation"]}}</p>
    <hr>
{% endfor %}
```
Let's take a look at localhost:5000!

#### Video Overview


# Queries with Variable Data

## Objectives:

-   Learn about prepared statements

----------

With our  `SELECT * FROM friends`  statement, we are just asking for everything from the database. However, we will often want to provide variable data in the query that would be terrible to hard-code into the query. For example:

-   `SELECT * FROM friends WHERE id=1`  (where the actual id number will vary)
-   `UPDATE friends SET first_name="Bryanna" WHERE id=9`  (where the actual first name and id will vary)

**Whenever we run a query that includes variables, we should use a prepared statement rather than string interpolation**. In other words, use the following pattern instead of f-strings or string concatenation. We'll discuss  _why_  shortly. Practically what this means is that we'll need a  **string variable for the query**  and then a  **dictionary for the values to be used in the string**. When we call on the database connection to execute the query, we will pass both the query and the dictionary, like so:

<img src="https://i.ibb.co/ZHmXghr/prepared-Statement.png" alt="prepared-Statement" border="0">

-   **connection to the db  -  mysql**  - the instance of the MySQLConnection class
-   **query string  -  "INSERT INTO ..."**  - the string that will eventually be executed on our MySQL server
-   **data dictionary**  - the values that will be interpolated into the query string
-   **data dictionary keys  -  fn, id_num**  - the keys of the data dictionary used in the query string with %-interpolation

-   (i.e.  **%(key_name)s**)

We'll go over a fleshed out example in the next module.


# From Form to DB

## Objectives:

-   Practice interacting with a MySQL database from a Flask application
-   Create data in your database based on user input
-   Learn how to use prepared statements to run INSERT queries

----------

Now that we can retrieve friends, let's add the functionality that allows us to create a friend. This will be handled by the route that we set for the 'action' attribute in our form. Let's add a form to our template:

#### first_flask_mysql/templates/index.html
```html
<h1>Add a Friend</h1>
<form action="/create_friend" method="POST">
    <p>First Name: <input type="text" name="fname"></p>
    <p>Last Name: <input type="text" name="lname"></p>
    <p>Occupation: <input type="text" name="occ"></p>
    <input type="submit" value="Add Friend">
</form>
```
Now we need a method to handle the submission of our form. Let's update our server.py file and think about the SQL query we're going to want to run:

#### first_flask_mysql/server.py
```py
@app.route("/create_friend", methods=["POST"])
def add_friend_to_db():
    print(request.form)
    # QUERY: INSERT INTO first_flask (first_name, last_name, occupation, created_at, updated_at) 
    #                         VALUES (fname from form, lname from form, occupation from form, NOW(), NOW());
```
**Remember that because this query includes variables, we should use a prepared statement**. Following the pattern from the last page, here's how we can combine the form's information with our query:

<img src="https://i.ibb.co/P14Ydp3/mysql.png" alt="mysql" border="0">

-   route  -  /create_friend  - the route that will handle the submission of the form
-   method  -  POST  - the type of request, generally a POST request
-   input names  -  fname, lname, occ  - the names on all input fields that will become the keys of the request.form dictionary
-   connection to the db  -  mysql  - the instance of the MySQLConnection class
-   query string  -  "INSERT INTO ..."  - the string that will eventually be executed on our MySQL server
-   data dictionary  - the values that will be interpolated into the query string
-   data dictionary keys  -  fn, ln, occup  - the keys of the data dictionary used in the query string with %-interpolation (i.e.  **%(key)s**)

To Python, the query variable is just a string, and the data dictionary just another variable. But when passed to our MySQL server through our PyMySQL connection, our MySQL database understands the string as a query it can execute!

Once the data has been processed, remember to redirect, because we don't want to render on a post!

Note: We have set up the query_db method so that each attempted query will be printed to the terminal.  _Whenever the query you put together does not seem to work or gives an error message, investigate the actual query being run in the terminal. You may try copying and pasting the query into MySQL Workbench to see if you have the right syntax._

#### Overview Video

# SQL Injection

## Objectives:

-   Learn about SQL injection
-   Learn how to prevent SQL injection

----------

As mentioned in the last module, let's discuss further why we want to use prepared statements.

Take a look at this code snippet. Hopefully it feels familiar:
```sql
query = "SELECT * FROM users WHERE email = %(email)s;"
data = { 'email' : request.form['email'] }
result = mysql.query_db(query, data)
```
Here, we are using a  **prepared statement**  in order to create our SQL query with data provided by our user. This is done by leaving placeholders in our query that are filled in with the values from our data dictionary.

Maybe you're thinking it seems tedious to create a dictionary just to pass the user's email input into the query. Perhaps we can be clever and use literal string interpolation to generate our query, and save ourselves from the step of making a dictionary at all.

***** DANGER, LAZY CODING BELOW *****
```sql
# this code is for demonstration purposes only
# DO NOT use this code in production, it will leave you vulnerable to SQL injection
query = f"SELECT * FROM users WHERE email = '{request.form['email']}';"
result = mysql.query_db(query)
```
This might save us some code, but it is not worth it! Creating a query this way allows for  **SQL injection**, which means that we are vulnerable to any input that a user may provide in the form,  _such as more SQL code_. For example, consider what will happen if our user types the following into our form's email input:

<img src="https://i.ibb.co/jk22M91/emailinput.png" alt="emailinput" border="0"></a>  

By using plain string interpolation, this would turn our query into:
```
SELECT * FROM users WHERE email = 'joe@gmail.com' OR '1'='1'; 
```
Since '1' = '1' will always evaluate to true, this query will now fetch all the data from the users table. We may have just opened a huge portion of our database to a malicious user. Any user with SQL knowledge may easily figure out how to manipulate our SQL queries. They may gain access to sensitive data or force us to run a very dangerous query.

### Other Examples of SQL Injections

Consider another scenario where the user put in the following as their email:
```
joe@gmail.com"; DROP TABLE users;
```
What would have happened if the way you prepared the SQL query was like this?  
```sql
query = f"SELECT * FROM users WHERE email = '{request.form['email']}';"
result = mysql.query_db(query)
```
The query it would have run would have been
```
SELECT * FROM users WHERE email = "joe@gmail.com";  DROP users;
```
In other words, it would have dropped the entire users table!

What if the user passed the following as their email input?
```
joe@gmail.com"; UPDATE users SET password = '____' WHERE id = '___'
```
This would have changed someone's password. Similarly, you can see how one could set oneself to be an admin or retrieve sensitive information from other users table (e.g. credit card, address, etc). The possibilities are endless.

Now that you're feeling paranoid about SQL injection, cheer yourself up with this  [xkcd comic](https://xkcd.com/327/)!

## Prepared Statements to the Rescue

Fortunately, by using  **prepared statements**, we can be assured that the user input will not be interpreted as SQL code. Our users may type in all the dangerous characters they'd like - apostrophes, semicolons, parentheses - and it won't matter. With the prepared statement, everything will simply be treated as a regular string, so our query will be harmlessly nonsensical as it looks for an impossible email address:
```
SELECT * FROM users WHERE email = "joe@gmail.com' OR '1'='1"; 
```
There are many ways to protect against SQL injection, including using a framework and trusted libraries. For example, the way we currently have PyMySQL set up, we will not be able to run more than one query at a time. Users will therefore not be able to attach extra queries to ours. We may also try to  **sanitize**  strings from our post data manually by  **escaping**  special characters with the '/' character.

Let's definitely stick with running queries by using the following pattern any time user input is concerned:
```sql
query = "SELECT * FROM users WHERE email = %(email)s;"
data = { 
    'email' : request.form['email'] 
}
result = mysql.query_db(query, data)
```
## Overview Video

# Assignment: Create and Read Pets

## Objectives:

-   Practice setting up a database in MySQL
-   Create a Flask application that displays data from a MySQL database
-   Take user input and add it to the database
-   Practice redirecting after going to a POST route

----------

Create an application where you can view all pets and add new ones. Use the following ERD as a guide:

<img src="https://i.ibb.co/m07mMGp/pets.png" alt="pets" border="0">

Have the main page show all pets and their data as part of a table. On the same page, allow users to enter data and submit that data to the database in order to add a new friend. How many routes do you need? What should each do? Think back to routing from the previous section, and remember never to render from a post route (once you're done building the features you need).

<img src="https://i.ibb.co/t2tpT97/CRPets.png" alt="CRPets" border="0">

- [ ]  Create a new Flask project
    
- [ ]  Create a new database with one pets table in MySQL
    
- [ ]  Create the template as shown in the wireframe
    
- [ ]  Allow pets to be added via the form
    
- [ ]  Display all pets on the table in the template
    
- [ ]  NINJA BONUS: Alter your queries to allow for SQL injection and then simulate an SQL injection attack on your database

# Assignment: Semi-Restful Users

## Objectives:

-   Practice connecting a Flask application to a MySQL database
-   Practice validating user input and using flash messages
-   Complete a full CRUD app (be able to create data, read data, update data, and delete data)

----------

Create a web app that can handle all of the CRUD operations (create, read, update and destroy) for a table. Create a database with a friends table that has first name, last name, email, created_at, and updated_at fields.

It's very common for a web application to provide the user interface for creating, reading, updating, or destroying a 'resource' (a row in a table). Since many web applications perform CRUD operations, you can imagine how confusing this could get if everyone followed different conventions for creating routing and method names for these operations.

A REST or RESTful route is simply a set of route naming conventions that the industry has agreed to follow in order to make it easier to send requests to APIs. We strongly encourage you to get familiar with the following rules for RESTful routing. (This will be handy when you're ready to create your own API!)

Follow the instructions in the wireframe below to build this application in Flask. To keep this organized, try to focus on just one route and template at a time.

<img src="https://i.ibb.co/HgpfnbT/CRUD-Users-Flask.png" alt="CRUD-Users-Flask" border="0">

- [ ]  Complete each of the following routes:
    
- [ ]  /users/new- GET - method should return a template containing the form for adding a new user
    
- [ ]  /users/create - POST - method should add the user to the database, then redirect to /users/<id>
    
- [ ]  /users/<id> - GET - method should return a template that displays the specific user's information
    
- [ ]  /users - GET - method should return a template that displays all the users in the table
    
- [ ]  /users/<id>/edit - GET - method should return a template that displays a form for editing the user with the id specified in the url
    
- [ ]  /users/<id>/update - POST - method should update the specific user in the database, then redirect to /users/<id>
    
- [ ]  /users/<id>/destroy - GET - method should delete the user with the specified id from the database, then redirect to /users
    
- [ ]  NINJA BONUS: Add a description (textarea) field to the user table and update the templates appropriately
    
- [ ]  NINJA BONUS: Ensure all the fields on the edit form are pre-populated (not just with placeholders)

# Basic Form Validation

## Objectives:

-   Learn why we should  _validate_  user input before using it or adding it to the database
-   Learn how to validate user input
-   Learn how to use  _flash messages_  to display error messages

----------

Form validation is a key component of any back-end developer's arsenal.  **Validation**  is more of a logical challenge than a whole bunch of new code to learn. Common validation rules include:

-   Checking that the data is present
-   Making sure the data is in the correct format

The most important validation tool is the if/else statement. Every validation is conditional!  **IF**  the data is not valid, we should let the user know,  **ELSE**  we should process it and update our database. Form validation centers around using  **if**  statements combined with functions that return  **TRUE**  or  **FALSE**  depending on whether the data given is valid.

Let's start adding validations to our previous  _first_flask_mysql_  project. We should have a form already set up on our index.html that is being sent to the create_friend method. This is what we currently have:

#### first_flask_mysql/server.py
```py
from flask import Flask, render_template, request, redirect
app = Flask(__name__)
@app.route('/')
def index():
    mysql = connectToMySQL("first_flask")
    friends = mysql.query_db("SELECT * FROM friends;") 
    print(friends)
    return render_template("index.html", all_friends = friends)
  
@app.route('/process', methods=['POST'])
def add_friend_to_db():
    mysql = connectToMySQL("flask_friends")
    query = "INSERT INTO friends(first_name, last_name, occupation, created_at, updated_at) VALUES (%(fn)s, %(ln)s, %(occup)s, NOW(), NOW());"
    data = {
        "fn": request.form["fname"],
        "ln": request.form["lname"],
        "occup": request.form["occ"],
    }
    new_friend_id = mysql.query_db(query, data)
    return redirect("/")
if __name__=="__main__":
    app.run(debug=True)
```
Right now if we submit the form, the data gets added to the database and then client gets redirected to the index page. We can even submit an empty form and that will get added to the database!  **Our goal will be to validate whether the information provided is valid and ultimately display a message whether the form submission was successful.**

## Step 1: Validations

We're going to focus on the add_friend_to_db method. Here's some pseudocode to highlight what we're going to be adding:
```py
@app.route('/process', methods=['POST'])
def add_friend_to_db():
    # if there are errors:
    	# figure out a way to show the user what went wrong
    # else if there are no errors:
        # code from above to actually insert user into the database
    return redirect("/")
if __name__=="__main__":
    app.run(debug=True)
```
Let's say we expect the first and last names to be required, and the occupation to be at least 2 characters. How should we check? This is where the handy built-in python function  `len()`  comes in!
```py
print(len(""))      # will print 0
print(len("hello")) # will print 5
```
Now we can incorporate this function into our conditional! Let's write out the conditional in actual code. Since we have 3 fields to check, we'll need 3 conditional statements. Since we want to check each one individually, they will be separate if statements. Let's add a boolean value to keep track of whether any of the fields are invalid:
```py
@app.route('/process', methods=['POST'])
def process():
    is_valid = True		# assume True
    if len(request.form['fname']) < 1:
    	is_valid = False
    	# display validation error
    if len(request.form['lname']) < 1:
    	is_valid = False
    	# display validation error
    if len(request.form['occ']) < 2:
    	is_valid = False
    	# display validation error
    
    if not is_valid:    # if any of the fields switched our is_valid toggle to False
        return redirect('/')    # redirect back to the method that displays the index page
    else:               # if is_valid is still True, all validation checks were passed
    	# add user to database
        # display success message
        # redirect to a method that displays a success page
```
## Step 2: Adding Error Messages

Now that we've got the logic set up, let's talk about displaying the error messages. Session is an option, but we only want to display it for a short time, but long enough that the message will still be available after a redirect. Luckily,  **flash messages are strings that exist for just one redirect cycle**! The difference between flash and session is that flash messages only last for one redirect while session stays until it is manually popped.  **This makes flash messages perfect for validations where we only need to display the error or message temporarily!**

To use flash messages we first need to import them from Flask. Under the hood, flash messages actually utilize session, so we need to import session as well. Modify your import statement:
```py
from flask import Flask, render_template, redirect, request, session, flash
```
Now using flash is as easy as invoking the flash function and passing in a string message! Let's first see how this would look in the if statement. Next we'll see how to display the messages on the client-side.
```py
@app.route('/process', methods=['POST'])
def process():
    is_valid = True
    if len(request.form['fname']) < 1:
    	is_valid = False
    	flash("Please enter a first name")
    if len(request.form['lname']) < 1:
    	is_valid = False
    	flash("Please enter a last name")
    if len(request.form['occ']) < 2:
    	is_valid = False
    	flash("Occupation should be at least 2 characters")
    
    if not is_valid:
        return redirect("/")
    else:
    	# add user to database
        flash("Friend successfully added!")
        return redirect("/")    # eventually we may have a different success route
```
Another way to handle multiple validations if using flash messages can be seen here:
```py
@app.route('/process', methods=['POST'])
def process():
    if len(request.form['fname']) < 1:
    	flash("Please enter a first name")
    if len(request.form['lname']) < 1:
    	flash("Please enter a last name")
    if len(request.form['occ']) < 2:
    	flash("Occupation should be at least 2 characters")
    
    if not '_flashes' in session.keys():	# no flash messages means all validations passed
    	# add user to database
        flash("Friend successfully added!")
    return redirect('/') # either way the application should return to the index and display the message
```
## Step 3: Displaying Flash Messages on the Template

The last step is to get those flash messages onto the template! The  [documentation](http://flask.pocoo.org/docs/1.0/patterns/flashing/)  shows us how:
```html
{% with messages = get_flashed_messages() %}     <!-- declare a variable called messages -->
    {% if messages %}                            <!-- check if there are any messages -->
        {% for message in messages %}            <!-- loop through the messages -->
            <p>{{message}}</p>                   <!-- display each message in a paragraph tag -->
        {% endfor %}
    {% endif %}
{% endwith %}
```
**Congratulations! We have learned how to do basic validations.**

#### Video Overview


# Assignment: Dojo Survey With Validation

## Objectives:

-   Practice working with a database
-   Practice validating user input
-   Practice using flash messages

----------

Take the Dojo Survey assignment that you completed previously and add a database and validations! All fields are required.

### <img src="https://i.ibb.co/mDyVypK/chapter2982-3795-survey-form.png" alt="chapter2982-3795-survey-form" border="0">

- [ ]  Create a new database with a table containing the fields indicated in the wireframe
    
- [ ]  Add validations to ensure all fields have a value. Display appropriate validation errors on the survey form if invalid.
    
- [ ]  If data is valid, save the information to the database and redirect to a page displaying the information that was just submitted
    
- [ ]  NINJA BONUS: Allow the comment field to be optional, but if provided should not exceed 120 characters
    
- [ ]  NINJA BONUS: Use a CSS framework to add styling
    
- [ ]  SENSEI BONUS: Create separate database tables for location and language and set up the appropriate relationships between ninja, location, and language.
    
- [ ]  SENSEI BONUS: Seed the location and language tables and have them populate the form fields. Save the form submission accordingly.

# Pattern Validation

## Objectives:

-   Learn about regular expressions (often referred to as regex)
-   Learn how to use regex to validate
-   Learn how to validate an email address
-   Review other methods that can be useful for validating

----------

Another common validation that needs to be performed is checking whether an input matches a certain pattern. For example, email addresses have a particular pattern; passwords are often required to have a certain number of different types of characters. We can achieve this by using something known as a  **regular expression**  or  **regex**.

A regex is a sequence of characters that defines a search pattern. It can be used to match a string that follows a pattern. For example, every email has a series of alphanumeric characters followed by an @ symbol followed by another series of alphanumeric characters followed by a "." and finally another series of alphanumeric characters. You don't need to know how to create regex at this point, but understanding what they are and what they are used for is definitely important. The Python regex for matching an email address based on the above criteria looks something like this (the preceding r indicates the string is a raw string, i.e. all characters should be taken literally):
```py
r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$'
```
The snippets below show the important additions to our server file:

#### some_project/server.py
```py
import re	# the regex module
# create a regular expression object that we'll use later 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
@app.route('/process', methods=['POST'])
def submit():
    if not EMAIL_REGEX.match(request.form['email']):    # test whether a field matches the pattern
        flash("Invalid email address!")
```
The EMAIL_REGEX object has a method called .match() that will return  _None_ if no match can be found. If the argument matches the regular expression, a match object instance is returned.

### Flash Messages with Categories

Say we want to  _categorize_  flash messages into different labels or buckets. We can utilize categories by passing a second argument in the flash function:
```py
flash("Email cannot be blank!", 'email')
```
Here's the  [documentation on flash messages with categories](https://flask.palletsprojects.com/en/1.1.x/patterns/flashing/#flashing-with-categories), where you can learn more about them, including how to display them on templates.

### Other Useful Validation Tools:

-   [str.isalpha()](https://docs.python.org/3.6/library/stdtypes.html#str.isalpha)  -- returns a boolean that shows whether a string contains only alphabetic characters
-   [other string methods](https://docs.python.org/3.6/library/stdtypes.html#string-methods)
-   [time.strptime(string, format)](https://docs.python.org/3.6/library/time.html#time.strptime)  -- changes a string to a time using the given format

# Assignment: Email Validation with DB

## Objectives:

-   Practice reading from and inserting into a database
-   Validate user input before adding it to the database
-   Practice using regex
-   Practice using flash messages
-   Practice redirecting after going to a POST route
-   Consider front-end versus back-end validations

----------

Create an application that asks a user to enter an email address and validates it.

#### index.html

A simple form for the user to submit an email.

<img src="https://i.ibb.co/F3B5DNZ/chapter3207-5866-email-validation-assignment1.png" alt="chapter3207-5866-email-validation-assignment1" border="0">

#### Error

If the email address is not valid, have a notification "Email is not valid!" to display on the homepage.

<img src="https://i.ibb.co/vPjT4T4/chapter3207-5867-email-validation-assignment2-png.png" alt="chapter3207-5867-email-validation-assignment2-png" border="0">

#### success.html

Once a valid email address is entered, save to the database the email address the user entered. On the success page, display all the email addresses entered along with the date and the time when the email addresses were entered.

<img src="https://i.ibb.co/02vmMHK/chapter3678-7610-basic-2-django.png" alt="chapter3678-7610-basic-2-django" border="0">


- [ ]  Create a new Flask project
    
- [ ]  Create a new database with a table containing an email address field
    
- [ ]  Set up the root route to display a form to input email addresses
    
- [ ]  Validate that the email is in the correct format
    
- [ ]  If invalid, redirect to the root route with an error message
    
- [ ]  If valid, redirect to a success route that displays a success message
    
- [ ]  Have the success route template also display a list of all the entries in the database
    
- [ ]  NINJA BONUS: Also validate that the email being added is unique
    
- [ ]  NINJA BONUS: Add a delete button on the success route allowing for the deletion of a specific email from the database

# Securing Passwords

## Objectives:

-   Understand what hashing is
-   Understand what encryption is
-   Learn techniques for protecting users' passwords
-   Understand what a salt is
-   Discuss the vulnerabilities that hackers might exploit to access our users' passwords

----------

As we've seen, hackers can find ways to gain access to your database. Web developers are responsible for keeping users' data safe. No one should know our users' passwords -  **not even us!** This can be very difficult to do correctly and is largely why we see so many websites offering us the option to sign up via Facebook or Google - they're passing the job of user authentication off to the experts (how you may feel about their expertise is a different matter). This may be an option you would like to explore in the future, but you should still know how to store - and how not to store - users' passwords.

----------

## BAD idea: Directly store passwords in the database

<img src="https://i.ibb.co/X7t7mp6/Screen-Shot-2018-03-19-at-4-24-11-PM.png" alt="Screen-Shot-2018-03-19-at-4-24-11-PM" border="0">

It should be pretty obvious why we would never want to put our users' passwords straight into our database. As we saw when we discussed SQL injection, it may be very easy for malicious users to access data that wasn't meant for them to see. So obviously we would never just store passwords in plain text! (It's obvious now, but unfortunately, many developers have had to learn that lesson the hard way.)

Instead, we'll want to mask the data somehow, so even if hackers got into our database, they wouldn't know what to do with it.

----------

## Good idea, but not good enough #1: Hash the passwords before storing them

<img src="https://i.ibb.co/VVWwkn3/Screen-Shot-2018-03-19-at-4-35-58-PM.png" alt="Screen-Shot-2018-03-19-at-4-35-58-PM" border="0">  

In order to mask our users' passwords, we will use a technique called  _hashing_. Hashing scrambles data in such a way that **cannot be reversed**. This is different from another technique you may have heard of called e_ncryption,_ which scrambles data with the use of an encryption key so that it is reversible. With encryption, anyone with the encryption key may decrypt the data. Ideally, only the sender and the receiver of the data should know the encryption key. Credit card data, for example, should be encrypted. Passwords, however, should be hashed, and we'll only store hashed passwords in our database.

We said that hashing is not reversible, so how can we match passwords? The answer is that a hashing algorithm will always produce the same output for a particular input. Therefore, we'll take the password input when a user logs in, hash it, and compare the hash to the value stored in the database.

Sadly, hashing is supposed to be irreversible, but many of the common hashing algorithms, such as  `md5()` and  `sha1()`, have been hacked and are no longer reliable. Besides, this technique leaves us vulnerable to brute force attacks. Hackers have even made  _rainbow tables,_ which are tables of common passwords (we're looking at you, "password123") and their hashes. Rainbow tables aren't even necessary anymore, though, because modern computers and the hashing algorithms are so fast, it doesn't take long for a hacker's program to test thousands of passwords. Imagine all the harm that could quickly be done with a for-loop like the one below:
```
for password in my_list_of_passwords_to_test:      # loop through every password we want to test
    if md5(password) in table:                     # find out if the md5 hash of the password is in the table
        print("I guessed a password!", password)   # print any passwords that belong to a user     
```
----------

## Good idea, but not good enough #2: Hash the passwords with a salt before storing them

A **salt** is a random long string that we add to a user's password before hashing it and storing it in the database. We'll keep the salt stored in our server. When the user comes back and logs in, we'll concatenate the salt to the password input, hash it, and see if it matches the value in the database. This will greatly reduce a hacker's ability to test common passwords because all the passwords are essentially random strings. However, if a hacker successfully breaks into our server and finds our salt, then we're no better off than we were with our previous idea, because the for-loop is easily adjusted:
```
for password in my_list_of_passwords_to_test:     # loop through every password we want to test
    if md5(password + salt) in table:             # see if the salt is concatenated to the password
        print("I guessed a password!", password)
```
----------

## Good enough #3: Give each user a unique salt

<img src="https://i.ibb.co/GPRVSFC/Screen-Shot-2018-03-19-at-5-14-05-PM.png" alt="Screen-Shot-2018-03-19-at-5-14-05-PM" border="0">

If we give each user a unique salt, we can just store that salt in the database as user data. It may seem silly, because now anyone who gets into our database will have all the salts. However, the point is not to keep the salts secret, but to slow down hackers' ability to test thousands of passwords. Notice our hacker's program now has a nested for-loop, which will take  _much_ longer to run:
```
for user in users:                                       # loop through all the users                
    for password in my_list_of_passwords_to_test:        # loop through every password we want to test
        if md5(password + user['salt']) in table:        # see if the user's salt is concatenated to the password
            print("I guessed a password!", password)
```
So far, this is our best option, and the big benefit it has is slowing down hackers' attempts to brute force their way to finding passwords. Since this strategy of slowing down hackers is the best we have, that leads us to the solution we should use, **Bcrypt.**

----------

## Bcrypt, the best we've got

Bcrypt is a hashing algorithm that is purposefully designed to be slow. It is not so slow to affect a particular user's experience, but hackers who are trying to brute force their way through thousands of passwords will not bother. Other than that, it uses the same ideas as we already listed above. Since it is slow, hackers may resort to rainbow tables again, so Bcrypt generates a salt. Bcrypt adds the salt to the user's password and hashes the result, which we store in the database.

An important thing to note is that, as developers, we have to do all we can to protect our users' data. However, if a user decides to use a weak password, there is nothing we can do. Take this lesson into your own practice. Keep your passwords secure, keep them unusual enough so they will never appear on a rainbow table, never give your password to a site you do not trust, consider using a trusted password manager, and do not reuse passwords for different accounts.

The next module will go over how to implement Bcrypt with your app.

# Flask-Bcrypt

## Objectives:

-   Add Bcrypt to your Flask app to keep passwords more secure
-   Know how to use Bcrypt's methods to hash passwords and compare passwords

----------

With your **virtual environment activated,** run the following command:
```py
(py3Env) $ pip install flask-bcrypt
```
In your Flask project's server.py file, add the following:
```py
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)     # we are creating an object called bcrypt, 
                         # which is made by invoking the function Bcrypt with our app as an argument
```
After making the object  **bcrypt**, we have access to two methods that we will use to generate our password hashes and to compare passwords.

1.  To generate a hash, provide the password to be hashed as an argument
    -   `bcrypt.generate_password_hash(password_string)`
2.  To compare passwords, provide the hash as the first argument and the password to be checked as the second argument
    -   `bcrypt.check_password_hash(hashed_password, password_string)`

Let's explore the  `generate_password_hash()`  method. If we pass it a string and print the result, we may see something like this:
```
$2b$12$sqjyok5RQccl9S6eFLhEPuaRaJCcH3Esl2RWLm/cimMIEnhnLb7iC
```
We will store this string in our database, and there is a lot of information contained in it! Within the first set of $ signs, we have the Bcrypt ID (in this case, 2b). Between the next set of $ signs, the number 12 tells us how many rounds of hashing we did - this is what slows Bcrypt down. If you want it to take even longer, you may pass a larger value as a second argument - just for fun, try asking it to run 17 rounds! The next 22 characters is the salt (128 bits), and the rest is our 184-bit hash.

Next, when we want to verify a user's password, we'll compare it with the hash we have associated with that user in the database. We pass both the hash and the provided password to  `check_password_hash()`. Bcrypt extracts the salt from the hash and applies it to the provided password, hashes it, and compares the result to the saved hash. If they match, it returns True. If not, it returns False.

#### Hashing Upon Registration

Let's see how some of our code may look when we are creating a user. In the example below, we did not include validations, but  _of course_  you would validate the user input before adding it to the database.
```py
@app.route('/createUser', methods=['POST'])
def create():
    # include some logic to validate user input before adding them to the database!
    # create the hash
    pw_hash = bcrypt.generate_password_hash(request.form['password'])  
    print(pw_hash)  
    # prints something like b'$2b$12$sqjyok5RQccl9S6eFLhEPuaRaJCcH3Esl2RWLm/cimMIEnhnLb7iC'
    # be sure you set up your database so it can store password hashes this long (60 characters)
    mysql = connectToMySQL("mydb")
    query = "INSERT INTO users (username, password) VALUES (%(username)s, %(password_hash)s);"
    # put the pw_hash in our data dictionary, NOT the password the user provided
    data = { "username" : request.form['username'],
             "password_hash" : pw_hash }
    mysql.query_db(query, data)
    # never render on a post, always redirect!
    return redirect("/")
```
#### Comparing Upon Login

Here's how our code may look when a user logs in. We'll need to check the provided password with the hash in the database:
```py
@app.route('/login', methods=['POST'])
def login():
    # see if the username provided exists in the database
    mysql = connectToMySQL("mydb")
    query = "SELECT * FROM users WHERE username = %(username)s;"
    data = { "username" : request.form["username"] }
    result = mysql.query_db(query, data)
    if len(result) > 0:
        # assuming we only have one user with this username, the user would be first in the list we get back
        # of course, we should have some logic to prevent duplicates of usernames when we create users
        # use bcrypt's check_password_hash method, passing the hash from our database and the password from the form
        if bcrypt.check_password_hash(result[0]['password'], request.form['password']):
            # if we get True after checking the password, we may put the user id in session
            session['userid'] = result[0]['id']
            # never render on a post, always redirect!
            return redirect('/success')
    # if we didn't find anything in the database by searching by username or if the passwords don't match,
    # flash an error message and redirect back to a safe route
    flash("You could not be logged in")
    return redirect("/")
```

# Assignment: Login and Registration

## Objectives:

-   Build an application that requires login and registration
-   Practice connecting a Flask application to a MySQL database
-   Become familiar with the logic that is required to validate a user's registration to a website
-   Become familiar with the logic that is required to validate a user logging in to a website
-   Process a user logging out of an application
-   Practice using session

----------

In this assignment, you're going to build a Flask application that allows login and registration. We've learned about how we can connect to the database, insert records posted from a form, retrieve records from a database and set a session/flash for any error or success messages that we get along the way. One of the major components to every website is login and registration.

### Registration

The user inputs their information, we verify that the information is correct, insert it into the database and return back with a success message. If the information is not valid, redirect to the registration page and show the following requirements:

#### Validations and Fields to Include

1.  First Name - letters only, at least 2 characters and that it was submitted
2.  Last Name - letters only, at least 2 characters and that it was submitted
3.  Email - valid Email format, does not already exist in the database, and that it was submitted
4.  Password - at least 8 characters, and that it was submitted
5.  Password Confirmation - matches password

### Login

When the user initially registers we would log them in automatically, but for logging in, we need to validate in a different way:

1.  Check whether the email provided is associated with a user in the database
2.  If it is, check whether the password matches what's saved in the database

**But how do we keep track of them once they've logged in?**  I think you might already know...session! We can create a session variable that holds the user's id. From our study in database design, we know that if we have the id of any table we can gather the rest of the information that is associated with that id. Storing a single session variable with the user's id is all we need to access all the information associated with that user.

### Logout

On the success page, have a logout button or link. When a user logs out, their session should be cleared. If the user attempts to access the success page (i.e. making a GET request by typing in the url), redirect them back to the login and registration page.

## Video: Assignment Overview

## Video: Thinking through using session in this assignment

## BONUS:

Add more fields to your registration form with different form elements. For example, include a drop down menu, radio buttons, checkboxes, and a datepicker. Include validations for each field. Have users provide their birthday, and require that they must be at least ten years old in order to register. Level up your password validations by requiring at least one capital letter and one number. Provide the user with several programming languages, and require that they check at least one as an interest of theirs. Customize this assignment and get creative!

- [ ]  Create a new Flask project
    
- [ ]  Create a new MySQL database with a table and the appropriate fields
    
- [ ]  The root route should display a template with the login and registration forms
    
- [ ]  Validate the registration input
    
- [ ]  If registration is invalid, error messages should be displayed on the index page
    
- [ ]  If registration is valid, hash the password and save the user in the database, store the user in session, and then redirect to the success page
    
- [ ]  Validate the login input
    
- [ ]  If login is invalid, display an error message on the index page
    
- [ ]  If login is valid, store the user in session and then redirect to the success page
    
- [ ]  Add a functioning logout button to the success page that clears session
    
- [ ]  After logging out, ensure you cannot reach the success page
    
- [ ]  NINJA BONUS: Add an additional validation on passwords to have at least 1 number and 1 uppercase letter
    
- [ ]  SENSEI BONUS: Add additional input types on the form. Get creative with your validations! (consider including a datepicker, radio buttons, or checkboxes)

# One-To-Many Relationships

### Objectives:

-   Review of One-To-Many relationships
-   Learn how to query across a One-To-Many relationship

For a full review of One-To-Many relationships, please refer to the [module from Web Fundamentals](http://learn.codingdojo.com/m/2/5513/35605), which also covers how to set up a One-To-Many relationship in SQL Workbench.  

## How do One-To-Many relationships work?

In order to create a One-To-Many relationship between our tables, we rely on a field called the  **foreign key**. This field is what allows us to have a common column between our tables that we can then  **join** tables on.

Let’s look at an example of a One-To-Many relationship. The easiest way to figure out whether two tables  **x** and  **y**  have such a relationship is to say the following words out loud:

“X can have many Y”

“Y can have many X”

Only one of these should be true for a One-To-Many relationship. For example:

“States can have many cities” (yup!)

“Cities can have many states” (nope!)

Based on the above, we know that states and cities have a One-To-Many relationship, with states being the “one” and cities being the “many”.

Let’s look at the two tables below, and see how a foreign key allows us to create a relationship between them.

**Table: States**
**id**|**name**|
|--|--|
|1|Washington|
|2|California|
|3|Oregon|
|4|Idaho|

**Table: Cities**

|**id**|**name**|
|--|--|
|1|Seattle|
|2|Tacoma|
|3|Boise|
|4|Portland|
|5|Bellevue|

In order to create the relationship, we will add a foreign key to our  **Cities**  table called “state_id”. In SQL Workbench, this will automatically be done if you use the existing 1:n button.  

**Note: The foreign key always goes in the “many” side of the relationship. Because one state has many cities, we will add the foreign key to the cities table.**

Here is what our  **Cities**  table will look like with the new field:

|**id**|**name**|**state_id**|
|--|--|--|
|1|Seattle|1|
|2|Tacoma|1|
|3|Boise|4|
|4|Portland|2|
|5|Bellevue|1|

As you can see, several cities have the same state_id.

## Querying across tables

There are two main types of queries I might want to do with this kind of relationship--a regular lookup, and a **reverse lookup**. Here are some examples of those two queries on the tables above.

Get the state that Portland is in (regular lookup):
```sql
SELECT name FROM States JOIN Cities ON States.id = Cities.state_id WHERE Cities.name = “Portland”;
```
Get the list of all cities in Washington (reverse lookup):
```sql
SELECT * FROM States JOIN Cities ON States.id = Cities.state_id WHERE State.name = “Washington";
```

# Report Card

### Objectives:

-   Practice setting up a table with a foreign key
-   Practice querying with a one-to-many relationship

Create an application that allows a teacher to add grades to a student report card according to the wireframe and requirements below.

<img src="https://i.ibb.co/XpmQmvZ/One-to-Many-Report-Card.png" alt="One-to-Many-Report-Card" border="0">


- [ ]  Create a database
    
- [ ]  Create tables for students and grades
    
- [ ]  Create the appropriate relationship between tables
    
- [ ]  Create a dashboard that displays all students
    
- [ ]  Create a page that displays the report card of a single student
    
- [ ]  Create a page that allows a teacher to add a new grade to a student's report card
    
- [ ]  NINJA BONUS: Allow the teacher to edit a grade
    
- [ ]  NINJA BONUS: Allow the teacher to delete a grade
    
- [ ]  SENSEI BONUS: Sort the grades on the report card from best to worst

# Assignment: Private Wall

## Objectives

-   Practice connecting a Flask application to a MySQL database
-   Include login and registration
-   Include multiple one-to-many relationships
-   Continue to think about web security and how others could potentially hack your site

----------

For this assignment, a user's "wall" is a list of their private messages. Once a user has logged in, they can view their wall and, on this same page, the logged in user can also send messages to other users. The yellow sticky notes indicate basic functionality. Review the green sticky notes for Ninja Bonuses and purple sticky notes for Sensei Bonuses.

<img src="https://i.ibb.co/2NckztW/Wall-Flask.png" alt="Wall-Flask" border="0">

## Additional Sensei Bonus

For the delete functionality, do not allow someone to remove a message that doesn't belong to them. If someone tries to remove a message that doesn't belong to them, have your app display the following:

<img src="https://i.ibb.co/dB6ZCPf/danger.png" alt="danger" border="0">

You don't really need to build the feature to report the IP address, but do log the user out if they try to remove a message that doesn't belong to them for the second time in a row. We'll leave it up to you to find out how to find the IP address of the user (a simple google search will show you how to do this in Flask).

## Video: Tips


# Checkpoint - Flask or Django? and what's next

Congratulations on making it this far! Let's take a moment to step back and understand what you've learned and what lies ahead.

If you have not skipped any of the mandatory assignments (and you should never skip any mandatory assignments), you would have started understanding the following fundamentals that we think are most important in building any web applications.

-   Understanding of HTTP request/response cycle
-   Submitting information using Form and handling the data using POST
-   Storing information in Session securely (a bit more lesson in the later modules)
-   How to pass information from Database to the application (and include this in HTMl, CSS, or Javascript)
-   Basic Security (preventing from sql injection, hacking session, form validation - both front end and backend, password encryption)
-   Basic understanding of Ajax (Ajax will be introduced in the next chapter)
-   How to put together basic SQL statements (select, insert, delete, simple group by statements)
-   Basic understanding of OOP and familiarity with its syntaxes

At CodingDojo, we have spent the last 10+ years really trying to understand the fastest way for students to understand these key assignments and have very carefully laid out all the mandatory assignments. We really believe that doing the mandatory assignments (sometimes over and over) and getting familiar with the concepts presented in these mandatory assignments is really the best way and the fastest way to master these key concepts.

At this point, we recommend that you reflect back and see if you're somewhat comfortable with the concepts above and also ask yourself, if you had to rebuild the Private Wall assignment from scratch (including login and registration), how long it would take you to build that. If the answer is more than 8 hours, my strong recommendation is to NOT move forward with Django but to

1.  Go back and make sure you finish all the mandatory assignments up to Adding AJAX
2.  Make sure you devoted some time to understand AJAX. No one can call themselves a true developer unless they understand and know how to use AJAX.
3.  Make sure you are feeling comfortable with SQL queries. Knowing how to do SQL queries is extremely important.
4.  Instead of moving on to Django, dwell in Flask and get very comfortable with the concepts in Flask. You can build all enterprise applications in Flask and do NOT need Django. You can also take the whole belt exam in Flask and it counts exactly the same as taking the exam in Django.

Now, Django does have some useful features and if you've mastered the fundamentals up to this point, then Django will be a nice thing to know. If you haven't truly understood the fundamentals yet and move on to Django, not only it will take you much longer to learn Django (than if you just mastered the fundamentals and then moved on to Django), you may also build some bad habits and do things without truly understanding why things are being done that way.

My recommendation for those who are not able to build the Private Wall assignments in 8 hours from scratch (including login and registration), is always to stay in Flask, get familiar with AJAX, take the test in Flask, and then spend some time on weekends or project week to get familiar with Django. All students who take this route felt much better about their ability to build enterprise level applications and were able to get to self-sufficiency a lot faster (than students who did not heed to this advice and skipped the mandatory assignments up to this point).

Also, please remember that one of the best ways to learn is by helping other cohort members and verbalizing concepts you've just learned. Without verbalizing what you've learned, you'll find it's much easier to forget. Learn and verbalize what you've learned by helping others, and you'll find that you will retain that information a lot better but also more deeply understand the concepts you've just learned.

# Leads and Clients (optional but strongly recommended for all students to complete)

## Objectives:

-   At a deeper level, understand how the server generates a http response which the browser can use to render the html/css or to give to the Javascript interpreter.
-   Have you get exposure to generating beautiful graphs/plots using jQuery and know how to insert information from the database to Javascript.

----------

In the  [Lead Gen Business assignment](http://learn.codingdojo.com/m/2/5514/35640)  from Web Fundamentals/MySQL, you wrote some complex queries for leads, sites, and clients. In this assignment, you'll use some of those queries to create a simple report dashboard:

<img src="https://i.ibb.co/XstJpWh/leads-clients.png" alt="leads-clients" border="0">

The main goal of this assignment is to see how you can get data from your Flask server and use it in script tags on the template. Start by pulling all the appropriate information from the database to generate the table and the graph.

If you have time, allow the user to change the reporting date range by adjusting the two dates on the top right. This assignment can be a bit difficult but teaches a lot of great lessons that could save you lots of time later when you're working on real complex projects.

#### Tips

-   In the wireframe/assignment,  _customers_  and  _clients_  are used interchangeably.
-   Test your queries in MySQL Workbench/MySQL command line to ensure you don't have any syntax issues and that your query is doing what you think it's doing.
-   Use inspect element to view the data being rendered in your script tags.
-   Don't forget that "" indicate literal strings, while words without quotes are read as variables.
-   Play around with the code directly at  [https://canvasjs.com/jquery-charts/animated-chart/](https://canvasjs.com/jquery-charts/animated-chart/)  to make sure you understand what it's doing and get a sense for which parts you'll need to update.

#### Video Overview

- [ ]  Write and test the query in MySQL Workbench to obtain a list of client names and the total # of leads they've generated (for all time)
    
- [ ]  Create a new Flask project and create a template that mirrors the wireframe provided
    
- [ ]  Take a few minutes to read through the code found here and try to get a basic idea of what it's doing: https://canvasjs.com/jquery-charts/animated-chart/
    
- [ ]  Create a template mirroring the wireframe above, and include the JavaScript code found in the link above
    
- [ ]  Provide the appropriate data from your Flask server to the template and have it render the data for clients and number of leads
    
- [ ]   NINJA BONUS: Allow the user to select start and/or end dates and have the data table and chart display update accordingly
    
- [ ]  SENSEI BONUS: Explore other charts/graphs available and render data from another query

# Admins (Advanced Login)

## Assignment Objectives:

-   Gain a deeper understanding on what's happening behind the scene when a user logs in
-   Understand how to create and grant different user access levels
-   Continue to think about web security and how to make the application more secure

----------

Build upon the previous login and registration assignment, but add an additional field in the users table that indicates whether the user is an admin. For this particular assignment, create a new field called user_level where user_level of 1 indicates a "normal user" and user_level of 9 indicates a "super admin". For other limited access, you may later assign some users to user_level of 2-8. For now, you decide to just create two type of users: a normal user with user_level of 1 or a super admin with user_level of 9.

After manually making one of your users a super admin, depending on whether the logged in user is a super admin or a normal user, redirect the user to a different page (see below).

<img src="https://i.ibb.co/zRT0GFS/Advanced-Login.png" alt="Advanced-Login" border="0">

Like the previous assignment, do NOT allow a normal user to access the url they are not supposed to. For example if a normal user tries to visit "/admin" or say "/remove/13" (to remove user 13) or "/make_admin/5" (where it makes user 5 a super admin), do not allow them to do anything but where you log them off and redirect them to a page like below:

<img src="https://i.ibb.co/KKxS14X/danger2.png" alt="danger2" border="0">

Continue to think about how a malicious user could potentially hack your site and continue to think about web security.

## Additional Video (admin features and advanced security)


# Session Security with Login

Storing user_id in session and relying only on that to verify that the user logged in could be dangerous. Please watch the video below to see how you could make your application more secure.

