
# Introduction to ORMs

## Objectives:

-   Understand what an ORM is
-   Understand the pros and cons of an ORM

----------

It's time to get to full-stack and integrate a database! Django has its own database that is automatically created inside the project folder. It's in a file called db.sqlite3, and it won't be human readable, just know that you should not delete it!

We could use SQL queries in order to write and read from this database, but Django actually provides us something that makes this step unnecessary--an Object Relational Mapper.

Let's take a moment to get a better understanding of what an Object-Relational Mapper (ORM) is and what it does. Practically speaking, Django's ORM allows us to write pure Python code without having to manage long SQL query strings in our logic. You know from experience how cumbersome SQL queries can get when doing complex statements. The ORM helps our code become much clearer and easier to read.

Think back to OOP and working with  _instances of a class_. While our database is still written in SQL, an ORM can translate each row in a table to an  _instance of a Python class_, with each of the database fields being an  **attribute**  of the class. The ORM also comes with  **methods**  that actually perform SQL queries. We'll also add our own methods to customize the functionality of our classes.

An ORM can also help address some security concerns by sanitizing user-provided data and preventing SQL injection attacks. Watch the video below to understand more about these concerns and how and why you should be aware of these features.

# Models in the MTV (MVC) Structure

## Objectives:

-   Understand why Models are a separate component of the MTV (MVC) architecture
-   Learn how to build a Django model

----------

## The Why

Let's get started using the ORM! Models are the M of the MTV architecture. Remember that the goal of modularizing is to separate our code so that each part has a specific purpose.

The purpose of models is to do all the work of interfacing with the database, whether retrieving information from or putting information into it. The phrase  **skinny controllers and fat models**  is often used to describe this design pattern:

_As a general rule, any heavy logic, including database queries, should be performed by the Model. If a controller (in Django, that's the views.py file) needs to perform logic or get information from the database, it should use a Model method to do so._

## The How

When we created our app, the Django CLI actually set up the  `models.py`  file for us. So far we have left it empty, but it's finally time to use it!

**Models**  are simply  **classes**  that map to our database tables. We'll start with just one table, and then talk about adding relationships over the next few modules and assignments. On the left is the ERD as we might have designed it in MySQL Workbench. On the right is the corresponding class we will actually write in our models.py file.

#### Hypothetical MySQL Workbench Diagram

#### my_app/models.py

<img src="https://i.ibb.co/gZ4m6KD/movies-ERD.png" border="0">

```py
from django.db import models
    
class Movie(models.Model):
    title = models.CharField(max_length=45)
    description = models.TextField()
    release_date = models.DateTimeField()
    duration = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```
Let's break down the code in the models.py file a little bit:

##### Why models.Model?

First, notice we are  _inheriting_  from the  `models.Model`  base class. If you didn't have a chance to practice inheritance back in the OOP chapters,  _**inheritance**_  is an important OOP principle that allows us to write code in one class (parent) and then allow other classes (children) to  _inherit_  that same code without having to re-write it in the child classes.

Practically speaking, this means that, even though we don't see additional code, Django's Model class provides a lot right out of the box. There's no way the Django developers could have anticipated all the different classes we as developers might create, but what they could anticipate was that we'd need classes, and that these classes would need to be created in our database, and they'd each need a primary key field. With that in mind, they created one generic parent Model class that contains these fields and functionalities.

You'll notice, for example, that we do not need to type an  `id`  field into any of our classes--Django automatically adds a field called "id" to every class inheriting from models.Model and sets it to be an auto-incremented field. We also don't have to write a separate  `__init__`  method for each class. Very shortly, we'll also see the models come pre-loaded with all the CRUD functionality so we aren't required to write out all the SQL statements.

##### Other Fields

Besides the id field, you'll notice that every field from our ERD has a corresponding line in our class. Each field is named and its type is specified. (We won't talk about relationship fields yet--those will come soon enough!) This is a great opportunity to begin reading documentation. The documentation will tell you what is required for each field type and what other options you can specify for each field. You can find a full list of allowed column types  [here](https://docs.djangoproject.com/en/2.2/ref/models/fields/#field-types). Below is a list of a few common types with some brief explanations to help you get started.

-   [CharField](https://docs.djangoproject.com/en/2.1/ref/models/fields/#charfield)
    -   Any text that a user may enter. This has one required parameter,  `max_length`, that is the maximum length of text that can be saved.
-   [TextField](https://docs.djangoproject.com/en/2.1/ref/models/fields/#textfield)
    -   Like a  `CharField`, but with no maximum length. Your user could copy the entire text of the Harry Potter series into the field and it would save in the database correctly.
-   [IntegerField](https://docs.djangoproject.com/en/2.1/ref/models/fields/#integerfield)
    -   Holds an integer value
-   [FloatField](https://docs.djangoproject.com/en/2.1/ref/models/fields/#floatfield)
    -   Holds a float value; this is good for numbers with potentially varying numbers of decimal places
-   [DecimalField](https://docs.djangoproject.com/en/2.1/ref/models/fields/#decimalfield)
    -   This is a good field for a number with a  _fixed number of decimal places_, like currency. There are 2 required parameters:  `max_digits`  refers to the total number of digits (before and after the decimal place), and  `decimal_places`  refers to how many decimal places.
-   [BooleanField](https://docs.djangoproject.com/en/2.1/ref/models/fields/#booleanfield)
    -   Holds a boolean value
-   [DateTimeField](https://docs.djangoproject.com/en/2.1/ref/models/fields/#datetimefield)
    -   Used for a combination of a specific date and time. This field can take two very useful optional parameters. Setting the  `auto_now_add`  argument to True adds the current date/time when an object is created. Setting  `auto_now=True`  automatically updates any time the object is modified.

#### Video Overview

In this video, we'll go over the next 4 modules which explain how to make models, create a database with tables, and use the Django shell.

# Migrations

## Objectives:

-   Learn how to create a database and table(s) in SQLite based on our model(s)
-   Understand what migrations do

----------

Now that we've set up our models, it's time to create an actual database with some tables! Luckily, Django can do the whole job for us with minimal code.

To do this, (basically the equivalent of forward engineering in MySQL Workbench), we are going to run a couple of commands from the terminal.
```
  > python manage.py makemigrations
  > python manage.py migrate
```
**_makemigrations_**  is a kind of staging. When this command runs, Django looks through all our code, finds any changes we made to our models that will affect the database, and then formulates the correct Python code to move on to the next step. Note that if this step has errors, the next step will not work, so you will need to fix any errors before you can move on to migrating.

**_migrate_**  actually  _applies_  the changes made above. This step is where the SQL queries are actually built and executed.

The migration process is split into two steps so that Django can check and make sure you wrote code it can understand before moving on to the next step.

##### A Few Notes:

1.  _**Never**  delete migration files_ and  **always**  `makemigrations`  and  `migrate`  anytime you change something in your  `models.py`  files – that's what updates the actual database so it reflects what's in your models.
2.  For now we are going to be using  **SQLite,** a SQL database that comes pre-packaged with Django. It is best used in a development environment because it is stored as  _local memory_  in a file and as such is very fast. It is generally not recommended for use once our application is ready for production. Luckily, changing what kind of database we are using is quite simple. In the deployment section, we'll learn how to switch to a **MySQL**  database.
3.  Django ORM models and queries will always be the same no matter which database we are using.

# Django Shell

## Objectives:

-   Learn what the Django Shell is
-   Learn how to import models into the shell

----------

Before tying models directly into our web applications, we're going to take a minute to open the Django shell to interact with our models and practice writing queries using Django's ORM.

To use the shell, we'll run the following command in our terminal from our project's root directory (where our _manage.py_ file is located):

> python manage.py shell

Your terminal output should look like this:

<img src="https://i.ibb.co/5jG9L4K/Screen-Shot-2018-03-25-at-1-34-00-PM.png" border="0">

Once we're in the shell, we can access all of our functions and classes in our files. To do so, we just need to specify which modules (files) we need.  Since we are interested specifically in working with our models, let's import them:
```py
>>> from your_app_name_here.models import *
```
**We will need to run this import  _every time_  we start the shell.**

**_Caution_:**  Since models.py contains the classes you wrote, importing everything in models.py is okay, but generally when you're importing other libraries/modules, the Django community discourages the practice of importing all (*). A good explanation can be found here: [https://stackoverflow.com/questions/2360724/what-exactly-does-import-import](https://stackoverflow.com/questions/2360724/what-exactly-does-import-import).

## Viewing the Database

We can always use the shell to view the data in our database, but sometimes it can be frustrating to figure out how objects map to rows in a table. If you find the shell too frustrating to navigate, you can use a program called DB Browser for SQLite to view your database tables. DB Browser can be downloaded [here](https://sqlitebrowser.org/dl/).

To get your browser set up, follow the steps in this video:

#   
ORM CRUD Commands

## Objectives:

-   Learn/have a reference for basic ORM CRUD (Creating, Reading, Updating, and Deleting) commands

----------

Now that you have imported your models, let's start talking queries! This module is a little bit long--spend just a few minutes reading through to get familiar with what we're about to do. Just like we learned INSERT, SELECT, UPDATE, and DELETE statements in MySQL, we'll need methods that have the same functionality as those query commands.

Once you've spent just a few minutes reviewing CRUD in this module, jump into the Users assignment! Use this module as a guide to practice each of the queries in the shell. Remember, the best way to learn is by doing!

While SQL understands data in terms of tables and rows, in Django we'll refer to our data in terms of classes and class instances. Each row of data is an  _instance_ of the associated class. Even though a class instance is more than a dictionary, we can still think of an instance kind of like a dictionary, where our class's field names are the keys, and the actual data from our database are the values.

## Overview of Commands

-   Creating a new record

-   ClassName.objects.**create**(field1="value for field1", field2="value for field2", etc.)

-   Reading existing records

-   Methods that return a single instance of a class

-   ClassName.objects.**first**() - gets the first record in the table
-   ClassName.objects.**last**() - gets the last record in the table
-   ClassName.objects.**get**(id=1) - gets the record in the table with the specified id

-   **this method will throw an error unless  _only and exactly one record matches_  the query**

-   Methods that return a list of instances of a class

-   ClassName.objects.**all**() - gets all the records in the table
-   ClassName.objects.**filter**(field1="value for field1", etc.) - gets any records matching the query provided
-   ClassName.objects.**exclude**(field1="value for field1", etc.) - gets any records  _not_  matching the query provided

-   Updating an existing record

-   c = ClassName.objects.**get**(id=1)  
    c.field_name = "some new value for field_name"  
    c.**save**()

-   Deleting an existing record

-   c = ClassName.objects.**get**(id=1)  
    c.**delete**()

-   Other helpful methods

-   Displaying records

-   ClassName.objects.get(id=1).**__dict__**  - shows all the values of a single record as a dictionary
-   ClassName.objects.all().**values**() - shows all the values of a QuerySet (i.e. multiple instances)

-   Ordering records

-   ClassName.objects.all().**order_by**("field_name") - orders by field provided, ascending
-   ClassName.objects.all().**order_by**("**-**field_name") - orders by field provided, descending

To take a deeper dive into any of these commands, keep scrolling. For the next few assignments, we'll be running all these commands in the shell. Once we go full stack, we will utilize these queries in our  `views.py`  file. The examples below utilize this model:
```py
class Movie(models.Model):
    title = models.CharField(max_length=45)
    description = models.TextField()
    release_date = models.DateField()
    duration = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```
## CREATING

To add a new record to a table:

-   ClassName.objects.**create**(field1="value for field1", field2="value for field2", etc.)
-   SQL Equivalent: "INSERT INTO tablename (field1, field2) VALUES ('value for field1', 'value for field2');"

The  **create** method  _returns an instance of the model_  with the values that were just added. This means that if we wanted to do something with the instance after creating in our database, we could set a variable and use it like so:
```py
newly_created_movie = Movie.objects.create(title="The Princess Bride",description="the best movie ever",release_date="1987-09-25",duration=98)
print(newly_created_movie.id)	# view the new movie's id
```
Another way to add a row to our database is by creating an instance of the class (think back to the OOP section) and saving it, like so:
```py
newly_created_movie = Movie(title="The Princess Bride",description="the best movie ever",release_date="1987-09-25",duration=98)
newly_created_movie.save()
```
By default, all fields in our models are non-nullable, meaning all fields are required upon creation. If you want to change this default behavior, check out  [Django's documentation](https://docs.djangoproject.com/en/1.11/ref/models/fields)  on the null property.

## READING

There are several ways that we might want to retrieve records from the database.

### Multiple Records

There are several different methods that will return multiple records (or lists of instances).

#### All

To get all the rows from a given table:

-   ClassName.objects.**all**()
-   SQL Equivalent: "SELECT * FROM tablename;"

The  **all**  method  _returns a  **list**  (technically a QuerySet) of instances of the model._
```py
all_movies = Movie.objects.all()
```
#### Filter (WHERE)

To specify criteria for retrieving rows from a given table:

-   ClassName.objects.**filter**(field1="value to match", field2="another value", etc.)
-   SQL Equivalent: "SELECT * FROM tablename WHERE field='value to match' AND field2='another value';"

The  **filter**  method also _returns a  **list**  (technically a QuerySet) of instances of the model._
```py
some_movies = Movie.objects.filter(release_date='2018-11-16')
```
#### Exclude (WHERE NOT)

To specify criteria for filtering  _out_ records to retrieve:

-   ClassName.objects.**exclude**(field1="value to match", field2="another value", etc.)
-   SQL Equivalent: "SELECT * FROM tablename WHERE NOT (field='value to match' AND field2='another value');"

The  **exclude**  method also _returns a  **list**  (technically a QuerySet) of instances of the model._

other_movies = Movie.objects.exclude(release_date='2018-11-16')

When we have a list of instances, we can iterate through that list and view each instance and its values:
```py
for m in all_movies:    # m represents each movie instance as we iterate through the list
    print(m.title)	# that means m has all the properties of the Movie class, including title, release_date, etc.
```
### Single Records

There are also several different methods that will return a single instance of a class.

#### Get

To get a specific row from the table, specify a field and value.

-   ClassName.objects.**get**(field1="unique value")
-   SQL Equivalent: "SELECT * FROM tablename WHERE field1='unique value' LIMIT 1;"

The  **get**  method  _returns a  **single instance**  of the model._

one_movie = Movie.objects.get(id=7)

If our specified value(s) finds no matching results or more than one matching result from the database, we will get an error. This is why we should really only use fields that we know will be unique, with values that we are certain are in the database. For this reason,  `id`  is the most common field to use with  **get**.

#### First

To get the first row from the table:

-   ClassName.objects.**first**()
-   SQL Equivalent: "SELECT * FROM tablename ORDER BY id LIMIT 1;"

The  **first**  method  _returns a  **single instance**  of the model._  If no order is specified before calling the  **first**  method, the data is ordered by the primary key.
```py
first_movie = Movie.objects.first()
```
#### Last

To get the last row from the table:

-   ClassName.objects.**last**()
-   SQL Equivalent: "SELECT * FROM tablename ORDER BY id DESC LIMIT 1;"

The  **last**  method  _returns a  **single instance**  of the model._  Again, if no order is specified before calling the  **last**  method, the data is ordered by the primary key.
```py
last_movie = Movie.objects.last()
```
When we are working with a single instance, we can access any of the instance's values with dot notation. For example:
```py
print("Movie 7", one_movie.title)
print("First movie", first_movie.release_date)
print("Last movie", last_movie.description)
```
## UPDATING

In order to update an existing record, we first need to obtain the instance of the record we want to modify and then use the  **save**  method to commit those changes to the database. For example:
```py
movie_to_update = Movie.objects.get(id=42)	# let's retrieve a single movie,
movie_to_update.description = "the answer to the universe"	# update one/some of its field values
movie_to_update.title = "The Hitchhiker's Guide to the Galaxy"
movie_to_update.save()	# then make sure all changes to the existing record get saved to the database
```
The equivalent SQL statement would be:

-   "UPDATE tablename SET field1='new value', field2='new value' WHERE id=id_value;"

## DELETING

In order to delete an existing record, we again need to obtain the instance of the record and then use the  **delete**  method. For example:
```py
movie_to_delete = Movie.objects.get(id=2)	# let's retrieve a single movie,
movie_to_delete.delete()	# and then delete it
```
The equivalent SQL statement would be:

-   "DELETE FROM tablename WHERE id=2;"

## Helpful Tip

You've probably noticed in the shell that printing whole objects just results in something like  `<Movie Object (1)>`, which is not particularly helpful. To change how our models display, we can  _override_  the  `__str__`  method in the class. This is pretty handy and shows how we can leverage some of Python's magic methods to make our lives easier.
```py
class Movie(models.Model):
    # fields removed for brevity
    def __str__(self):
        return f"<Movie object: {self.title} ({self.id})>"
```
##### OPTIONAL: iPython

Also, if you would like, you could also install iPython (pip install ipython). This replaces the default shell with a prettier one (TAB indent works, line numbers, syntax highlighting, etc).


# Assignment: Users (Shell)

## Objectives:

-   Practice using the Django Shell to run ORM commands to manipulate our database

----------

Create a new project called  _single_model_orm_  with an app called  _users_app_. Using the following ERD, complete the tasks listed below:

<img src="https://i.ibb.co/Y0JgfK2/chapter2240-1990-users.png"  border="0">

-  [ ] Create a model called User following the ERD above
    
- [ ]  Create and run the migration files to create the User table in your database
    
- [ ] Create a .txt file where you'll save each of the queries you'll run in the shell
    
-  [ ] Run the shell and import your User model
    
- [ ]  Query: Create 3 new users
    
- [ ]  Query: Retrieve all the users
    
- [ ]  Query: Retrieve the last user
    
- [ ]  Query: Retrieve the first user
    
- [ ]  Query: Change the user with id=3 so their last name is Pancakes.
    
- [ ]  Query: Delete the user with id=2 from the database
    
- [ ]  Query: Get all the users, sorted by their first name
    
- [ ] BONUS Query: Get all the users, sorted by their first name in descending order
    
- [ ]  Submit your .txt file that contains all the queries you ran in the shell

# ORM Basics Quiz 

  
1. What does Django's ORM do for us?

- [ ]  sanitizes user input
- [ ]  creates a database schema and tables based on our models
- [ ]  contains methods that perform SQL
- [x]  all of the above

2. Which of the following would correctly add a computer to our database? (Given the class has the following attributes: brand (CharField), name (CharField), and price (DecimalField))

- [x]  Computer.objects.create(brand="Lenovo", name="Yoga", price=1099.99)
- [ ]  Computer.objects.new(brand="Lenovo", name="Yoga", price=1099.99)
- [ ]  Computer.objects.create(brand="Lenovo", name="Yoga", price="1099.99")

3. Given: computers = Computer.objects.get(id=10), what is computers?

- [ ]  a list of Computers instances that have an id of 10
- [ ]  the id of the matching Computer
- [x]  an instance of the Computer with an id of 10
- [ ]  a list containing the single Computer instance with an id of 10

4. When would Computer.objects.get(name="MacBook") throw an error?

- [ ] If there are no computers in the database with the name "MacBook"
- [ ]  If there is exactly one computer in the database with the name "MacBook"
- [ ]  If there are multiple computers in the database with the name "MacBook"
- [x]  a and c

5. Given: computers = Computer.objects.exclude(brand="HP"), what is computers?

- [ ]  A list of Computer instances, but without their brand
- [x]  A list of all the Computer instances except for the ones whose brand is HP
- [ ]  A list of all the Computer instances whose brand is HP
- [ ]  The string values of all the attributes of computers, except for brand

6. Which of the following methods are important for updating an instance in the database?

- [x]  get and save
- [ ]  get and update
- [ ] filter and save
- [ ]  filter and update

# Putting Everything Together

## Objectives:

-   Understand how models fit in the whole MTV (MVC) architecture

----------

All the queries you have been running in the shell will now be in your controller (i.e. views.py file), where appropriate.

To make sure our controller knows about our models, we just need an import statement at the top. Then we can utilize the methods we have learned where needed. Using our Movie class, for example:

#### my_app/views.py
```py
# other imports
from .models import Movie
# show all of the data from a table
def index(request):
    context = {
    	"all_the_movies": Movie.objects.all()
    }
    return render(request, "index.html", context)
```

#### my_app/templates/index.html
```html
<h1>All Movies</h1>
<ul>
{% for movie in all_the_movies %}
    <li>{{ movie.title }}</li>
{% endfor %}
</ul>
```


### Video Overview

# Assignment: Users with Templates

## Objectives:

-   Practice incorporating models into the whole MTV (MVC) architecture

----------

The shell practice in the previous assignment allowed us to focus just on the Model portion of the MTV architecture. But while the shell is very useful, it can be difficult to visualize the data being saved and retrieved and can be tedious adding data in manually. Let's add Templates and Views back into the mix!

Working with the same Users project and app from the previous assignment, add a route that renders a template that looks something like this:

<img src="https://i.ibb.co/pbvj4Rp/CR-Users-Django.png" border="0">

- [ ]  Add a template to your app
    
- [ ]  Add a route that renders this template and have it display a table with all the data from the database
    
- [ ]  Add a form to the page
    
- [ ]  Add a route that processes the form information, adds it to the database, and then redirects to display the template

# Altering Models After Creation

## Objectives:

-   Know how to handle changing a model after initial creation

----------

Whenever we need to make changes to our models after the initial migration (i.e. add fields, remove fields, or alter properties of existing fields), we will need to re-run the  `makemigrations`  and  `migrate`  commands. Say, for example, you created a table, but then realized later you wanted to add another field. If you find yourself seeing an error like this, come back to this module!

![](https://s3.amazonaws.com/General_V88/boomyeah2015/codingdojo/curriculum/content/chapter/Error_non-nullable_field.PNG)

This error is telling us that we are trying to add a field that isn't allowed to be null, but any existing data will obviously not have values for that field. (Even if you haven't actually added any data, you'll still get this error.) To make sure our existing data maintains integrity, we need to provide a value for this new field for any existing rows of data. Django gives you two options. Option 1 allows us to specify a value right here in the shell. Option 2 allows us to quit attempting to make migrations and update our models to add an argument to specify a default.

#### Option 1

This is the quickest, simplest option. Type 1 and hit enter. You'll then see a prompt that asks what value you would like:

<img src="https://i.ibb.co/bWdGFJ4/model-update-1.png" border="0">

The value you provide should be compatible with the field type: type the value next to the  `>>>`  and hit enter. For example, if it's a CharField, you should provide a string (eg. "no value" or ""). For an IntegerField, provide a number value (eg. 0).  **Hint: for a DateField or DateTimeField, read the message above the  `>>>`  prompt!**

The only exception is for a ForeignKeyField--the command line tool doesn't really allow for complex imports and retrievals, so you can actually specify a value for that field's primary key. In our case, that will be an integer.

Once done, don't forget to run  `migrate`!

#### Option 2

If you know you want to provide a default value for any existing and potentially future entries for this new field in your table, type 2 and hit enter. In your model, revise the new field by adding a default argument and value. You might also consider setting the field to be nullable, if that field is optional. For example:
```py
age = models.IntegerField(default=200)	# if no age is entered for a new/existing, age will be set to 200
age = models.IntegerField(null=True)	# if no age is provided, the field will remain empty
```
#### Video Overview

#### Option 3 - Everything's broken, I have no options left

If you have tried everything and hit a brick wall with your database, or corrupted your data beyond repair, as a last-ditch effort you can delete your database and start over from scratch. To do this, you will need to delete the following files/directories:

-   db.sqlite3
-   your_app_name/migrations
-   your_app_name/__pycache__

After you delete these, you will need to re-run your makemigrations and migrate commands. When you make your migrations, you will need to include the app name:
```
python manage.py makemigrations your_app_name
python manage.py migrate
```
**IMPORTANT:** There is a reason that this is so difficult to do! Databases should as a rule never be deleted after creation, as this interferes with the reliability of your trusted data source. We typically want to store any changes ever made to a database so that we can audit it at any time, so this should only be used in an emergency. For more information on why you shouldn't delete data, check out this [link.](https://www.infoq.com/news/2009/09/Do-Not-Delete-Data/)

# One to Many Relationships

## Objectives:

-   Understand how to establish one-to-many relationships between models
-   Learn how to create instances when models have a foreign key
-   Learn how to read an instance with its associated relationship data

----------

To indicate a one-to-many relationship between models, Django uses a special field,  `ForeignKey`. Consider these models, where one author can write many books and one book can be written by only one author:

<img src="https://i.ibb.co/0VpQB3H/books-authors.png" border="0">

```py
class Author(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name="books", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

Notice that rather than having a simple integer field as our foreign key, the  `Book`  model has this line:  `models.ForeignKey(Author, related_name="books", on_delete = models.CASCADE)`. While the CRUD operations are fundamentally the same, let's take a look at how we create and read when we have a relationship between two models.

#### CREATING

Remember that by default, all fields are required. The created_at and updated_at fields will be populated automatically, but the other two fields must be set upon creation. Since title is a CharField, we can pass it a string; but the author field is expecting an instance of the Author class. So to create a record that has this foreign key relationship, we first need to have an instance of an Author, and then we can pass it like we have any other field:
```py
this_author = Author.objects.get(id=2)	# get an instance of an Author
my_book = Book.objects.create(title="Little Women", author=this_author)	# set the retrieved author as the author of a new book
    
# or in one line...
my_book = Book.objects.create(title="Little Women", author=Author.objects.get(id=2))
```
#### READING

Now say we are trying to view books with their associated authors.  **Joins in Django happen automatically**. If you have a book object, you don't need to run any additional query to get information about the author. If we retrieve an instance of a book:
```py
some_book = Book.objects.get(id=5)
```
Just like we are able to view the book's title, we can also view the book's author:
```py
some_book.title		# returns a string that is the title of the book
some_book.author	# returns the Author instance associated with this book
```
Because  `some_book.author`  is an instance of the Author class, we can now access the author's fields, like so:
```py
some_book.author.name		# return the name of the author of this book
some_book.author.id		# returns the id of the author of this book
```
**Just as we are able to filter by other fields, we can also search based off of a  `ForeignKey`  relationship.**  This code will find all of the books by the author with ID 2:
```py
this_author = Author.objects.get(id=2)
books = Book.objects.filter(author=this_author)
    
# one-line version:
books = Book.objects.filter(author=Author.objects.get(id=2))
```
#### Video Overview

# Reverse Lookup with related_name

## Objectives:

-   Understand the related_name argument
-   Understand how to query on the relationships from either model
-   Learn how to display a list of items on a template

----------

You may have noticed that we haven't mentioned the  `related_name`  field yet. This is used for a  **reverse look-up**. When we create a relationship in a Django model, Django places a field in the corresponding table, which we can access by the related_name we provide. This means that when we added the author field in our Book class, Django has also placed a field in the Author class that holds information about all of a given author's books. To keep track of this, it may help to add that field in as a comment so that you remember how to access it, as shown below.

**Note** the author field in the  `Book`  class is missing the required  `on_delete=models.CASCADE`  attribute

<img src="https://i.ibb.co/JqRxxhg/1to-Mrelationship.gif" border="0">

Because the Author class has a  `books`  field, we can access the books of a given author like so:  `some_author.books.all()`! (You need to say  `.all`  because there could potentially be many books connected to this author, not just one.) This can be especially convenient on a template (we aren't using templates quite yet, but this is a preview!):

#### book_project/apps/books/views.py
```py
def index(request):
    context = {"authors": Author.objects.all()}		# we're only sending up all the authors
    return render(request, "index.html", context)
```
#### book_project/apps/books/templates/index.html
```html
<h1>Author List</h1>
<ul>
  {% for author in authors %}
    <li>{{author.name}}
      <ul>
    	<!-- looping through each author's books! -->
        {% for book in author.books.all %}	
          <li><em>{{book.title}}</em></li>
        {% endfor %}
      </ul>
    </li>
  {% endfor %}
</ul>
```
<img src="https://i.ibb.co/X2jpmLd/author-list.png" border="0">

**Note:**  We do not include the parentheses when calling  _all_  on the template.

Even though we haven't talked about many-to-many relationships quite yet, the way related_name works will be the same in those relationships.

# Assignment: Dojo & Ninjas (Shell)

## Objectives:

-   Practice using the Django Shell to run ORM commands to manipulate our database
-   Practice one-to-many relationships

----------

Create a new project called  _dojo_ninjas_proj_  and an app called  _dojo_ninjas_app_. For this project, use the following diagram as a guide for creating your models:

<img src="https://i.ibb.co/7twB2V5/chapter2240-1991-dojo-erd.png"  border="0">

- [ ]  Create the Dojo class model
    
- [ ]  Create the Ninja class model
    
- [ ]  Create and run the migration files to create the tables in your database
    
- [ ]  Create a .txt file where you'll save each of your queries from below
    
- [ ]  Run the shell and import your models
    
- [ ]  Query: Create 3 new dojos
    
- [ ]  Query: Delete the 3 dojos you just created
    
- [ ]  Query: Create 3 more dojos
    
- [ ]  Query: Create 3 ninjas that belong to the first dojo
    
- [ ]  Query: Create 3 ninjas that belong to the second dojo
    
- [ ]  Query: Create 3 ninjas that belong to the third dojo
    
- [ ]  Query: Retrieve all the ninjas from the first dojo
    
- [ ]  Query: Retrieve all the ninjas from the last dojo
    
- [ ]  Query: Retrieve the last ninja's dojo
    
- [ ]  Add a new text field called "desc" to your Dojo class
    
- [ ]  Create and run the migration files to update the table in your database. If needed, provide a default value of "old dojo"
    
- [ ]  Query: Create a new dojo
    
- [ ]  Submit your .txt file that contains all the queries you ran in the shell

# Assignment: Dojos & Ninjas with Template

## Objectives:

-   Practice incorporating a one-to-many relationship in a full-stack application

----------

Using the same project from the previous assignment, add a template and the necessary routes to perform these actions:

<img src="https://i.ibb.co/p0D68np/Dojos-Ninjas-Django.png" border="0">

- [ ] Add a template to your app
    
- [ ]  Add a route that renders this template and have it display a list of all the dojos and their associated ninjas
    
- [ ] Add a route to process the creation of a new dojo
    
- [ ]  Add a route to process the creation of a new ninja; the dropdown on the form should be a list of all existing dojos
    
- [ ]  NINJA BONUS: Add a delete button next to each dojo name that deletes that dojo (and all associated ninjas) from the database
    
- [ ]  SENSEI BONUS: Add a count of ninjas next to each dojo name (eg. Ninjas at the Painting Dojo - 2; Ninjas at the Architecture Dojo - 0)

# Many to Many Relationships

## Objectives:

-   Understand how to establish many-to-many relationships between models
-   Learn how to create an instance of a many-to-many relationship
-   Learn how to read an instance with its associated relationship data

----------

You may remember that in order to use a many-to-many relationship in SQL, you had to construct a third table that contained foreign key relationships to the two tables you wanted to connect.  **Django will do this for you automatically**  if your model includes a  `ManyToManyField`. We'll use these models as an example, where each publisher can publish many books, and each book can be published by many publishers:

<img src="https://i.ibb.co/LdJ2M3t/bookspublishers.png" border="0">

```py
class Book(models.Model):
	title = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
class Publisher(models.Model):
	name = models.CharField(max_length=255)
	books = models.ManyToManyField(Book, related_name="publishers")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
```
Unlike with a  `ForeignKey`,  **it doesn't matter which model has the  `ManyToManyField`**. The model would still work if the Book model has a field named publishers instead (though we would need to put the Publisher class first).

Adding a relationship between two existing records is simple:
```py
this_book = Book.objects.get(id=4)	# retrieve an instance of a book
this_publisher = Publisher.objects.get(id=2)	# retrieve an instance of a publisher
    
# 2 options that do the same thing:
this_publisher.books.add(this_book)		# add the book to this publisher's list of books
# OR
this_book.publishers.add(this_publisher)	# add the publisher to this book's list of publishers
```
And to remove a relationship between two existing records:
```py
this_book = Book.objects.get(id=4)	# retrieve an instance of a book
this_publisher = Publisher.objects.get(id=2)	# retrieve an instance of a publisher
    
# 2 options that do the same thing:
this_publisher.books.remove(this_book)		# remove the book from this publisher's list of books
# OR
this_book.publishers.remove(this_publisher)	# remove the publisher from this book's list of publishers
```
The two methods for adding shown above are equivalent because a  **ManyToManyField is automatically symmetrical**. That is, by adding a book to a publisher, Django will also automatically add the publisher to the book. This means that we can add or look up from the other end without issue.

The syntax to see all books from a given publisher is the same as when doing a reverse look-up on a  `ForeignKey`  relationship:
```py
this_publisher.books.all()	# get all the books this publisher is publishing
this_book.publishers.all()	# get all the publishers for this book
```
Remember to leave off the parentheses when referring to this collection in your template:  `this_publisher.books.all`.

#### Video Overview

# Assignment: Books/Authors (Shell)

## Objectives:

-   Practice using the Django Shell to run ORM commands to manipulate our database
-   Practice many-to-many relationships

----------

Create a new project called  _books_authors_proj_  and an app called  _books_authors_app_. Use the following diagram as a guide for designing your models:

<img src="https://i.ibb.co/ZBqMP6C/books-authors-ERD.png" border="0">

- [ ]  Create the Book class model
    
- [ ]  Create the Author class model
    
- [ ]  Create and run the migration files to create the tables in your database
    
- [ ]  Create a .txt file where you'll save each of your queries from below
    
- [ ]  Query: Create 5 books with the following names: C Sharp, Java, Python, PHP, Ruby
    
- [ ]  Query: Create 5 different authors: Jane Austen, Emily Dickinson, Fyodor Dostoevsky, William Shakespeare, Lau Tzu
    
- [ ]  Add a new text field in the authors table called 'notes'.
    
- [ ]  Create and run the migration files to update the table in your database.
    
- [ ]  Query: Change the name of the C Sharp book to C#
    
- [ ] Query: Change the first name of the 4th author to Bill
    
- [ ]  Query: Assign the first author to the first 2 books
    
- [ ]  Query: Assign the second author to the first 3 books
    
- [ ]  Query: Assign the third author to the first 4 books
    
- [ ]  Query: Assign the fourth author to the first 5 books (or in other words, all the books)
    
- [ ]  Query: Retrieve all the authors for the 3rd book
    
- [ ]  Query: Remove the first author of the 3rd book
    
- [ ]  Query: Add the 5th author as one of the authors of the 2nd book
    
- [ ]  Query: Find all the books that the 3rd author is part of
    
- [ ]  Query: Find all the authors that contributed to the 5th book
    
- [ ]  Submit your .txt file that contains all the queries you ran in the shell

# Assignment: Books/Authors with Templates

## Objectives:

-   Practice incorporating a many-to-many relationship in a full-stack application

----------

Using the same project from the previous assignment, create an application that does the following:

<img src="https://i.ibb.co/h1bKBR9/Books-Authors-Django.png" border="0">

- [ ]  Add a template for creating books that also displays a table of all books in the database
    
- [ ]  Complete the route for adding a book to the database
    
- [ ]  Add a template that displays a specific book and its details, including all the authors associated with the given book
    
- [ ]  Create a form on the specific book template that has a dropdown of all the authors in the database. The "Add" button should add the selected author to the given book.
    
- [ ]  Add a template for creating authors that also displays a table of all authors in the database
    
- [ ]  Complete the route for adding an author to the database
    
- [ ]  Add a template that displays a specific author and its details, including all the books associated with the given author
    
- [ ]  Create a form on the specific author template that has a dropdown of all the books in the database. The "Add" button should add the selected book to the given author.
    
- [ ]  SENSEI BONUS: Have the dropdown menus only include authors or books not yet associated with the given book or author, respectively

# Advanced Queries (optional)

This is a great opportunity to delve into some  [documentation](https://docs.djangoproject.com/en/2.2/ref/models/querysets/). We have learned the basics for querying, but there are a lot more ways to query with Django's ORM. Reading through the documentation might be overwhelming the first time. As a tip, I recommend reading about a concept you already understand; this helps you get familiar with the vocabulary and format of a given set of documentation.

For example, if we start with the  [_exclude_  section](https://docs.djangoproject.com/en/2.1/ref/models/querysets/#exclude), hopefully you find much of their description familiar. Then we reach this code snippet:
```py
Entry.objects.exclude(pub_date__gt=datetime.date(2005, 1, 3), headline='Hello')
```
From this, we can assume their Entry class has attributes named  _pub_date_  and  _headline_. Then we see this  `__gt`  and aren't sure what this means. Search the docs for a minute to see if you can figure it out. Hopefully you found  [this section](https://docs.djangoproject.com/en/2.1/ref/models/querysets/#gt), which explains that  `__gt`  means  _greater than_. Neat!

This example shows us the syntax for some of the more advanced queries we can run. By starting with an attribute, we can drill into that attribute with a variety of different  [field lookups](https://docs.djangoproject.com/en/2.1/ref/models/querysets/#field-lookups). The syntax, as we have seen, is to use the double underscore and then the lookup keyword. For example, with our own Book model, we can filter on the title name:
```py
lil_books = Book.objects.filter(title__startswith="Little")
```
We can also search by a field in the  _related object(s)_  by using a double underscore, and even apply lookups on fields within  _that_  object:
```py
books = Book.objects.filter(author__name="Louise May Alcott")
books = Book.objects.filter(author__name__contains="Al")
```

# Assignment: Sports ORM I

## Objectives:

-   Practice using more advanced queries

----------

Using the sports_orm, complete all the following queries and show their results on index.html.

The purpose of this assignment is to practice using the Django ORM to make queries on a pre-existing database. You MUST install the sports_orm before you can complete this assignment. In your Django folder, run this terminal command:  `git clone https://github.com/TheCodingDojo/sports_orm.git`  This will create a folder named  `sports_orm`; if you  `cd`  into this new folder,  `python mangage.py migrate`  and  `python manage.py runserver`, you should see lists of sports leagues, teams, and players. Your goal for this assignment is to modify  `leagues/views.py`  and/or  `leagues/templates/leagues/index.html`  so that instead the page shows:

1.  ...all baseball leagues
2.  ...all womens' leagues
3.  ...all leagues where sport is any type of hockey
4.  ...all leagues where sport is something OTHER THAN football
5.  ...all leagues that call themselves "conferences"
6.  ...all leagues in the Atlantic region
7.  ...all teams based in Dallas
8.  ...all teams named the Raptors
9.  ...all teams whose location includes "City"
10.  ...all teams whose names begin with "T"
11.  ...all teams, ordered alphabetically by location
12.  ...all teams, ordered by team name in reverse alphabetical order
13.  ...every player with last name "Cooper"
14.  ...every player with first name "Joshua"
15.  ...every player with last name "Cooper" EXCEPT those with "Joshua" as the first name
16.  ...all players with first name "Alexander" OR first name "Wyatt"

Hint: Try editing the context dictionary for these queries!
```py
context = {
	# commenting out the "leagues" key so they don't conflict
	# "leagues": League.objects.all(),
	"teams": Team.objects.all(),
	"players": Player.objects.all(),
	# query 1: All baseball leagues
	"leagues": League.objects.something(something=something),
}
```

## Assignment: Sports ORM II

Complete the following queries using the sports_orm and display the results on index.html.

This is the second part of the Sports ORM assignment. Note that, in the models, every player has exactly one .curr_team, and every team has exactly one .league. Modify apps/leagues/views.py and/or apps/leagues/templates/leagues/index.html so that when you start the server, the index page shows:

1.  ...all teams in the Atlantic Soccer Conference
2.  ...all (current) players on the Boston Penguins
3.  ...all (current) players in the International Collegiate Baseball Conference
4.  ...all (current) players in the American Conference of Amateur Football with last name "Lopez"
5.  ...all football players
6.  ...all teams with a (current) player named "Sophia"
7.  ...all leagues with a (current) player named "Sophia"
8.  ...everyone with the last name "Flores" who DOESN'T (currently) play for the Washington Roughriders
9.  ...all teams, past and present, that Samuel Evans has played with
10.  ...all players, past and present, with the Manitoba Tiger-Cats
11.  ...all players who were formerly (but aren't currently) with the Wichita Vikings
12.  ...every team that Jacob Gray played for before he joined the Oregon Colts
13.  ...everyone named "Joshua" who has ever played in the Atlantic Federation of Amateur Baseball Players
14.  ...all teams that have had 12 or more players, past and present. (HINT: Look up the Django annotate function.)
15.  ...all players and count of teams played for, sorted by the number of teams they've played for
  
