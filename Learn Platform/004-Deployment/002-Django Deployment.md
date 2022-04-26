# Servers

## Objectives:

-   Understand what a server is

----------

We just learned a little bit about what a server is, including the idea that a server is simply a computer like the one you're using now. Your computer, however, is designed to be able to handle many things, from graphics rendering to storage, video playback and much more. On the other hand, a server's sole purpose is to handle requests and send back some sort of response. In order to do so, a server is designed with much more processing speed, storage, and RAM.

If you visit  [www.codingdojo.com](http://www.codingdojo.com/), your computer will make a request to Coding Dojo's server. Once your request reaches the server, the server will respond by sending back files that can be interpreted by your browser. You may remember the types of files that can be interpreted by any modern browser: HTML, CSS and JavaScript. In addition, of course, browsers can display images, audio files, and video.

### Web Server Components

Let's look more closely at what's happening on the server side when the client makes a request.

1.  **Web Server**  - The web server receives a request from the client. The webserver asks the logic unit to retrieve some content.
2.  **Application**  - The logic unit receives requests from the web server. Its job is to run appropriate segments of your code according to the request's instructions. If that code requires information from the database, the logic unit will retrieve that data before organizing it and sending back a response to the web server.
3.  **Database**  - The Database is simply a file or a container for document storage like your computer's hard-drive. Its sole purpose is to store files, update files, and retrieve files according to instructions received from the interpreter.

Now that we understand what a web server does, let's build one!

# Process Managers

## Objectives:

-   Understand what a process manager is
-   Learn about Green Unicorn as a process manager

----------

In general, the process manager performs the following roles:

1.  Restarts the app automatically if it crashes
2.  Gains insights into runtime performance and resource consumption
3.  Modifies settings dynamically to improve performance
4.  Load Balancing

Green Unicorn, AKA Gunicorn, performs these roles by acting as an intermediary between incoming requests and your Django app. While you were testing your app on your local machine, it was ok to use Django’s built-in, light-weight testing server, but that server wasn’t designed to be used in a deployment environment.

Gunicorn, on the other hand, is designed to handle incoming requests that will need to be routed to the interpreter. This includes any route you've added to urls.py. We'll learn more about our other server, Nginx, which will be serving static files such as images.

Gunicorn needs a way to communicate with our app. When creating a new Django project you may have noticed that a document called  `wsgi.py`  is automatically generated. What you need to know is that your  `wsgi.py`  file is the glue that connects the Gunicorn server to your Django app. It’s how Gunicorn knows where to look for all that good code you wrote!

**Note:**  How WSGI works, what it is, and why it’s needed is a bit outside our scope here. In order to truly understand what WSGI does, you’ll need to dig into some more complex topics. To try to explain it briefly here would be a disservice. As always, when you read about or hear of something new, be curious. Go out there and learn more. A good place to start is by reading the  [Python docs on the topic](https://www.python.org/dev/peps/pep-3333/).

Chances are that when you deploy an app you’ve been developing in a local environment, you need to use some kind of process manager, regardless of the technology stack. Some common combinations include Unicorn for Rails, pm2 for NodeJS, and Apache for PHP.

There are three basic functions you will need to set up when you add Gunicorn to your project. To add this functionality, Gunicorn needs some instructions on how to do the following:

-   Which socket to connect to
-   What to do if a process fails
-   How many workers to set up

Armed with these instructions, Gunicorn takes over the job of ensuring that your app keeps running if an error occurs, directing traffic to the appropriate port, and running concurrent processes. In short, Gunicorn makes sure your deployment server runs more smoothly.

# Setup

## Objectives

-   Get our local Python project ready for deployment

----------

Before we create our server we have to do some setup first. Choose a Django project with a database and let's get started!

When we are finished, our virtual machine will be set up to serve any Django project. This will enable you to make an easy swap with a new project (like your belt). We'll show you how later.

In this first section, we will be navigating around on our local machine. If you are using Unix (Mac), or Linux, these commands should look familiar to you.  **If you are on Windows, you will want to use git bash (i.e. _not command prompt_) for the purposes of deployment.** These commands will also work in git bash.

1.  Make sure the appropriate virtual environment is activated.
2.  Once the virtual environment is activated, navigate into the correct project directory (same level as manage.py). We need to take a snapshot of all the installed pip modules into a .txt file. We'll use this file to install all of the required pip modules on our remote machine with a single command.
    ```
    (djangoPy3Env) project_name$ pip freeze > requirements.txt
    ```
3.  Open the requirements.txt file and, if they exist, remove pygraphviz, pydot and anything with MySQL in it. These modules can be tricky to install and require additional installations, so we remove them now to prevent problems later.
4.  Time to make a  **git repo**! Make sure you're in the project directory (the same level as  `manage.py`). First, let's create a  `[.gitignore](https://git-scm.com/docs/gitignore)`  file.
    ```
    (djangoPy3Env) project_name$ touch .gitignore
    ```
    As the name implies, your gitignore file tells git to ignore any files, directories, etc. you include in the file.
    
5.  Open your  `.gitignore`  file in your text editor and add these lines:
    
    #### project_name/.gitignore
    ```
    .vscode
    env/
    venv/
    __pycache__/
    .vscode/
    db.sqlite3
    ```
6.  Now initialize a git repository:
    ```py
    (djangoPy3Env) project_name$ git init
    (djangoPy3Env) project_name$ git add --all
    (djangoPy3Env) project_name$ git commit -m "initial commit"
    ```
7.  Create a new  _GitHub_  repo  [on GitHub](https://github.com/new). Copy the url of the new repository.
8.  In the terminal, run the commands (GitHub also provides these instructions upon repo creation):
    ```py
    (djangoPy3Env) project_name$ git remote add origin https://github.com/your_github_username/your_github_repo_name
    (djangoPy3Env) project_name$ git push origin master
    ```

# EC2 | Intro

## Objectives:

-   Rent space from Amazon Web Services (AWS)
-   Create an EC2 instance on AWS

----------

While there are many services out there that help with application deployment, we'll be using Amazon EC2. This service provides easily scalable servers and storage space in the cloud that makes deployment easy. Also, the lowest-tier servers are free. We are going to be renting some space on a computer owned by Amazon.

We have been using our own computer, localhost, to host our applications for us. Our computer was not designed to be a server, it was designed to be a client. Amazon has some powerful computers that can run multiple high traffic applications so we will be renting a small corner of a very large and powerful server computer.

Before we get started, make sure you have signed up for AWS Free Tier  [here](http://aws.amazon.com/free/). AWS requires you to provide a credit card during sign up, but don't worry; AWS will only charge you if you purchase non-free services. AWS will not charge you upon signing up. (In this chapter, we will demonstrate how to run a free instance. Amazon EC2 offers up to 1 year of free use so that programmers like us can enjoy the free service.)

1.  Log in to the AWS console at  [https://aws.amazon.com/](https://aws.amazon.com/)
2.  Once you have logged in, click on  _Services_  and click on  _EC2_.
    
	<img src="https://i.ibb.co/YpSBg3t/chapter3227-7755-2-ec2.png" border="0">
    
3.  Launch a new instance from the EC2 Dashboard by clicking  _Launch Instance_  as shown below.
    
    <img src="https://i.ibb.co/gFnYdkZ/chapter3227-7756-3-launch-instance.png" border="0">
    
4.  Select  **_Ubuntu Server 18.04, SSD Volume Type_**  option. Do NOT select Ubuntu 16.04
    
    <img src="https://i.ibb.co/2d05QCm/Screen-Shot-2019-07-16-at-3-00-58-PM.png"  border="0">
    
5.  Select the  _t2.micro_  option and click  _Review and Launch_.
    
    <img src="https://i.ibb.co/rxY5BY9/chapter3227-7758-5-review-launch.png" border="0">
    
6.  Click the  _Edit security groups_  link in the lower right corner.
    
    <img src="https://i.ibb.co/qpKwQsH/chapter3227-7759-6-edit-sec-groups.png" border="0">
    
7.  SSH option should be there already. Update its source to  _MyIP_. Click the add a rule button and add HTTP and HTTPS, set source to  _Anywhere_, and then click  _Review and Launch_.
    
    <img src="https://i.ibb.co/4TW5dL5/chapter3227-7761-8-completed-rules.png" border="0">
    
    (If you plan on reconnecting to this instance from a different location, see the  _Reconnecting_  module at the end of this chapter.)
    
8.  Next, you'll be asked to create a key file. This is what will let us connect and control the server from our local machine.
    
    Name your pem key whatever makes the most sense to you as shown in the next step. Give it a generic name, not the name of your project, as we can reuse this key.
    
    <img src="https://i.ibb.co/rtBSqwn/chapter3227-7762-9-download-pem.png" border="0">
    
9.  Click  _Download Key Pair_. The key will automatically be saved wherever your browser saves by default. This next part is very important! Put your pem key in a file that has no chance of  **_EVER_**  being pushed to GitHub or anywhere public. You should not send this file via email, or in any other way make it publicly available:
    
    <img src="https://i.ibb.co/bb8Szbb/chapter3227-7754-1-pem-key-folder-path.png" border="0">
    
10.  After launching your instance, you will see a screen with lots of information. Scroll to the bottom of the page and click  _View Instances_.
    
	   <img src="https://i.ibb.co/FJN9LXF/chapter3227-7763-10-view-instance.png" border="0">
    
11.  (Optional) Once you have several instances running, you will want to be able to identify what your different instances are for. We have the option of naming our instance, so let’s do so now by clicking on our instance’s name column as shown.
    
	   <img src="https://i.ibb.co/R96PmrT/chapter3227-7764-11-name-instance.png" alt="chapter3227-7764-11-name-instance" border="0">

# Server Access

## Objectives

-   Connect to our AWS server instance!

----------

1.  Back in your terminal, navigate to the folder that holds the pem key file you just downloaded. Now we’re ready to use our .pem file to connect to the AWS instance!

-   **Windows users:**  you cannot use the command prompt for this. Use git bash or another terminal that allows for ssh.

3.  In your AWS console, click  _Connect_  at the top of your screen and use the supplied code in your terminal (PC users: use a bash terminal to do this).
    
    <img src="https://i.ibb.co/G7SQSzx/chapter3227-7765-12-connect.png" border="0">
    
4.  A popup will appear with instructions on how to connect. Copy the two commands, highlighted in the red boxes, and paste them in your terminal.
    
    <img src="https://i.ibb.co/T0YwFMH/chapter3227-7766-13-connect-pop.png" border="0">
    
    ```py
    the_folder_containing_your_pem_file$ chmod 400 your_pem_name.pem
    the_folder_containing_your_pem_file$ ssh -i "your_pem_name.pem" ubuntu@your_instance_address_here
    ```
    
5.  You will likely be prompted to continue. Type  `yes`  and wait for a few seconds. If all goes well, you should be on your Ubuntu cloud server. Your terminal should show something like this in the far left of your prompt, signaling you are now logged into your AWS instance! We are no longer affecting our own computer--we are now remotely logged into the server we are renting from Amazon!
    ```py
    ubuntu@54.162.31.253:~$ #Commands you write appear here
    ```

## Server Configuration

## Objectives:

-   Install the necessary programs on our AWS instance

  

1.  Now we are going to set up our remote server for deployment. Our server is nothing more than a small allocated space on someone else’s larger computer (in this case, the big computer belongs to Amazon!). That space has an installed operating system, just like your computer. In this case, we are using a distribution of Linux called Ubuntu, version 18.04.
2.  Although we have linux, our new computer is otherwise empty. Let’s change that so we can start building a server capable of providing content that the rest of the world can access. Let's check for updates first.
    ```py
    ubuntu@54.162.31.253:~$ sudo apt-get update
    ```
3.  Now let's install nginx
    ```py
    ubuntu@54.162.31.253:~$ sudo apt-get install nginx
    ```
4.  Let's make a clone of our git repository on this machine. (NO SUDO!)
    ```py
    ubuntu@54.162.31.253:~$ git clone https://github.com/your_username_here/your_repo_name_here
    ```
5.  Let's now install venv so we can create a virtual environment.
    ```py
    ubuntu@54.162.31.253:~$ sudo apt-get install python3-venv //Say YES when prompted
    ```
6.  Navigate to your repository folder
    ```py
    ubuntu@54.162.31.253:~$ cd {{ repo name }}
    ```
7.  Now let's create a virtual environment and activate it.
    ```py
    ubuntu@54.162.31.253:~/myRepoName$ python3 -m venv venv //We are using the venv command and naming our virtual env venv
    ubuntu@54.162.31.253:~/myRepoName$ source venv/bin/activate
    ```
8.  Let's now install the dependencies that we will need in our virtual environment.
    
9.  ```py
    (venv) ubuntu@54.162.31.253:~/myRepoName$ pip install django==2.2
    (venv) ubuntu@54.162.31.253:~/myRepoName$ pip install bcrypt
    (venv) ubuntu@54.162.31.253:~/myRepoName$ pip install gunicorn
    ```

# VIM

## Objectives:

-   Learn about VIM, a text editor for Unix
-   Learn a few basic commands for VIM

----------

If you have used VIM before, skip to the next tab.

VIM is a terminal based file editor. We will use it to change the necessary files in order to get our project running. In the following instructions, you'll be using the  `vim`  command to enter the editor. The  `vim`  command can be used either to:

-   edit existing files, or
-   create and open a new blank file.

Because there is no GUI (graphical user interface), it's important to learn a few keyboard commands for navigating around VIM:

-   `**i**`  - enter INSERT mode. You should see  `**–INSERT–**`  at the bottom left corner of your terminal. Now use your arrow keys to move the cursor to where you want to edit and make your changes.
-   `**esc**`  - exit INSERT mode.
-   `**:**`  - when not in INSERT mode, enters the vim command interface. You should now see a colon at the bottom left corner of your terminal.

-   `**w**`  and  `**Enter**`  - save.
-   `**wq**`  and  `**Enter**`  - save and quit.
-   `**q!**`  and  `**Enter**`  - quit without saving.

# Modifying Settings

## Objectives:

-   Update our deployed settings.py file

----------

#### IMPORTANT

#### Anywhere you see {{myRepoName}} – replace that whole thing INCLUDING the {{}} with your outer folder name (same as GitHub repository name).

#### Anywhere you see {{projectName}} – replace that whole thing INCLUDING the {{}} with the project folder name (the name of your Django project).

#### Anywhere you see {{yourEC2.public.ip}} – replace that whole thing INCLUDING the {{}} with the public IP address of your newly created server.

----------

If you named your repo something different from your project, the repo name and project name may be different, but it is okay if they are the same.

1.  Navigate into your main project directory, where  `settings.py`  lives.
    ```py
    (venv) ubuntu@54.162.31.253:~/myRepoName$ cd {{projectName}}
    ```
2.  We're going to use a built-in text editor (VIM) in the terminal to update the code in  `settings.py`.
    ```py
    (venv) ubuntu@54.162.31.253:~/myRepoName/projectName$ sudo vim settings.py
    ```
3.  You'll need to add a line that allows you to serve static content. You'll also need to modify a couple of lines, as follows. Don't forget to type  `i`  to enter insert mode.
    ```
    # inside settings.py
    # modify these lines
    DEBUG = False
    ALLOWED_HOSTS = ['{{yourEC2.public.ip}}']	# keep the quotes!
    STATIC_ROOT = os.path.join(BASE_DIR, "static/")	# add this line at the bottom; don't replace any existing lines!
    ```
    Save and quit. (`esc`,  `:wq`,  `enter`)  
    
4.  Navigate back to the folder that holds  `manage.py`. Make sure your virtual environment is still activated!
    ```py
    (venv) ubuntu@54.162.31.253:~/myRepoName/projectName$ cd ..
    ```
5.  Gather all of the static files in your project into one location:
    ```py
    (venv) ubuntu@54.162.31.253:~myRepoName$ python manage.py collectstatic	# type yes when prompted
    ```
6.  If you ignored your db and/or migrations files, this is a great time to also make and run migrations, just as you would have done on your local machine!
    ```py
    (venv) ubuntu@54.162.31.253:~myRepoName$ python manage.py makemigrations
    (venv) ubuntu@54.162.31.253:~myRepoName$ python manage.py migrate
    ```
# Gunicorn

## Objectives:

-   Set up gunicorn

----------

You may remember that Gunicorn is our process manager. Let's get it set up.

1.  Let's first test Gunicorn by directing it to our Django project's wsgi.py file, which is the entry point to our application.
    ```py
    (venv) ubuntu@54.162.31.253:~myRepoName$ gunicorn {{project_name}}.wsgi
    ```
    If your Gunicorn process ran correctly, you will see something like the following printed to the terminal:
    ```
    [2016-12-27 05:45:56 +0000] [8695] [INFO] Starting gunicorn 19.6.0
    [2016-12-27 05:45:56 +0000] [8695] [INFO] Listening at: http://0.0.0.0:8000 (8695)
    [2016-12-27 05:45:56 +0000] [8695] [INFO] Using worker: sync
    [2016-12-27 05:45:56 +0000] [8700] [INFO] Booting worker with pid: 8700
    ```
    Exit the process by typing  `ctrl-c`.
    
    Deactivate the virtual env by typing  `deactivate`
    
2.  Now we're going to set up Gunicorn to run as a service. You'll be using  _systemd_  as your init system to manage and control aspects of your server including services. The primary advantage of turning Gunicorn into a service is that Gunicorn will start with the server after being rebooted and once configured will just work. To be able to turn Gunicorn on and off, we're going to create a  _systemd_  service file and make some changes.
    ```py
    ubuntu@54.162.31.253:~myRepoName$ sudo vim /etc/systemd/system/gunicorn.service
    ```
3.  In the VIM text editor, copy and paste the following code. Don't forget to type  `i`  before copying and pasting the lines below!
    ```
    [Unit]
    Description=gunicorn daemon
    After=network.target
    [Service]
    User=ubuntu
    Group=www-data
    WorkingDirectory=/home/ubuntu/{{myRepoName}}
    ExecStart=/home/ubuntu/{{myRepoName}}/venv/bin/gunicorn --workers 3 --bind unix:/home/ubuntu/{{myRepoName}}/{{projectName}}.sock {{projectName}}.wsgi:application
    [Install]
    WantedBy=multi-user.target
    ```
4.  Now that our service file has been created, we can enable it so it starts on boot.
    ```py
    ubuntu@54.162.31.253:~$ sudo systemctl daemon-reload	# systemctl ends with the letter L, not a number
    ubuntu@54.162.31.253:~$ sudo systemctl restart gunicorn
    ubuntu@54.162.31.253:~$ sudo systemctl status gunicorn
    ```
    You should see a green dot next to gunicorn.service and the lines "Booting worker with pid: ....". It should look like this;  
    
      
    
    <img src="https://i.ibb.co/dGkBd3Z/Screen-Shot-2019-07-16-at-4-37-20-PM.png" border="0">
    
      
    
    _Note:_  if any additional changes are made to the gunicorn.service the previous three commands will need to be run in order to sync things up and restart our service.
    
5.  CHECK: Type  `ls`. If you DO NOT see a {{projectName}}.sock file, double and triple check the file from above (case sensitivity, appropriate spacing, spelling, etc.).

## Troubleshooting Steps and Common Errors:

If you see output that looks like this when you start your gunicorn service:

<img src="https://i.ibb.co/3dJdMnj/Screen-Shot-2019-07-16-at-4-40-36-PM.png" border="0">

It is likely that you cloned your repository with sudo or created your virtualenv with sudo. If that is the case, terminate your EC2 instance and start over.

  

If you see output that looks like this:

<img src="https://i.ibb.co/hgKMLRt/Screen-Shot-2019-07-16-at-4-40-48-PM.png" border="0">

Read the error message it gives you. This will often be a typo in one of your configuration files. Another common error is not installing Gunicorn and Django in the same environment. Go over the steps again until you see the green dot output.

# Nginx

## Objectives:

-   Set up NGINX

----------

1.  We now need to create a new file to configure NGINX, our web server.
    ```py
    ubuntu@54.162.31.253:~$ sudo vim /etc/nginx/sites-available/{{projectName}}
    ```
2.  Add the following to this new document, editing what's inside curly braces {{}}. Don't forget to type  `i`  to enter insert mode.
    ```
    server {
      listen 80;
      server_name {{yourEC2.public.ip}};
      location = /favicon.ico { access_log off; log_not_found off; }
      location /static/ {
          root /home/ubuntu/{{myRepoName}};
      }
      location / {
          include proxy_params;
          proxy_pass http://unix:/home/ubuntu/{{myRepoName}}/{{projectName}}.sock;
      }
    }
    ```
3.  Save and exit. (`esc`,  `:wq`,  `enter`)
4.  Now we're going to create a link to this file to let NGINX know what settings to use. Run the following (taking note of the space after {{projectName}}):
    ```py
    ubuntu@54.162.31.253:~$ sudo ln -s /etc/nginx/sites-available/{{projectName}} /etc/nginx/sites-enabled
    ```
5.  CHECK: Make sure the link was successful. If not successful, double and triple check the file we just created.
    ```py
    ubuntu@54.162.31.253:~$ sudo nginx -t
    ```
6.  Now that we have our custom configuration, we will remove the Nginx default site.
    ```py
    ubuntu@54.162.31.253:~$ sudo rm /etc/nginx/sites-enabled/default
    ```
7.  All that is left to do is restart our NGINX server with our updated settings.
    ```py
    ubuntu@54.162.31.253:~$ sudo service nginx restart
    ```

# Wrapping Up

## Objectives:

-   Test out our deployed server!
-   Highlight common errors

----------

If you don't see any errors from the last step, drumroll...go to your URL! You are on the internet--amazing!!

## Common errors and where to start debugging:

-   502, bad gateway: there is a problem in your code. Hint: any error starting with 5 indicates a server error
-   Your Gunicorn process won’t start: Check your .service file; typos and wrong file paths are common mistakes
-   Your NGINX restart fails: Check your NGINX file in the sites-available directory. Common problems include typos and forgetting to insert your project name where indicated.
-   Make sure the URL requested is correct (example if your root route is /home, make sure you put /home after the IP)

# Adding a MySQL Server (optional)

## Objectives:

-   Learn how to use a MySQL server (vs. SQLite) as the database server

----------

SQLite is great for testing, but it's not really efficient in the context of real-world use. This may be a bit too much to go into here, but let’s look at a quick summary of why that is, and what we’ll use instead.

Although the developers of SQLite have done much to improve its performance, particularly in version 3, it suffers from some lack of efficient write concurrency. If your site has a lot of traffic, a queue begins to form, waiting for write access to the database. Before long, your response speed will slow to a crawl. This happens only on high-traffic sites, however.

MySQL databases, on the other hand, are incredibly fast, and very good at performing multiple operations concurrently. In addition, MySQL can store an incredibly large amount of data, and thus scales well.

This might never be a consideration for small to medium sized projects, but is key information in the real world. Very soon you may be working for a company that handles a large volume of requests, and it is important to know why depending on a SQLite database alone is not a practical solution for enterprise or large startups.

If you’d like to learn how to add a MySQL database to the app we just deployed, read on. It’s not as hard as you might think, thanks to Django migrations!

1.  First, we’ll need to install everything necessary to run MySQL from our deployment machine.
    ```py
    ubuntu@54.162.31.253:~$ sudo apt-get install libmysqlclient-dev -y
    ```
2.  Next we'll need to install MySQL-server
    ```py
    ubuntu@54.162.31.253:~$ sudo apt-get install mysql-server -y
    ```
    **IMPORTANT: When prompted with the purple screen, don't just hit enter! Enter a password for this server. We recommend using  `root`  for now. You'll have to type it twice.**
    
3.  CHECK: Make sure it installed correctly.
    ```py
    ubuntu@54.162.31.253:~$ mysql -u root -p
    ```
    Enter the password you just set. You should now be in the MySQL server prompt:
    ```py
    mysql>
    ```
4.  We're now going to create the database for our project. You can call it whatever you want but we recommend giving it the name of your project.
    ```py
    mysql> CREATE DATABASE {{projectName}};
    ```
    **Don't forget semicolons at the end of each line. If you just keep getting the  `->`  after hitting enter, type a  `;`  and press enter.**
    
5.  Exit the MySQL prompt.
    ```py
    mysql> exit
    ```
6.  Activate your virtual environment:
    ```py
    ubuntu@54.162.31.253:~myRepoName$ source venv/bin/activate
    ```
7.  Install a pip module inside our virtual environment to help connect our python code to our MySQL database:
    ```py
    (venv) ubuntu@54.162.31.253:~myRepoName$ pip install mysqlclient
    ```
8.  Now that we have MySQL all set up, we are ready to change some lines in our  `settings.py`  document so we can start working with our MySQL database! Navigate to the appropriate folder and open it with VIM.
    ```py
    ubuntu@54.162.31.253:~myRepoName/projectName$ sudo vim settings.py
    ```
9.  Change the databases section in settings.py to look like below. Note: The schema name is the database we just created in step , and the password is the password we set up when we installed the MySQL server in step .
    ```
    DATABASES = {
      'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '{{schemaName}}',
        'USER': 'root',
        'PASSWORD': '{{password}}',
        'HOST': 'localhost',
        'PORT': '3306',
        }
    }
    ```
10.  Save and quit
11.  We’re almost done! Now the only thing left to do is to make migrations!
    ```py
    (venv) ubuntu@54.162.31.253:~myRepoName$ cd ..
    (venv) ubuntu@54.162.31.253:~myRepoName$ python manage.py makemigrations
    (venv) ubuntu@54.162.31.253:~myRepoName$ python manage.py migrate
    ```
12.  Now just need to restart Gunicorn:
    ```py
    (venv) ubuntu@54.162.31.253:~myRepoName$ sudo systemctl restart gunicorn
    ```
13.  CHECK: Now visit your site! You should be finished at this point, with a fully functioning site. Since we just created a brand new database, you obviously won't have any data yet, but share your site with your family and friends and you'll have lots of data in no time!

# Reconnecting

## Objectives:

-   Learn how to reconnect after initial deployment

----------

Remember how we said that we would have to change our security settings every time our IP changes? The bad news is that this will happen often. The good news is that it's easy to change those settings, if you know where to look.

1.  In your AWS console, with your instance selected, scroll down to view some options. Next to security groups, you will see launch-wizard. Click it!  
    <img src="https://i.ibb.co/5Mqr4N6/chapter3227-7767-14-security-groups.png" border="0">
2.  Now you just have to update the IP connected to the instance. In the next window you will see something like this at the bottom of your screen. Click the inbound tab, and then select edit.  
    <img src="https://i.ibb.co/Zm292nX/chapter3227-7768-15-edit-groups.png" border="0">
3.  Now, all that is left to do is let AWS automatically change our IP to the new one. Do this by selecting the dropdown in the SSH row, under source, and select MyIP (it is already selected, but doing so again will refresh your IP to the current on). Once this is done, click save. You’re ready to SSH into your instance again!  
    <img src="https://i.ibb.co/tDz1yjQ/chapter3227-7769-16-update-security-groups.png" border="0">
