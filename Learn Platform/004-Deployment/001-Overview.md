# Overview

## Objectives:

-   Learn what deployment is
-   Understand why deployment is important

----------

## Why Should I Learn to Deploy?

In your work as a web developer you will probably not be deploying your own work. The larger a company becomes, the more complicated the deployment process gets. This set of tasks is often automated, meaning a developer or team of developers is tasked with creating and managing internal tools that make deployment simple. This is a job in its own right, known as Dev Ops (development operations). That being said, there are plenty of good reasons to learn to deploy:

1.  **Your Portfolio**  - It is important to have a portfolio containing projects that can be shown to recruiters or interviewers. In order for potential employers to access and interact with your project, it has to be deployed to its own IP address.
2.  **Working Knowledge**  - Often when we follow up with interviewers, one comment we've received in the past is that students didn't have a solid understanding of deploying web applications. It is a highly desirable skill in case you end up being the only engineer at a young start-up. Also, this knowledge will help you integrate with a team that potentially has a lot of moving pieces.
3.  **The Extra Mile**  - After you've created all the client and server-side components, actually deploying your app is really the capstone to this process. There is nothing like seeing your site up and running on a domain that you've purchased.

## Where and How do I Deploy?

There are many services that assist with deployment. If you ever need to deploy a prototype quickly, these services might be the best choice. However, throughout the bootcamp we'll be learning the more challenging and complicated skill of constructing your own server on a remote computer.

#### In the Cloud

You may have already heard people talk about deploying apps to the cloud. What this means is setting up your application on a remote machine that can be accessed by browsers sending requests to your server.

There are many web server hosting choices. We will be using Amazon Web Services (AWS). Amazon has servers all over the world consisting of many powerful computers. These computers are connected to the internet, allowing us to rent out a small piece of that server for our use. The piece of a server we are given is very much like the computer you are currently using, but without a screen, keyboard or user interface. In order to access it, we will use a secure shell via the command line to open a window into our remote computer. We will then install everything we need to build and run our app. You'll learn more about that process in the following tabs.

When we deploy, we are setting up a web server on the AWS computer and connecting it to our application. When a client makes a request to our IP address, it is received by the web server. We are using an open source web server called  **NGINX**. NGINX is used for things like web serving, caching and load balancing. Next, NGINX needs to be able to talk to our application. This is where a  **WSGI**  (Web Server Gateway Interface) comes in. WSGI is what Python web apps use to connect to the web server (NGINX). We are using a certain implementation of a WSGI called  **Gunicorn**  (or Green Unicorn). When we set up Gunicorn, we create a .sock file. That .sock file is a UNIX domain socket that plugs Gunicorn into our app and NGINX. Three instances of these application/web server connections will be implemented to handle heavier traffic. With our application plugged into our web server, we are able to handle requests from the client.

In the video below, Greg says that the app being deployed is a Django app, but it could also be a Flask app!

Now that you've had a brief introduction to our goal and the technologies that we will be using, let's also talk about how we are going to access our server so that we can configure it.

# Deployment Basics

## Objectives:

-   Understand the steps required to deploy a Python project

----------

##### Your Server

We are using Amazon Web services to deploy our Python project. That means we have an Ubuntu server, a Linux operating system! However, it does not have anything else. Think back to how we had to do a number of installations on our own computers before we could start building Python projects. We will need to do the same for our Ubuntu server. But how do we get to it?

`Keep your PEM key secure, DO NOT push your PEM key to Github!`

The  **PEM key**  we download when we create our server instance is what gives us permission to  **SSH**  (Secure Shell) into our server. Never put your PEM key on GitHub or in any other way share your PEM key. Keep it in a directory that you know you will never have any chance of accidentally pushing to GitHub or otherwise sharing with anyone. If someone gets your PEM key, they may SSH into your server, do whatever they'd like, and run up your bill!

When we SSH into our server, we create a pipe between our computer and our server. We will have a terminal window that is actually a window into our terminal. Keep in mind that this window is no longer your own computer! We are now on our Ubuntu server, and we need to do the same installations as we did on our own computer so that we may run our Python project. For now, we will only interact with our Ubuntu server through this terminal window. We will not be able to use VSCode or MySQLWorkbench or any other GUI.

##### Your Code

When our Ubuntu server has everything it needs to run our Python project, we need to put our code in our server! To do this, we will use GitHub. We push our code from our computer onto GitHub, then pull the code from GitHub into our Ubuntu server.

##### Deploy!

Once our Ubuntu server has everything it needs, we'll set up Nginx and Gunicorn. Follow all the steps very closely and think about what each command is for!
