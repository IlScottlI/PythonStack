# Why MySQL and Database Design?

In this day and age, you've probably created dozens of different accounts for different websites and services, all with their own login information. You've probably written messages in forums, 'liked' posts, or even uploaded and shared images, videos, or audio with other people across the internet. One thing in common across all these different websites is that you're always  **creating, manipulating, and saving data.**

Besides the HTML and CSS that make up the  **view**  of a particular page, and the backend  **logic**  that dictates the functionality, there's also the  **database**, which is in charge of your data! Databases are merely collections of organized information that can easily be accessed, managed, and updated. As a full-stack developer, you need to be familiar with building your database and designing the rules by which it stores data!

_One of the most important things about database design is organizing your data to minimize repetition._  Your database is the backbone of your application, and it is very important to understand how to properly organize it to maximize efficiency and minimize data queries. In this chapter, we will explore how to create  **relational**  **database models** and explore the different ways in which you can relate data using them.

## Why ERD First?

ERD is short for 'Entity Relationship Diagram'. That's just a fancy way of saying that ERDs are essentially  _visual blueprints_  for how your database looks and behaves. ERDs and SQL work together very intimately. An ERD is a map of the  structure of how we want to store our data, and SQL is the language we use to manipulate the data as per the relationships we defined in our ERD. Learning database design first will help us visualize how our relational databases look, making it much easier to pick up the actual SQL syntax.

## Why ERD?

ERD is a process of laying out your tables and establishing relationships between them, making your data relational. Just about any data imaginable can be stored in a relational manner, there really isn't anything you can't do using a relational database like MySQL. Later, you will learn non-relational databases where everything is stored in a single table. There are pros and cons for both, but we find it's much easier to go from a relational database to a non-relational database.

## Objectives

-   Understand how to create an ERD
-   Understand how to approach modeling data to best fit the web application you are building
-   Understand proper normalization techniques

# Overview

## Main Topics for Database Design

There are many different terms and concepts that you will learn throughout this chapter, but they all point to one very simple concept:  **Don't Repeat Data.**  If you can remember this one concept, the rest is just getting yourself familiar with the terminology.

1.  **Database Relationships**
    -   One to One
    -   One to Many
    -   Many to Many
2.  **Three (3) Forms of Normalization**
3.  **MySQL Workbench**
4.  **Data Types**

## What's the Point?

When we normalize our tables, we don't repeat data. This means that in the long run, we can use our storage space more efficiently.

There's also another advantage we get by normalizing our tables and establishing relationships between them. We will learn later that the  _ids_ and the _foreign keys_  serve as the glue between our tables. Using SQL, we can manipulate our tables and create the customized table that we need for the job at hand.

By breaking out our data into different tables, we make each table be good at one thing: storing instances, or rows, of that data. Also if we separate our tables, our database becomes more modular.  **This means that we can create our own customized tables depending on the task at hand using SQL.**

We will learn this in the next chapter but it is crucial to understand that we are using the strategy of normalizing our tables and setting relationships between them because we want to save storage space; and also because it makes our database more modular so that we can create more variety of customized tables using SQL.


# One to One Relationships

Consider the following table  _**customers:**_

<img src="https://i.ibb.co/X2t8D0k/chapter2161-1521-Screen-Shot-2013-10-04-at-12-26-01-PM.png" border="0">

Although each customer can only have one address, it would seem more fitting and better organized if we separate out the address and put it in its own table. We can then keep better track of specific information about a given address without the fear of our table getting too large to manage.

<img src="https://i.ibb.co/JdxM57d/chapter2161-1522-Screen-Shot-2013-10-04-at-1-33-06-PM.png" border="0">

Don't worry, we'll continue to explore  _foreign keys_  throughout this chapter!

<img src="https://i.ibb.co/gD9yq2J/chapter2161-1523-Screen-Shot-2013-10-04-at-12-27-10-PM.png" border="0">

Since each address that we have can only belong to a single customer and each customer can only have one address, we call this a  **One to One Relationship**.

We can visualize the relationship between the customer and address records like this:

<img src="https://i.ibb.co/rffT383/graph-1.png" border="0">

Note that the existence of a relationship can be optional, like having a customer record that has no related address record.

## What Can We Do with SQL

Even though we split up our tables into two different tables, we can combine them into one using SQL. No need to know how to do this yet, but it is important to see how a table can be joined as long as there is a  _foreign key_  that references another table's id. We'll cover actual SQL syntax in the next chapter.

<img src="https://i.ibb.co/9y9Mwf0/0Bw6pb7.gif" border="0">

## Examples of One-to-One

The easiest way to check to see if your relationship makes sense for your data is to simply talk through the relationship out loud. Remember that relationships go in two directions. For example, one address has only one ZIP code, but one ZIP code can have many addresses, thus making it a different type of relationship. Check out some of the sample One-to-One relationships below:

-   **Customers and Credit Cards** - Every Customer has one Credit Card, every Credit Card belongs to one Customer.
-   **User and Email**  - Every User has one Email Address, every Email Address has one User.
-   **Product and Image**  - Every Product has an Image, every Image is of a Product.

# One to Many and Many to One Relationships

Continuing from our previous example of  **_customers_**  and  **addresses** tables where **one customer**  can only have  **one address**...

<img src="https://i.ibb.co/kJXwZqs/chapter2161-1524-Screen-Shot-2013-10-04-at-1-38-16-PM.png" border="0">

We now want our customers to be able to order items from us. To add our **_orders_**  table, it will require us to define a different relationship. Each customer is able to have  **multiple orders**, but each order can only belong to  **one customer**

<img src="https://i.ibb.co/34HLM9j/chapter2161-1525-Screen-Shot-2013-10-04-at-1-38-53-PM.png" border="0">

Since one customer can have many orders for any given user we call this a  **One to Many**  Relationship.

<img src="https://i.ibb.co/kxLh80m/graph-2.png" border="0">

## What Can We Do with SQL

Notice how the _foreign key_ and the  _id_ of the table that we want to combine act as the glue. We can join different tables using SQL. Once again, we will learn how to do this later on but it is important to know that we are setting up these relationships so that we can create customized tables like the illustration below by using SQL to join different tables on the  _foreign key_  and the _primary id_.

![](http://i.imgur.com/SdHYDDl.gif)

## Examples

One-to-Many is probably the most common relationship you'll encounter while making web applications. Often times a One-to-One relationship is actually much more similar to a One-to-Many. Below are a few examples:

-   **Messages and Comments**  - One Comment belongs to one Message, but one Message can have many Comments.
-   **States and Cities**  - One City is only in one State, but one State can have many Cities.
-   **Customers and Orders**  - One Order only has one Customer, but one Customer can have many Orders.

# Many to Many Relationships

We have a table that keeps track of each of the orders the customer placed but we haven't created a way to keep track of the items they are ordering.

<img src="https://i.ibb.co/cgyfyqt/chapter2161-1526-Screen-Shot-2013-10-07-at-3-39-23-PM.png"  border="0">

Here we created an  **_items_**  table to hold the name and description of each item that the customer can order.

<img src="https://i.ibb.co/GnmzRkQ/chapter2161-1527-Screen-Shot-2013-10-07-at-4-21-19-PM.png" border="0">

Since each order can have many different items and those same items can show up in many different orders, we have to use a different type of relationship to connect orders to items.  **Orders**  can have many  **items**  and  **items**  can have many  **orders**, so we call this a  **Many to Many** Relationship.

In a  **Many to Many**  relationship, we create a  _connector table_  that has both the _order_id_ and the  _item_id_  so that we can determine all the items in a particular order.

<img src="https://i.ibb.co/tHJgKBP/chapter2161-1528-Screen-Shot-2013-10-07-at-4-26-47-PM.png" border="0">

Here is how we can visualize this kind of relationship:

<img src="https://i.ibb.co/pyLQLhX/graph-3.png" border="0">

If you want to include the  **_items_orders_** records in the graph, it may look like this:

<img src="https://i.ibb.co/Z8sY1wT/graph-4.png" border="0">

## What Can We Do with SQL

![](http://i.imgur.com/zu3hsWo.gif)

## Examples

Many-to-Many is often the most confusing type of relationship for lots of people, but if you make sure to talk-out the relationship out loud, you'll quickly find if it works or not. Remember,  **anytime you have a Many-to-Many, it will require some sort of joining table!** Check out the below examples and use how we describe the relationship as a guide:

-   **Users and Interests** - One User can have many Interests, one Interest can be applied to many Users.
-   **Actors and Movies**  - One Movie can have many Actors, one Actor can be in many Movies.
-   **Businesses and Cities**  - One Business can be spread across many Cities, one City can be home to many Businesses.


# Normalization

### **What is Normalization?**

_Database normalization_  is simply a convention for splitting large tables of data into smaller separate tables with the primary goal being to **not repeat data.** Why is this so important? Let's say that you wear a watch so you can check the time, because it's very important for you to know what the current time is. Would wearing eight watches make it easier? No way! Now we have eight conflicting accounts of what the proper time is. Worse yet, if we ever want to update the time, we'd have to do it for every watch independently. That's not very efficient!

You can apply a similar concept to database design. If we want to store a user's email address, we'd want to store it in only one place. Then, if we ever need to refer to it again, we'd simply use the  **id**. The id will never change, so even if we update the user's email address, none of the other connections we defined in our database will be damaged. Neat!

Below are the three main rules of database normalization. You should use these as a  _guide_  for designing your ERDs. Always remember, however, that they are common convention, and not absolute rules. **It is possible to take normalization to an extreme.**  For example, a simple address field. One state can have many cities, one city can have many streets, one street can have many buildings, one building can have many apartments, one apartment can have many residents... and so on. Yikes, that can get really crazy really quick! In the next sections, you'll learn more about why this type of complexity can be inefficient, especially for simple assignments.

### First Form

****Each Column in your table can only have 1 value.****

Ex. You should not have an  **address**  column in your table that lists the address, city, state, and zip, all separated by commas.

### **Second Form**

**Each Column in your table that is not a  _key (primary or foreign)_  must have unique values.**

Ex. If you have a  **movies**  table with a  **categories**  column, you should not have a category repeated more than once.

### **Third Form**

**You cannot have a non-key column that is dependent on another non-key column.**

Ex. If you have a  **books**  table with columns  **publisher_name** and  **publisher_address,** the publisher_address and publisher_name should be separated into a separate table and linked to books with a foreign key. The publisher_address is dependent on the publisher_name and neither column is a key column.

# Quiz
  
1. A real world parallel of a primary key would be which one of the following:

- [x]  Social Security Number
- [ ]  Birthday
- [ ]  Street Address
- [ ]  Last Name

2. Which of the following relationships requires a foreign key?

- [ ]  Many to Many
- [ ]  One to One
- [ ]  One to Many
- [x]  All of the Above

3. Which of the following is the best example of a many to many relationship

- [ ]  users have many photos and photos have many users
- [x]  users have many interests and interests have many users
- [ ]  blogs have many posts and posts have many blogs
- [ ]  messages have many comments and comments have many messages

4. Which of the following violates the first form of normalization

- [ ]  Having a column in your products table called assembly which contains the information for how to assemble the product.
- [ ]  Removing the type column from your products table and adding a relationship of '**products  _has-many_  types**'
- [x]  Having a column in your products table with a comma-separated list of all the different categories that the product belongs to
- [ ]  Separating out price from the products table to create a prices table with a relationship of '**products  _has-one_  price**'

5. In a One to One relationship the joining tables are related by having a foreign key in both tables

- [ ]  True
- [x]  False

6. In the relationship of '**states  _has-many_  cities**', the foreign key that joins the tables together goes in the states table.

- [ ]  True
- [x]  False

7. To pass the second form of normalization, you should find any non-key columns that have repeated values and separate them out into another table and create the proper relationship.

- [x]  True
- [ ]  False

8. Which of the following violates the third form of normalization?

- [x]  A users table with profile_pic_name and profile_pic_url columns
- [ ] A pictures table with url and name columns
- [ ]  A many to many relationship without a joining table
- [ ]  Having an interests column in your students table that lists out each students different interests

9. What is the most important thing to remember about database design?

- [ ]  Creating the proper relationships between tables so that our data stays organized
- [x]  Making sure we don't repeat data
- [ ]  Making sure each table created has a unique identifier
- [ ]  Making sure to name your tables all lowercase and plural

10. What is the main purpose for Normalization?

- [ ]  Separating your data into as many tables as possible
- [x]  Creating a convention for organizing and avoiding the duplication of data
- [ ]  Having a cool name to explain an obvious process
- [ ]  Only to make sure that you don't repeat data and no other reasons

## What is MySQL Workbench?

MySQL Workbench is just a Graphical User Interface (GUI) for us to interact with MySQL, one of the most popular relational databases in the world - through SQL commands.

## Why MySQL Workbench?

We use MySQL Workbench when we are interacting with our databases because it will help us run some SQL queries. It also has a great interface where we can map out our tables and establish relationships between them.

## Install MySQL Workbench

Install the latest stable version found at [http://dev.mysql.com/downloads/workbench/#downloads](http://dev.mysql.com/downloads/workbench/#downloads)


# Conventions

We will be following a set of conventions to create our database. We don't have to follow these conventions, but we recommend our students to follow them for the following reasons:

1.  Developers can have a better understanding of your database if you are using a set of industry standards.
2.  Developers can create software to automate a lot of the queries if some assumptions can be made. In later chapters, you will learn about Object Relational Mappers (ORM), which are programs that other developers use to make database queries easier by providing some handy functions. These functions will only work if we have followed conventions that ORM author expects, which are primarily based on set industry standards.

## Guidelines

Down the line, you may find yourself working with a company that has set up their database conventions a little bit differently, but these are the guidelines that we feel are best for this course:

1.  **make the table name plural and ALL lowercase** - make it plural (ex. users, leads, sites, clients, chapters, courses, modules)
2.  **use "id" as the primary key** - name it  _id_ (also make it auto-incremented).
3.  **name foreign keys with singular_table_name_id** when referencing to a primary key in another table name it [_singular name of the table you're referring to]_id_  (ex. user_id, lead_id, site_id, client_id, chapter_id, course_id, module_id).
4.  **use  _created_at_  and _updated_at_** as columns for the timestamp in EVERY table you create.

When we do things in ORM or in Ruby on Rails, it becomes extremely important that we follow these naming conventions.

# Data Types

The following are the data types that you will be using 95% of the time. Although there are quite a few other data types that you can use, focus on these for now.

## **Simple Data Types:**

-   **VARCHAR(_number of characters_)**
    -   Used to store non-numeric values that can be up to 255 characters. It is called a VARCHAR because it can store a variable number of characters and will only use the space required for each record that is stored in the database. VARCHAR should be used for values with different character lengths like an email, first_name, or last_name.
-   **CHAR(_number of characters_)**
    -   Also used to store non-numeric values, however, it will use up all space for the set number of characters regardless of what value is added. For instance, if I set CHAR(15), and I try to store the value "Coding", it will use up the equivalent of 15 characters even though "Coding" is only 6 characters long. Char is good to use for things that will always be a given number of characters. Char would work well for something like a state_abbreviation.
-   **INT**
    -   Used to store integers.
    -   The columns that you will find mostly using the INT are things like a unique identifier for each table. The majority of rows in a table will not exceed 2.1 billion records. INT is good to use for most normal number values like a phone_number or a zip_code.
    -   **unsigned**  (positive numbers only) - can store numerical values from 0 up to 4294967295
    -   **signed**  (positive and negative numbers) - can store numerical values from -2147483648 up to 2147483647

  

-   **BIGINT**
    -   BIGINT would be used for columns that would need to store huge numbers. In most cases, you wouldn't need BIGINT, but if you wanted to store something like a Facebook id when using Facebook's API, since they have over a billion users the id will need to be a data type of BIGINT.
    -   **unsigned** (again positive numbers only) -  can store numerical values from 0 up to 18446744073709551615
    -   **signed** (positive and negative numbers) - can store numerical values from 9223372036854775807 to -9223372036854775808.

  

-   **TINYINT**
    -   TINYINT would be good to use for numbers that will be relatively small. A good example of something that would use a TINYINT is user level identifier (0 - inactive user, 1 - active user, 9 - admin).
    -   **unsigned -** can store numerical values from 0 up to 255
    -   **signed -** can store numerical values from -128 up to 127
-   **FLOAT**
    -   Used to store floating point numbers (numbers that need to have decimal places). An example column for this would be like an item_cost.
-   **TEXT**
    -   Used to store a large amount of text, like a description, message, or comment. Use this for any text that VARCHAR() is too small to handle.
-   **DATETIME**
    -   used to store a date and time in the format  _YYYY-MM-DD hh:mm:ss_

# Simple Blog

The best way to learn how to map out your tables is to look at a few examples. We will be going through a series of examples in the next 5 tabs before we continue with the assignments.

Study the wireframe below and then watch the video to see one way we could have laid out our ERD.

![](http://i.imgur.com/cMAmRPo.png)

## Video Walkthrough

# Likes

Look at the wireframe below and create an ERD diagram. Then look at the video afterwards and compare your ERD diagram with the demo.

**Step 1: Look at the wireframe and determine what database tables you need to be able to come up with the app.**

**Step 2: Set up the relationships and make sure you rename your foreign keys to be singular.**

![](http://i.imgur.com/1RV6v5R.jpg)

## Video Walkthough


# Food Reviews

Look at the wireframe below and create an ERD diagram. Then look at the video afterwards and compare your ERD diagram with the demo.

![](http://i.imgur.com/qwhXoRX.png)

## Video Walkthrough

N.B.: It is reasonable to include a '_rating_' or '_num_stars_' column in the reviews table, of type  _tinyint(1)_.

# Product Categories

Look at the wireframe below and create an ERD diagram. Then look at the video afterwards and compare your ERD diagram with the demo.

![](http://i.imgur.com/J1syoow.png)

## Video Walkthrough

# Belt Certifications

Look at the wireframe below and create an ERD diagram. Then look at the video afterwards and compare your ERD diagram with the demo.

![](http://i.imgur.com/WsZZtj7.png)

## Video Walkthrough

## Assignment: Books

Create an ERD to represent the database for an application that tracks users, books, and user's favorite books.

Each book should have a title and an author, and each user should be able to save a list of their favorite books. Use the MySQL Workbench for creating this database. For the purposes of this assignment, you may include the author's name directly into the book records, even though it would be better normalized by creating a separate author's table.


## Assignment: Blogs

Create the ERD for a platform that allows users to create blogs, similar to [blogspot.com](http://blogspot.com/).

The platform must allow users to register, create multiple blogs, and even allow the user to invite other users to be co-administrators of the blog. The administrators of the blog can change the blog name, add posts, edit posts, add comments, edit comments for each post, and upload new files associated with the blog post. We also want to capture information about which page the logged in users are viewing (e.g. page visited, when they visited, how long they stayed, IP address, name, etc).

Use the MySQL workbench to complete this assignment.

## Assignment: User Dashboard

Create an ERD for the User Dashboard wireframe.

You can download the [wireframe here](https://s3.amazonaws.com/General_V88/boomyeah/company_209/chapter_2692/handouts/chapter2692_3350_MVC-advanced-assignment.pdf).

Note: There are many ways to approach structuring data for large web applications. Try thinking through some of the actions a user can do and make your ERD fit the functionality.

## Assignment: Normalization

Recreate the below ERD model so that it passes all 3 forms of Normalization.

This ERD is in violation of multiple Normalization forms. The purpose of this ERD is to keep track of the students information and ALL the interests that a student may have.

**Hint: You will need to create a new type of relationship.**

<img src="https://i.ibb.co/r4nRZBX/chapter3052-7919-MVC-advanced-assignment.png" border="0">

