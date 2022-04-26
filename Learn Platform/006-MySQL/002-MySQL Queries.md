# SQL

For any relational database like MySQL, you will interact with it using SQL. In the previous chapter, we learned how to design a schema for our data: we set up the collections that we needed, and we set up the relationships among tables. Now we will see the importance of relationships, and how to use SQL to adjust the data in any way we can imagine.

<img src="https://i.ibb.co/z61Lxhv/chapter3569-6756-sql-icon.png"  border="0">

SQL stands for **Structured Query Language**, which is a programming language designed for managing data in relational databases. SQL statements are used to perform tasks; they can  **SELECT** data, **SELECT** data **WHERE** some conditions are true, **INSERT** data, **UPDATE** data, **DELETE** data, and **JOIN** different tables together. As we go over all of the basic SQL commands, be patient. You will be learning a domain-specific language, unrelated to languages you may have previously seen. However, mastering SQL is the key to mastering the database component of your application.

## Database and SQL

We will install and run a MySQL  **server**  on our operating system to connect first to MySQL Workbench, and later our web applications. This will be a database server, which will be listening for connections on localhost (just like our Flask web servers). Also like our web servers, our MySQL server will be assigned a port number. After we install and configure MySQL, we will then connect to our database from MySQL Workbench via localhost and whichever port our MySQL server is using.

# Installation (Mac)

We will use the  **homebrew**  package manager to install and initialize the required MySQL software. If you haven't yet installed homebrew, you may  [refer back](http://learn.codingdojo.com/m/7/3679/24615)  to the installation steps from earlier in the course.

#### All of the listed steps below are commands you will run in your Terminal.

1.  Use homebrew to install MySQL.  
    `brew install mysql`
2.  Use homebrew to start your MySQL Server as a "service", meaning it will run in the background and allow connections.  
    `brew services start mysql`
3.  Now with MySQL installed, you have access to some new command line tools. Run the following command to set the MySQL  **root**  user's password to "root".  
    `mysqladmin -u root password "root"`  
    `mysql -u root -p`
    
    ----------
    
    # Installation (Windows 10)
    
    1.  **Download** the required MySQL software from the MySQL  [website](https://dev.mysql.com/downloads/mysql/)  Choose the MySQL Installer MSI Option.
    2.  Follow the installer guidelines, with the following considerations:
        -   Choose the password "root" for your root user password
        -   For "Windows Service" make sure you have the "Configure MySQL Server as a Windows Service" and "Start the MySQL Server at System Startup" options selected.
    
    <img src="https://i.ibb.co/HnrT4Bk/mysql-service.png" border="0">
    
    
    The installer will configure your Windows system to run the MySQL Server automatically on startup, listening on the default port 3306, as well as establish the required environment variables to run MySQL tools from a Windows shell
    
    Open a MySQL shell from CMD/PowerShell to make sure everything is working correctly:
    
    `mysql -u root -p`  and enter "root" when prompted
    
    ----------
    
    ### Troubleshooting:
    
    **Problem:**  Running  `mysql`  in CMD/PowerShell gives the following error:  `'mysql' is not recognized...`
    
    **Solution:**  Make sure you have an Environment Variable PATH to your MySQL executables. Likely to be in C:\\Program Files\MySQL\MySQL Server 5.7\bin

# Connecting to MySQL Server

Now that you have installed, configured, and started a MySQL server on our operating system, we can now connect to it with MySQL Workbench.

Open up MySQL Workbench, which will bring up a main menu showing your different DB connections. Most of you will only have one, unless you have added more. Select the wrench icon to test and configure your connections.

><img src="https://i.ibb.co/FqxnkqV/mysql-conn-main.png" border="0">

Here you will notice the Hostname: 127.0.0.1 (the IP address for localhost), Port, and Username. Here you can change the port number if your MySQL server is on a different port. Test the connection with the button at the bottom of this menu.

<img src="https://i.ibb.co/PQ9BgLG/mysql-conn-config.png" border="0">

  

----------

# Changing your Port

If you wish to change the port on the MySQL server, you can do so by adding a configuration file to a specific directory path depending on your OS. If you do change your port here, make sure that your connection settings in MySQL Workbench also reflects this change.

Let's say we wanted to change the port our server is listening on to 3307 (instead of the default 3306). Create a file named  **my.cnf**  (the name is important), and add the following text:
```py
[client]
port = 3307
[mysqld]
port = 3307
```
Make sure this file gets saved to one the following directories, depending on your OS

### Mac/Linux:  `/etc/my.cnf`

### Windows:  `C:\MySQL\MySQLServer\my.cnf`

When the file is saved, you will need to restart your MySQL server to reflect this change

### Mac
```py
brew services restart mysql
```
### Windows
```py
NET STOP MYSQL
NET START MYSQL
```

# Importing Structure and or Data

There are two main ways to import structure (tables and columns) or data (rows or records) or a combination of both into your MySQL Workbench. If you have an SQL file, you can just copy and paste the commands into the editor and click run. If you have an ERD diagram, you can forward engineer into MySQL workbench. We will go over how to do both ways.

## From SQL to MySQL Workbench

## From ERD to MySQL Workbench


# SELECT Basics

First, let's go over how we can  **SELECT** data from a database. First, import the [twitter.sql](https://s3.amazonaws.com/General_V88/boomyeah/company_209/chapter_3569/handouts/chapter3569_5436_twitter.sql)  into your MySQL workbench. The twitter.sql file contains the SQL statements to create a database called **_twitter_** along with certain tables and pre-populated fields.

Remember that you are learning a new language. Watch the videos once, then watch it a second time following along. Also, make sure you run all of the commands listed out in this tab. Even though you might understand it conceptually, it is important that we type the commands so we can retain our knowledge.

## Import From  _twitter.sql_

Go ahead and download the [twitter.sql](https://s3.amazonaws.com/General_V88/boomyeah/company_209/chapter_3569/handouts/chapter3569_5436_twitter.sql)  file. Copy and paste what is in the .sql file into your MySQL Workbench editor. The ERD of the database is as follows:

![](http://i.imgur.com/pJ7GbOP.png)

## _users_

Let's see what's in the  **_users_**  table by running:
```sql
SELECT * 
FROM users;
```
## 

![](http://i.imgur.com/K8La9fJ.png)

## _faves_

Let's see what's in the  **_faves_**  table by running:
```sql
SELECT * 
FROM faves;
```
![](http://i.imgur.com/ZN20ATr.png)

## _follows_

Let's see what's in the  **_follows_**  table by running:
```sql
SELECT *  
FROM follows;
```
## 

![](http://i.imgur.com/WO4hyPX.png)

## _tweets_

Let's see what's in the  **_tweets_**  table by running:
```sql
SELECT *
FROM tweets;
```
## 

![](http://i.imgur.com/lbwsJ59.png)

## Basics

What query would you run to get all of the users?
```sql
SELECT * 
FROM users;
```
What query would you run to only get the first names of all of the users?
```sql
SELECT first_name 
FROM users;
```
What query would you run to only get the first and last names of all of the users?  
```sql
SELECT first_name, last_name
FROM users;
```
## SELECT w/ Conditionals

What query would you run to only get the first name of users with id of 2?
```sql
SELECT first_name
FROM users
WHERE id = 2;
```
What query would you run to get the last names of users with id of 2 or 3?
```sql
SELECT last_name
FROM users
WHERE id = 2 OR id = 3;
```
What query would you run to get all of the users with id greater than 2?
```sql
SELECT *
FROM users
WHERE id > 2;
```
What query would you run to get all of the users with id less than or equal to 3?
```sql
SELECT *
FROM users
WHERE id <= 3;
```
What query would you run to get all of the users with first names ending in "e"?
```sql
SELECT * 
FROM users
WHERE first_name LIKE "%e";
```
What query would you run to get all of the users with first names starting in "K"?
```sql
SELECT * 
FROM users
WHERE first_name LIKE "K%";
```
## SELECT w/ Sorting

What query would you run to get all of the users with the youngest users at the top of the table?
```sql
SELECT *
FROM users
ORDER BY birthday DESC;
```
What query would you run to get all of the users with the oldest users at the top of the table?
```sql
SELECT *
FROM users
ORDER BY birthday ASC;
```
What query would you run to get all of the users with the first name that ends with "e" with the youngest users at the top of the table?
```sql
SELECT *
FROM users
WHERE first_name LIKE "%e"
ORDER BY birthday DESC;
```
What query would you run to get only the first names of all of the users in alphabetical order?
```sql
SELECT first_name
FROM users
ORDER BY first_name;
```
The default for ORDER BY is ASC so we can leave that part out if we want the sorting to be ascending.

### Note

**Before moving on to the next tab, it will be best to go over the following tutorials on SQL Zoo:**

-   SELECT Basics: [http://sqlzoo.net/wiki/SQLZOO:SELECT_basics](http://sqlzoo.net/wiki/SQLZOO:SELECT_basics)
-   SELECT name: [http://sqlzoo.net/wiki/SELECT_names](http://sqlzoo.net/wiki/SELECT_names)
-   SELECT from World: [http://sqlzoo.net/wiki/SELECT_from_WORLD_Tutorial](http://sqlzoo.net/wiki/SELECT_from_WORLD_Tutorial)

# INSERT Basics

Now, let's go over how we can INSERT data. We can do this in two ways. One way is to manipulate the table directly using our MySQL Workbench and another way is to run direct SQL commands in the editor.

Even if you are using the GUI to insert data, it is important to see what kind of SQL commands it is running. We are going to have to run INSERT statements using SQL commands later so it is important that we know how to INSERT data both ways.

## Inserting Records

The SQL command pattern for INSERTing records is as follows:
```sql
INSERT INTO table_name (column_name1, column_name2) 
VALUES('column1_value', 'column2_value');
```

# UPDATE Basics

We can UPDATE our database in two ways as well. Once again, it is important to pay attention to the SQL commands that are being run even if we just use the GUI because we will have to run UPDATE commands later in the bootcamp. Try updating your table both ways.

## Updating Records

The SQL command pattern for updating/editing records is as follows:
```sql
UPDATE table_name SET column_name1 = 'some_value', column_name2='another_value' WHERE condition(s)
```
**IMPORTANT**: if  **WHERE** condition is not added to the **UPDATE** statement, the changes will be applied to every record in the table.

# DELETE Basics

You can DELETE your records as well.

If you are getting an error regarding SQL SAFE UPDATES, run the following command to let MySQL Workbench know that you know what you are doing and you want to DELETE stuff from the database.
```sql
SET SQL_SAFE_UPDATES = 0;
```
## Deleting Records

The SQL command pattern for deleting/removing records is as follows:
```sql
DELETE FROM table_name WHERE condition(s)
```
**IMPORTANT**: if  **WHERE** condition is not added to the **DELETE** statement, it will delete all the records on the table.

# Fun with Functions

Go ahead and follow along with the video to practice more SQL commands.

Functions can be applied to the selected columns. There can be a variety of reasons why you might want to use functions. Below are some of the most commonly used functions separated by the purpose for using them. Get familiar with how to use some of these functions, but DO NOT TRY TO MEMORIZE ALL OF THESE. If you understand how functions work, then you should be able to quickly reference a function and understand how to use it.

When calling a function on a column, make sure that column is the appropriate Data Type for that function.

**Text Functions Data Types (**VARCHAR, TEXT, CHAR etc.**)**

**Numeric Functions Data Types (**INT, BIGINT, FLOAT etc.**)**

**Date and Time Functions Data Types (**DATETIME**)**

**SELECT** _**FUNCTION** **(**column**)**_ **FROM** _table_name_

<img src="https://i.ibb.co/2q7Lq52/chapter2161-1533-Screen-Shot-2013-10-08-at-10-24-19-PM.png" border="0"><img src="https://i.ibb.co/k9CZNRm/chapter2161-1532-Screen-Shot-2013-10-08-at-10-15-47-PM.png" border="0">

To see the different types of formatting for DATE_FORMAT() look here: [SQL Date Format](https://www.w3schools.com/sql/func_mysql_date_format.asp).

Again, DO NOT TRY TO MEMORIZE THESE FUNCTIONS. You should be aware of the types of functions that exist, and look up the details only when needed. For example, the RAND() function above  _actually_ returns a decimal number as low as  **0**  and as high as "**almost 1.0**". Is this detail worth memorizing? No! Just become familiar with them, and develop a keen eye for reading documentation and quickly understanding functions.

# Joining Tables

Remember  _foreign keys_  from the last chapter? We now get to put them to use! We JOIN two tables on the _ids_ that match each other. This means that we can't JOIN tables together that don't have a relationship with each other (e.g. **One to One**, **One to Many**, **Many to Many**). A _foreign key_  in a table matches up directly with an id in another table. Let's take a peek at what this looks like.

Go ahead and download the [morepractice.sql](http://s3.amazonaws.com/General_V88/boomyeah/company_209/chapter_3569/handouts/chapter3569_5437_morepractice.sql)  and follow along with the video.

Here is another example:

### **One to One**
```sql
SELECT * FROM customers 
JOIN addresses ON addresses.id = customers.address_id;
```
<img src="https://i.ibb.co/G5d3w8M/chapter2161-1536-Screen-Shot-2013-10-09-at-8-56-44-AM.png" border="0">

## ![](http://i.imgur.com/0Bw6pb7.gif)

### **One to Many**
```sql
SELECT * FROM orders 
JOIN customers ON customers.id = orders.customer_id;
```
<img src="https://i.ibb.co/P4kWVk4/chapter2161-1537-Screen-Shot-2013-10-09-at-8-57-06-AM.png" border="0">

## 

![](http://i.imgur.com/SdHYDDl.gif)

### **Many to Many**
```sql
SELECT * FROM orders 
JOIN items_orders ON orders.id = items_orders.order_id 
JOIN items ON items.id = items_orders.item_id;
```
<img src="https://i.ibb.co/Xp1bqWY/chapter2161-1538-Screen-Shot-2013-10-09-at-8-57-35-AM.png" border="0">

![](http://i.imgur.com/zu3hsWo.gif)

The above examples are using a JOIN, also referred to as INNER JOIN. However, there may be times where you would want to use a different type of JOIN. Imagine that in the **One to Many** relationship above there was a customer that had not yet placed an order. There wouldn't be a  _customer_id_  listed in the  **_orders_**  table. If we wanted to get the results of all the customers orders including the customers that hadn't yet placed an order we would have to use a **LEFT JOIN**. See the visual representations of what you can expect to be included when using different types of joins.

## Grouping Results

In the previous section, we saw how we could use functions to manipulate a single value in a single row. With  **GROUP BY**, we will group multiple rows together, by performing a function to combine the values of those rows. Because this results in a single result for the group, it will combine those grouped rows into a single resultant row.

As you can imagine, there are many different ways that we might combine multiple values into a result. Below are a list of the most common ones, often called  _Grouping Functions_  or  _Aggregate Functions_.

**Aggregate Functions**

<img src="https://i.ibb.co/9Gj499B/chapter2161-1534-Screen-Shot-2013-10-08-at-11-17-10-PM.png" border="0">

# Left Join

In addition to the basic JOIN, there are many other types of joins that you can do in SQL. However, you can make any web application using only JOIN and LEFT JOIN. This is why we advise our students that once they understand the basic JOIN, to focus only on learning the LEFT JOIN. These two are enough.

Only after you have mastered LEFT JOIN should you move on to additional JOINs. It is very important for you to run all of the following commands in this tab and visualize what is happening. We are joining the tables, starting from left to right, gluing each table based on the _primary id_  and  _foreign key_. This is why we set up relationships so we can do LEFT JOINs and create customized tables when we need them.

First, study the ERD below. Then run the commands that follow.

![](http://i.imgur.com/pJ7GbOP.png)

We will still use the [twitter.sql](https://s3.amazonaws.com/General_V88/boomyeah/company_209/chapter_3569/handouts/chapter3569_5436_twitter.sql)  database file for this exercise.

----------

### **1. What query would you run to get all tweets from the user id of 1?**
```sql
SELECT *
FROM users
LEFT JOIN tweets
ON users.id = tweets.user_id
WHERE users.id = 1;
```
![](http://i.imgur.com/ZhmF9pB.png)

![](http://i.imgur.com/Mr8VQru.gif)

You can just grab the tweets by:
```sql
SELECT tweets.tweet
FROM users
LEFT JOIN tweets
ON users.id = tweets.user_id
WHERE users.id = 1;
```
![](http://i.imgur.com/gKNg297.png)

Or rename the output column that you want as  _kobe_tweets_  by modifying the statement to look like the following:
```sql
SELECT tweets.tweet as kobe_tweets
FROM users
LEFT JOIN tweets
ON users.id = tweets.user_id
WHERE users.id = 1;
```
![](http://i.imgur.com/VV9ZGWn.png)

----------

### **2. What query would return all the tweets that the user with id 2 has tagged as favorites?**
```sql
SELECT first_name, tweet
FROM users
LEFT JOIN faves
ON users.id = faves.user_id
LEFT JOIN tweets
ON faves.tweet_id = tweets.id
WHERE users.id = 2;
```
![](http://i.imgur.com/2nmRPT9.png)

![](http://i.imgur.com/OXmW155.gif)

### 

----------

### 3. What query would you run to get all the tweets that user with id 2, or user with id 1, has tagged as favorites?
```sql
SELECT first_name, tweet
FROM users
LEFT JOIN faves
ON users.id = faves.user_id
LEFT JOIN tweets
ON faves.tweet_id = tweets.id
WHERE users.id = 1 OR users.id = 2;
```
![](http://i.imgur.com/VzP6Fy3.png)

----------

### **4. What query would you run to get all the users that are _following_ the user with id 1?**

This will be the first time we are introduced to a  **self-join**. This often scares a lot of the students, but we aren't doing anything new. We are just dealing with a  **many to many relationship, but we are using the same table twice**.

For example, we know that one user can have many followers and that one user can follow many other users. This is a many to many relationship but the two rows that are having a relationship just happen to be of the same type. We could have another table called _followers_ but that would be repetitive because we would have the same columns or field names as we are just storing a user. We don't need the second table because we can do a self-join.  **The key word to remember is the word "AS" because it lets us join the same table twice by providing SQL with another variable to reference the table that is getting joined again.**
```sql
SELECT users.first_name as followed, users2.first_name as follower
FROM users
LEFT JOIN follows
ON users.id = follows.followed_id
LEFT JOIN users as users2
ON users2.id = follows.follower_id
WHERE users.id = 1;
```
![](http://i.imgur.com/diNQAyl.png)

![](http://i.imgur.com/1BamKdr.gif)

----------

### **5. What query would you run to get all users that are  _not_  following the user with id of 2?**

This requires  _nested queries_, which you can learn about at [http://sqlzoo.net/wiki/SELECT_within_SELECT_Tutorial](http://sqlzoo.net/wiki/SELECT_within_SELECT_Tutorial).
```sql
SELECT *
FROM users
WHERE users.id NOT IN (
SELECT follower_id
FROM follows
WHERE followed_id = 2
) AND users.id != 2;
```
We can run functions on specific columns and often times it is paired up with the GROUP BY statement. We will have plenty of practice with functions in the next tab.
```sql
SELECT users.first_name as user, COUNT(users2.first_name) as follower_count
FROM users
LEFT JOIN follows
ON users.id = follows.followed_id
LEFT JOIN users as users2
ON users2.id = follows.follower_id
WHERE users.id = 1
GROUP BY users.id
```
#### 

![](http://i.imgur.com/TIGtZd0.png)

## Left Join vs. Join

#### 

As mentioned earlier, LEFT JOIN and JOIN are all that you need for web development. They are very similar, but you should not think of them interchangeably. There is a difference in the output that they provide, specifically in the cases where a record in one table has no matching record in the joining table.

For example, running the following SQL command in our **_twitter_** database will result in the following:
```sql
SELECT first_name, tweet
FROM users
LEFT JOIN tweets
ON users.id = tweets.user_id
```
![](http://i.imgur.com/UudNV2D.png)

Notice that this result includes a final row containing Rajon with no associated tweet.

Now if we change the LEFT JOIN command to the JOIN command, the output will be as follows:
```sql
SELECT first_name, tweet
FROM users
JOIN tweets
ON users.id = tweets.user_id
```
![](http://i.imgur.com/rAADn41.png)

In the second example, Rajon is omitted from the table. When SQL uses the keyword JOIN, it only includes those records that have matches on both sides. It will omit any records that don't have a '_partner'_.

On the other hand, LEFT JOIN will include all the records from the  _first_ table (the 'left' table, the first one mentioned when reading from left to right),  _regardless_  of whether that record has a matching _foreign key_ in the (right) table that we are trying to join to it.

To summarize, JOIN will only include the intersection of the two tables, whereas LEFT JOIN will include all records from the first table, plus the records from the second table that correspond. This is why the JOIN is sometimes called the INNER JOIN, while all the other joins (including LEFT JOIN) are referred to as OUTER JOINs.

# Exporting Database

We can export the database that we built from our MySQL workbench into an SQL file. If we want to share our database records to other developers, we can just send them the SQL file and they can run the export on their local machine to create the databases and populate it with data.

We would also have to export our database when we submit our belt exams so that, whoever is grading your application, can execute the .sql file that you provided and they can use the same database you used to work on the exam.

# Quiz

1. You can use the BETWEEN operator for which of the following scenarios

- [ ]  A. finding all the rows between 2 values with type DATETIME
- [ ]  B. finding all the rows between 2 values with type VARCHAR
- [ ]  C. finding all the rows between 2 values with type INT
- [ ]  D. Both A and C
- [x]  E. All of the above.

2. 'ORDER BY id DESC' will show the most recent record first (this assumes that we have created a table using the proper conventions with id being a unique primary key)

- [x]  True
- [ ]  False

3. Where do we apply mysql functions?

- [ ]  any of the columns specified in the select statement
- [ ]  in the where clause
- [x]  any place within a query where you are making reference to a column
- [ ]  only when using a group by statement

4. In the query 'SELECT * FROM users LEFT JOIN posts ON users.id = posts.user_id;' the left table is posts

- [ ]  True
- [x]  False

5. What will you expect to be returned from the following query 'SELECT * FROM customers JOIN orders ON customers.id = orders.customer_id;'

- [x]  Only the orders where the customer_id has a match for the id in the customers table
- [ ]  The orders where the customer_id has a match for the id in the customers table and all the customers that don't have a match
- [ ]  The orders where the customer_id has a match for the id in the customers table and all the orders that don't have a match
- [ ]  All the records in both tables

6. It is wise to specify a grouping function when using a GROUP BY statement

- [x]  True
- [ ]  False

7. What would the result of the following query be 'SELECT DATE_FORMAT('2012-03-09 12:30', '%W %M %D %Y at %r') AS great_time';

- [x]  Friday March 9th 2012 at 12:30:00 PM
- [ ]  Fri Mar 9 12' at 12:30
- [ ]  March 9th at 12:30:00
- [ ]  Friday Mar 9 2012 at 12:30 PM

8. In the following query, what would you expect to get returned 'SELECT clients.company, SUM(billing.amount) AS total_sales FROM clients LEFT JOIN billing ON billing.client_id = client.id GROUP BY clients.company HAVING SUM(billing.amount) > 3500;'

- [ ]  A list of all the companies and their total billing amounts
- [x]  A list of each company whose total billing amounts are greater than 3500
- [ ]  A list of companies with their total sales
- [ ]  A list of all the billing amounts that are greater than 3500

9. When would you want to use a LEFT JOIN instead of a JOIN?

- [x]  when there are records you wish to have displayed in the left table that don't have a match for the records in the right table
- [ ]  when there are records you wish to have displayed in the right table that don't have a match for the records in the left table
- [ ]  if you want to have all the records displayed for both tables even if they don't have a match
- [ ]  You can always use LEFT JOIN instead of JOIN

10. Which records will be displayed in the following query 'SELECT id, first_name FROM users LIMIT 11,10 ;'

- [x]  10 records of user's first_name and id, starting with the 12th record in the result (regardless of that record's id)
- [ ]  2 records of user's first_name and id, specifically the users with ids 11 and 10
- [ ]  10 records of user's first_name and id, starting with id = 11 (regardless of whether lower ids are found in the table)
- [ ]  11 records of user's first_name and id, starting with the 10th record in the result (regardless of that record's id)

## To Do: MySQL Workbench Setup

Use MySQLWorkbench to connect to your localhost.

Learn how to use MySQL workbench to do queries directly in the database. To connect to a specific database, use 'Use [databasename]' in the query box.

Create a text file with the commands you used as you query to the database. Upload the text file below.

## Assignment: MySQL Countries

Using the world database and the pictured ERD, complete all 8 of the below queries.

<img src="https://i.ibb.co/Cw4kX7Q/chapter2161-1539-Screen-Shot-2013-10-09-at-3-16-31-PM.png" border="0">

First grab the **_world_**  database  [(download the file here](https://s3.amazonaws.com/General_V88/boomyeah/company_209/chapter_3569/handouts/chapter3569_5432_wor
ld.sql))

If possible, work in groups and use MySQL Workbench to do the queries. We want you to get familiar with using MySQL workbench. The questions are of varying difficulty level.

Tip: If you are having difficulties, do the ones that are easier for you to solve first. Or separate the queries for each detail that is needed in each questions, then put them all together once you have the correct results for each separate query.

### Queries

1. What query would you run to get all the countries that speak Slovene? Your query should return the name of the country, language and language percentage. Your query should arrange the result by language percentage in descending order. (1)

2. What query would you run to display the total number of cities for each country? Your query should return the name of the country and the total number of cities. Your query should arrange the result by the number of cities in descending order. (3)

3. What query would you run to get all the cities in Mexico with a population of greater than 500,000? Your query should arrange the result by population in descending order. (1)

4. What query would you run to get all languages in each country with a percentage greater than 89%? Your query should arrange the result by percentage in descending order. (1)

5. What query would you run to get all the countries with Surface Area below 501 and Population greater than 100,000? (2)

6. What query would you run to get countries with only Constitutional Monarchy with a capital greater than 200 and a life expectancy greater than 75 years? (1)

7. What query would you run to get all the cities of Argentina inside the Buenos Aires district and have the population greater than 500, 000? The query should return the Country Name, City Name, District and Population. (2)

8. What query would you run to summarize the number of countries in each region? The query should display the name of the region and the number of countries. Also, the query should arrange the result by the number of countries in descending order. (2)

Note: You may download this PDF file displaying the expected results from the queries - **[Expected Results (World)](https://s3.amazonaws.com/General_V88/boomyeah/company_209/chapter_3569/handouts/chapter3569_5438_MySQL-Basic-World-Expected-Result.pdf)**

## Assignment: Sakila

Using the Sakila database, complete the below queries.

You can get the **_Sakila_**  database and ERD here ([sakila-data.sql](https://s3.amazonaws.com/General_V88/boomyeah/company_209/chapter_3569/handouts/chapter3569_5430_sakila-data.sql)  and [sakila-db-model.png](https://s3.amazonaws.com/General_V88/boomyeah/company_209/chapter_3569/handouts/chapter3569_5431_sakila-db-model.png)), please use these for reference.

### Note

Earlier in this section, we recommended for students name their tables all lower case and have a primary key called  _'id'_  in each table. These are the rules we follow, however not all developers follow these rules. The SQL file you'll be working with does NOT follow the rules we discussed, including naming the fields lower case. We still want you to follow the rules we taught, but use this as an opportunity to get comfortable with other SQL files that do not completely follow the rules of normalization.

### Queries

1. What query would you run to get all the customers inside city_id = 312? Your query should return customer first name, last name, email, and address.

2. What query would you run to get all comedy films? Your query should return film title, description, release year, rating, special features, and genre (category).

3. What query would you run to get all the films joined by actor_id=5? Your query should return the actor id, actor name, film title, description, and release year.

4. What query would you run to get all the customers in store_id = 1 and inside these cities (1, 42, 312 and 459)? Your query should return customer first name, last name, email, and address.

5. What query would you run to get all the films with a "rating = G" and "special feature = behind the scenes", joined by actor_id = 15? Your query should return the film title, description, release year, rating, and special feature.  _Hint: You may use LIKE function in getting the 'behind the scenes' part._

6. What query would you run to get all the actors that joined in the film_id = 369? Your query should return the film_id, title, actor_id, and actor_name.

7. What query would you run to get all drama films with a rental rate of 2.99? Your query should return film title, description, release year, rating, special features, and genre (category).

8. What query would you run to get all the action films which are joined by SANDRA KILMER? Your query should return film title, description, release year, rating, special features, genre (category), and actor's first name and last name.

Note: You may download this PDF file displaying the expected results from the questions above - [**Expected Result (Sakila)**](https://s3.amazonaws.com/General_V88/boomyeah/company_209/chapter_3569/handouts/chapter3569_5439_MySQL-Intermediate-Sakila-Expected-Result.pdf)

## Assignment: Friendships

Using the below ERD, write the SQL query that returns a list of users along with their friends' names.

<img src="https://i.ibb.co/HhynfSm/chapter3569-6392-friends.png" border="0">

Create the tables and populate them with some fake data. Your results should look like below:

|  first_name | last_name | friend_first_name | friend_last_name |
|--|--|--|--|
| Chris | Baker | Jessica | Davidson |
| Chris | Baker | James | Johnson |
| Chris | Baker | Diana | Smith |
| Diana | Smith | Chris | Baker |
| James | Johnson | Chris | Baker |
| Jessica | Davidson | Chris | Baker |


Your actual query will look something similar to this:
```sql
SELECT * FROM users 
LEFT JOIN friendships ON ____=____ 
LEFT JOIN users as user2 ON ____ = ____
```
Take note that we're joining the **_users_** table again but we're specifying the second  **_users_**  table  **as**  user2. You can then reference the second  **_users_** by calling user2 (e.g. user2.id, user2.first_name, etc).

You can also rename the fields that are displayed on the result by using the  **as**  keyword, like the below example:
```sql
SELECT user2.first_name as friend_first_name, user2.last_name as friend_last_name, ...  FROM ...
```
Knowing how to do joins can be tricky but is used quite often  _and will most likely appear again in your belt exam._

Note: The order which we return the results is alphabetical by friend_last_name.

## Assignment: Lead Gen Business

Complete the below SQL queries using the lead-gen-business-new database and the below wireframe.

<img src="https://i.ibb.co/Cn3WTpf/Lead-Gen-Biz-ERD.png" border="0">

### Note


If you're ahead, we strongly encourage that you work on this assignment as this would really help you understand how GROUP BY work and how powerful MySQL could be. If you have already spent more than 2 full days studying ERD and MySQL, just skip this assignment and come back later when you're done with the bootcamp.

If you already have a database called  **_lead-gen-business_**, go ahead and drop that database and recreate by importing the [lead-gen-business-new.sql](https://s3.amazonaws.com/General_V88/boomyeah/company_209/chapter_3569/handouts/chapter3569_5435_lead-gen-business-new.sql)  file. The database that is created will be different than the one in the  **_morepractice.sql_**  file that we used during the videos.

### Queries

1. What query would you run to get the total revenue for March of 2012?

2. What query would you run to get total revenue collected from the client with an id of 2?

3. What query would you run to get all the sites that client=10 owns?

4. What query would you run to get total # of sites created per month per year for the client with an id of 1? What about for client=20?

5. What query would you run to get the total # of leads generated for each of the sites between January 1, 2011 to February 15, 2011?

6. What query would you run to get a list of client names and the total # of leads we've generated for each of our clients between January 1, 2011 to December 31, 2011?

7. What query would you run to get a list of client names and the total # of leads we've generated for each client each month between months 1 - 6 of Year 2011?

8. What query would you run to get a list of client names and the total # of leads we've generated for each of our clients' sites between January 1, 2011 to December 31, 2011? Order this query by client id. Come up with a  **_second_**  query that shows all the clients, the site name(s), and the total number of leads generated from each site for all time.

9. Write a single query that retrieves total revenue collected from each client for each month of the year. Order it by client id.

10. Write a single query that retrieves all the sites that each client owns. Group the results so that each row shows a new client. It will become clearer when you add a new field called 'sites' that has all the sites that the client owns. (HINT: use GROUP_CONCAT)

Note: You may download this PDF file displaying the expected results from the questions above - [Expected Result (Leads)](https://s3.amazonaws.com/General_V88/boomyeah/company_209/chapter_3569/handouts/chapter3569_5440_MySQL-Optional-Leads-Expected-Result.pdf)

## Assignment: SQLZoo

Complete the tutorial at [http://sqlzoo.net/](http://sqlzoo.net/).

Notice how these SQL queries you learned are NOT just applicable for MySQL, but also on Oracle, SQL server, Postgres, Ingres, and any other SQL database you find. Finishing all the tutorials there will deepen your understanding on MySQL.

Note: In the tutorial, they discussed the nested functions and queries. Nested functions and queries should not be used unless it is absolutely necessary.



