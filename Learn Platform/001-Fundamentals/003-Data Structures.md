# Introduction to Data Structures

## Objectives:

-   Understand why data structures are important
-   Understand bits and bytes
-   Understand Big O Notation
-   Understand why memory management is important

----------

Data structures are data types that allow us to store and manage multiple values. Where  **primitive**  data types are single values, like numbers or strings,  **data structures**  allow us to have collections of values in a single variable. Arrays, lists, and dictionaries are each examples of data structures.

We have been  _using_  data structures for a few weeks, but now that we know how to construct classes with methods, we're going to take a deeper dive into how these work under the hood! We're going to start by looking specifically at one data structure known as a  **singly linked list**. The list is simply a  **class**  that has  **methods**; just as Python's list class has methods like  `append(val)`  and  `pop()`, we're going to write a class with the same functionality.

## Video Overview

<iframe width="560" height="315" src="https://www.youtube.com/embed/o-flkaAcRZ4" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

### Helpful links

1.  [https://web.stanford.edu/class/cs101/bits-bytes.html](https://web.stanford.edu/class/cs101/bits-bytes.html)
2.  [https://digital-photography-school.com/16-bit-vs-32-bit-vs-64-bit-what-does-it-all-mean/](https://digital-photography-school.com/16-bit-vs-32-bit-vs-64-bit-what-does-it-all-mean/)

# Linked Lists

## Objectives:

-   Review how arrays actually work
-   Understand how a linked list uses  _nodes_  to hold data
-   Understand the differences between linked lists and arrays
-   Construct a node and list class

----------

## Arrays

We already know about arrays.  **Arrays**  keep track of multiple values and are optimized for random access, meaning we can access the values in the array by index number, e.g.  _myArray[3]_. Arrays are a good choice for when we need to keep values in a specific order or  _randomly access_ a given value somewhere in the middle. This is possible because an array takes up an entire set of consecutive cells in memory. However, arrays are less efficient when we have to do a lot of inserting or deleting from the middle, as we must shift other values around to maintain order.

A  **Linked List**  is another data structure that stores values in sequential order, but is more optimized for quick insertion and deletion. Once you've seen how they work, this will make more sense!

Let's look at how we would insert a value into an array. Let's say we've got an array of strings, and we want to keep things alphabetical:

<img src="https://i.ibb.co/WDMZfCq/chapter3151-4173-array.png" alt="chapter3151-4173-array" border="0">

Now we want to add Ben to our contacts list, so his name should be added right between Alice and Chad. Since this is an array, what do we have to do?  

<img src="https://i.ibb.co/cD4Fp6M/chapter3151-4174-array2.png" alt="chapter3151-4174-array2" border="0">


If you said shift the four names to the right of where Ben needs to go, you're right. Shifting is an expensive operation, because it means we have to alter potentially every element in the array just to add one item. Imagine we have a million names and then want to add one to the front! That's one million operations. Yikes.

## Linked Lists

Enter linked lists. What's different about linked lists compared to arrays? Instead of storing all values consecutively in memory, each element in the collection holds not only its value, but also a link to the element next to it. But how can we store both of these pieces of data in one variable? If you're thinking classes, you are on the right track! To follow convention, we're going to call this container a  **node**.

### What is a node?

A  **node** is a  _class_  that, as described above, is going to have two attributes:

-   **value** - the actual value to be stored (eg. "Alice", "Ben", "Chad", etc.)
-   **next** -  a link to the node next to it in the list. For a computer, this is a reference to, or memory address of, that node. For a developer, this is a variable name that _points to_  or _references_  another node. If there isn't anything next to it, **next** can be set to **None**. Because we won't necessarily know who our node's neighbor will be upon creation, let's set the default to None.
```py
class SLNode:
 def __init__(self, value):
  self.value = value
  self.next = None
```
It is certainly possible for us to add more attributes to our node, but for now, we'll just have these two.

### How do we get from a node to a list?

Now that we have containers, or  **nodes**, for each element in our list, we need a way to actually  _manage_  them (i.e. to add new values to our list, remove values from the list, etc.). If you're thinking we need another class, you're absolutely right!

What's neat about a linked list is, as long as we know the first node, we can get to every other node by starting at the front and moving to the neighboring node as long as there is one. But we're getting ahead of ourselves--that will come soon enough!

Conventionally, this first node is referred to as the  **head**  of the list. When we first create a list, it will be empty:
```py
class SList:
    def __init__(self):
    	self.head = None
```
Now that we have our classes, let's make _an instance_ of our list:
```py
my_list = SList()
```
This may feel pretty abstract, but remember that the principles are still the same as when we made a User and BankAccount class. It's just that the goal of our class is different--we're not trying to represent a User, but a data structure called a  **Singly Linked List**. In the next assignment, we're going to add some methods to our SList class.

The goal of this video is to give you a visual to start thinking about these concepts. In the next module, you'll practice the code yourself:


# Singly Linked Lists

## Objectives:

-   Learn how linked lists work
-   Learn more about pointers
-   Learn how to traverse through a linked list

----------

Our class needs some methods! Let's start by adding a method that lets us add a node to the front of our list. We're going to take this slow.

### Adding a Value to the Front

A common functionality of a list is to be able to add values, so let's add such a method to our class.

1.  Just as we would pass in a value to a Python list's append method, our add_to_front method should accept a value to be added to the list:
    ```py
        class SList:
            def __init__(self):
                self.head = None
            def add_to_front(self, val):	# added this line, takes a value
    ```
2.  The first thing our method should do is create a node:
    ```py
    	def add_to_front(self, val):
                new_node = SLNode(val)	# create a new instance of our Node class using the given value
    ```
    This implies we have already created the Node class. We did this in the previous tab, but as a reminder, in a separate class (same file is okay):
    ```py
        class SLNode:
            def __init__(self, val):
                self.value = val
                self.next = None
    ```
3.  We want this new node to be the front of our list, but let's not be too hasty. Since the only node we have a reference to in our list is the head, if we replace it right away, we'll lose our reference to the current head, so let's save it before moving forward:
    ```py
    	def add_to_front(self, val):
                new_node = SLNode(val)
                current_head = self.head	# save the current head in a variable
    ```
4.  Currently our new node doesn't have a neighbor. Because we're trying to add this new node to the front, we now know its neighbor should be the current head that we just saved:
    ```py
    	def add_to_front(self, val):
                new_node = SLNode(val)
                current_head = self.head
                new_node.next = current_head	# SET the new node's next TO the list's current head
    ```
5.  Finally, we need this new node to be the head of our list:
    ```py
    	def add_to_front(self, val):
                new_node = SLNode(val)
                current_head = self.head
                new_node.next = current_head
                self.head = new_node	# SET the list's head TO the node we created in the last step
                return self	                # return self to allow for chaining
    ```

Take a moment to compare this functionality to appending a value to the front of an array. Hopefully you can see some of the benefits--no shifting necessary, no matter how many elements we have in our list!

### Traversing Through a List

Since this is pretty abstract, it might be helpful to have a function that goes through each node and prints its value. This is a great opportunity to learn how to  _traverse through a linked list_. To iterate through an array, we used a for loop with an index as our iterator. However, since our linked list isn't indexed, we have to come up with a different iterator. We'll use a  **pointer**  that will, in a loop, point at each node.

1.  This method won't require any input:
    ```py
    	def print_values(self):
    ```
2.  We need to start at the front of our list, so let's create a pointer to our first node:
    ```py
    	def print_values(self):
                runner = self.head	# a pointer to the list's first node
	```
3.  As long as the runner variable is pointing to a node:
    ```py
    	def print_values(self):
                runner = self.head
                while (runner != None):	# iterating while runner is a node and not None
    ```
4.  Let's print its value:
    ```py
    	def print_values(self):
                runner = self.head
                while (runner != None):
                    print(runner.value)	# print the current node's value
    ```
5.  Then, we need to "increment" our runner to the next node, or update the runner so it is pointing to its neighbor:
    ```py
    	def print_values(self):
                runner = self.head
                while (runner != None):
                    print(runner.value)
            	runner = runner.next 	# set the runner to its neighbor
                return self	                # once the loop is done, return self to allow for chaining
    ```

### Traversing Through a List and Adding a Value to the End

Let's practice traversing one more time. If we want to add a new node anywhere in our list, it just needs to become a neighbor of an existing node. To become the last node in our list, the list's current last node needs to point to this new node.

1.  This method will require a value to be added:
    ```py
    	def add_to_back(self, val):	# accepts a value
    ```
2.  Then we'll want to create a new node with the given value:
    ```py
    	def add_to_back(self, val):
                new_node = SLNode(val)	# create a new instance of our Node class with the given value
    ```
3.  Start an iterator at the beginning of the list:
    ```py
    	def add_to_back(self, val):
                new_node = SLNode(val)
                runner = self.head	    # set an iterator to start at the front of the list
    ```
4.  Because we want to make it to the last node, we'll want to stop on the node who doesn't have a neighbor:
    ```py
    	def add_to_back(self, val):
                new_node = SLNode(val)
                runner = self.head
                while (runner.next != None):	# iterator until the iterator doesn't have a neighbor
    ```
5.  Increment the runner to its neighbor (since we just checked to ensure there is, in fact, a neighbor):
    ```py
    	def add_to_back(self, val):
                new_node = SLNode(val)
                runner = self.head
                while (runner.next != None):
                    runner = runner.next # increment the runner to the next node in the list
    ```
6.  When the loop has finished running, runner will be pointing to the last node. Its next is currently set to None, but we want to make the new node we created at the beginning of this method to be its neighbor:
    ```py
    	def add_to_back(self, val):
                new_node = SLNode(val)
                runner = self.head
                while (runner.next != None):
                    runner = runner.next
                runner.next = new_node	# increment the runner to the next node in the list
    ```
7.  Consider the edge case where our list is empty. In that case, adding to the front would be the same as adding to the back. Since we've already written that method, let's use it!
    ```py
    	def add_to_back(self, val):
                if self.head == None:	# if the list is empty
                    self.add_to_front(val)	# run the add_to_front method
            	return self	# let's make sure the rest of this function doesn't happen if we add to the front
                new_node = SLNode(val)
                runner = self.head
                while (runner.next != None):
                    runner = runner.next
                runner.next = new_node	# increment the runner to the next node in the list
                return self                 # return self to allow for chaining
    ```

Let's test our class!
```py
my_list = SList()	# create a new instance of a list
my_list.add_to_front("are").add_to_front("Linked lists").add_to_back("fun!").print_values()    # chaining, yeah!
# output should be:
# Linked lists
# are
# fun!
```
_If you're feeling discouraged, confused, or overwhelmed, don't worry. We guarantee you are not the only one. This is a really difficult concept to pick up the first time around. Just keep practicing and breaking down each step one line at a time. Try to figure out which parts don't make sense and then talk it out with a classmate, TA, or instructor._

Once you have a good grasp of this idea of nodes with pointers, you have the building blocks for building some other really neat data structures like binary search trees, tries, graphs, and more. As it's such a critical concept, practice and review the code above so that you are able to re-create the code demonstrated above without looking at the platform. Make sure you feel very comfortable with adding a new node, traversing through the linked list, etc. Once you can create both SList and Node without looking at the codes above, then move on to some of the additional challenges.

### Additional Challenges

These are challenging! Hop up to a whiteboard, grab a cohort mate if available, and try to work through these together.

1.  `remove_from_front(self)`  - remove the first node and return its value
2.  `remove_from_back(self)`  - remove the last node and return its value
3.  `remove_val(self, val)`  - remove the first node with the given value
    Consider the following cases:-   the node with the given value is the first node
    -   the node with the given value is in the middle of the list
    -   the node with the given value is the last node
4.  `insert_at(self, val, n)`  - insert a node with value  _val_  as the  _n_th  node in the list
    Consider the following cases:-   _n_  is 0
    -   _n_  is the length of the list
    -   _n_  is between 0 and the length of the list

- [ ]  Create a new Python file and recreate the Node and SList classes
    
- [ ]  Add the add_to_front method to your SList class
    
- [ ]  Add the print_values method to your SList class
    
- [ ]  Add the add_to_back method to your SList class
    
- [ ]  Practice the above in code and on paper/whiteboard. Then try to write these methods from scratch without referencing the platform!
    
- [ ]  Practice the above on your computer and on paper or a whiteboard. Then try to write these methods from scratch without referencing the platform!
    
- [ ]  NINJA BONUS: complete the remove_from_front method
    
- [ ]  NINJA BONUS: complete the remove_from_back method
    
- [ ]  NINJA BONUS: complete the remove_val method
    
- [ ]  SENSEI BONUS: complete the insert_at method
    
- [ ]  SENSEI BONUS: consider and account for edge cases for all previous methods
#

# Other Data Structures

## Objectives:

-   Be exposed to other common data structures

----------

Throughout the rest of the course, we'll be reviewing several other common data structures. The video below provides a brief overview of some of these.

## Helpful Links

-   Hash Tables

-   [https://en.wikipedia.org/wiki/Hash_table](https://en.wikipedia.org/wiki/Hash_table)

-   Binary Search Trees

-   [https://en.wikipedia.org/wiki/Binary_search_tree](https://en.wikipedia.org/wiki/Binary_search_tree)

-   Stacks & Queues

-   [https://www.cs.cmu.edu/~adamchik/15-121/lectures/Stacks%20and%20Queues/](https://www.cs.cmu.edu/~adamchik/15-121/lectures/Stacks%20and%20Queues/Stacks%20and%20Queues.html)


# Doubly Linked Lists

## Objectives:

-   Understand the differences between singly linked lists and doubly linked lists
-   Understand the pros and cons of each
-   Construct a doubly linked list using OOP

----------

**Disclaimer**: If you're ahead and have already finished all the mandatory assignments, please work on this assignments before moving on to Flask. Many students mention how they were expected to do linked list on the whiteboard during their technical interviews. If you're on schedule or not so ahead, you can skip this assignment and come back when you have more time.

----------

These exercises are designed to help you prepare for technical interviews and to reinforce concepts you've learned about OOP. If you want to be better prepared for technical interviews, it's helpful to know linked lists and how they are used. Some interesting puzzles can be solved using linked lists (and you may be asked to solve problems using linked lists in technical interviews).

In technical interviews, our alumni are commonly asked problems involving linked lists. Learn about  _doubly-linked lists_, also known as  _DLists_. We started with  _singly-linked lists_  because they are simpler, but here's an opportunity to stretch your understanding and learn more by researching doubly-linked lists.

[http://en.wikipedia.org/wiki/Doubly_linked_list](http://en.wikipedia.org/wiki/Doubly_linked_list)  is a great start.

Once you have learned about linked lists, build a class in Python and demonstrate how you can:

-   add a new node to the end of the list,
-   delete an existing node,
-   insert a node between existing nodes (eg. before a given value, at a certain index, etc.)

You should have two classes for this: DoublyLinkedList and Node. Have DoublyLinkedList be the class that allows you to add a new node, delete an existing node, insert a new node between existing nodes, print out the values in the linked list. Have Node be the class that has the necessary properties for the node.

Please also think about the following:

1.  How would you know if you have a circular linked list?
2.  How would you get to the middle of the linked list?
3.  How would you remove duplicate values in the list?
4.  How would you reverse the values in the list?

Think hard about these puzzles and how you could potentially use multiple runners to tackle some of these tasks.

Spend up to 5 hours on this assignment.

#


