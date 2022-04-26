# (optional) Flask Deployment

  

Follow all the same steps up through Server Access. When you get to Server Configuration, STOP and continue from here.

## Server access:

Now we are going to set up our remote server for deployment. Our server is nothing more than a small allocated space on someone else’s larger computer (in this case, the big computer belongs to Amazon!). That space has an installed operating system, just like your computer. In this case, we are using a distribution of Linux called Ubuntu, version 16.04.

## Create a user:

We should have a non-root user who also has root privileges. Let's create one now! In the example, our user will be named "kermit", but you may use whatever name you like.
```
sudo adduser kermit              // This will ask you to create a password. Make it secure!
                                 // You may then fill in your information, or press <enter> for default
sudo usermod -aG sudo kermit     // this will give the user root privileges
su - kermit                      // switch to the user kermit, your terminal prompt will indicate the change
```
## Server configuration:

Although we have linux, our new computer is otherwise empty. Let’s change that so we can start building a server capable of providing content that the rest of the world can access. In order to do so, we have to install some key programs first. First, let’s install python, python dev, pip, nginx, and git

In the terminal:
```
sudo apt-get update
sudo apt-get install python3-pip python3-dev nginx git    // answer Yes when prompted!
sudo apt-get update
sudo pip3 install virtualenv
```
## mySQL

Next, we will need to install our mySQL server:
```
sudo apt-get update
sudo apt-get install mysql-server                      // answer Yes when prompted!
```
A pop up will ask you to set your password. Type it in carefully! If you make it different from the password you use on your local machine, remember that you will have to update your mysqlconnection file in your Flask project.

Next, we will need to set up the database that our project will need. This can easily be done by going to MySQL Workbench and reverse engineering your desired database, then forward engineering it.

**1. Reverse engineer**

<img src="https://i.ibb.co/QDWRR5M/Screen-Shot-2018-07-18-at-6-29-42-PM.png" border="0">

**2. Forward engineer**

We may filter out tables that we do not want forward engineered. Here, we are only going to process the tables in the simpleWall database. We excluded the tables from the emailVal and register databases by selecting them and clicking the right arrow.

<img src="https://i.ibb.co/jRSzwJP/Screen-Shot-2018-07-18-at-6-31-25-PM.png" border="0">  

**3. Copy the script**

When MySQL Workbench asks you to review the script, that's when you can copy it!

<img src="https://i.ibb.co/4237xdN/Screen-Shot-2018-07-18-at-6-32-04-PM.png" border="0">

  

Now, in our deployed server, we can open the mysql shell by typing:
```py
mysql -u root -p                                       // provide your mysql password when prompted
```
This is where you may run SQL queries! Including the code that will create your database for you! Just paste the script that you copied from MySQL Workbench, and it will create your database. You may verify that the database was created with:
```py
SHOW DATABASES;
```
When you are ready to leave the mysql shell, type:
```py
exit
```
## Get your project!

Now, we are going to clone our project that we want to deploy into our server and cd into it.
```py
git clone {{ url copied from github project }}
cd {{ project }}
```
Make sure your project looks exactly like you remember it, and now let's make a virtual environment. The  `~/myRepoName$` prompt in the code snippets provided is to ensure that you know that you should be in your project when running these commands.

## Virtualenv
```py
~/myRepoName$ virtualenv venv --python=python3            // create the environment and call it venv
~/myRepoName$ source venv/bin/activate                    // activate the environment
(venv) ~/myRepoName$ pip install -r requirements.txt      // install everything that requirements.txt says you need
(venv) ~/myRepoName$ pip install gunicorn                 // install gunicorn
```
## Gunicorn

Now, we need a wsgi.py file, which will help Gunicorn, our process manager, know how to interact with the application. We will use vim as our text editor to make our files. You may refer to the VIM module above if you are unfamiliar with using vim.
```py
(venv) ~/myRepoName$ vim wsgi.py                     // this will open the new, empty file for us
// to use vim, press i to enter insert mode, which allows you to type
// press [esc] when you are done typing
// type :wq to save and quit vim
// type :q if you want to quit vim without saving
```
We will need the following code in our wsgi.py file (this assumes that you named your server file server.py, if you named it something different you will have to put that name in place of  `server`  in the code below):
```py
from server import app as application
if __name__ == "__main__":
    application.run()
```
Now, we need to direct Gunicorn to our project's wsgi.py file, which is the entry point to our application.  
```py
(venv) ~/myRepoName$ gunicorn --bind 0.0.0.0:5000 wsgi:application
```
If your Gunicorn process ran correctly, you will see something like the following printed to the terminal:
```py
[2016-12-27 05:45:56 +0000] [8695] [INFO] Starting gunicorn 19.6.0
[2016-12-27 05:45:56 +0000] [8695] [INFO] Listening at: http://0.0.0.0:5000 (8695)
[2016-12-27 05:45:56 +0000] [8695] [INFO] Using worker: sync
[2016-12-27 05:45:56 +0000] [8700] [INFO] Booting worker with pid: 8700
```
If you have any error messages, read them carefully - you may need to install anything that was not already included in your requirements.txt file. Run the command again, reading your error messages, until you get the output you see above.

If that looks good, you may shut it down with ctrl + C, because we're still not done!  

Deactivate the virtual environment with:
```py
(venv) ~/myRepoName$ deactivate
```
Now, we need a systemd service unit file. This will automatically start Gunicorn when the server boots.
```py
sudo vim /etc/systemd/system/{{project}}.service
```
In this file you just created, we will need the following (everywhere where you see  `username`, replace that with the username you created for your server):
```
[Unit]
Description=Gunicorn instance to serve {{project}}
After=network.target
[Service]
User={{username}}
Group=www-data
WorkingDirectory=/home/{{username}}/{{repo name}}
Environment="PATH=/home/{{username}}/{{repo name}}/venv/bin"
ExecStart=/home/{{username}}/{{repo name}}/venv/bin/gunicorn --workers 3 --bind unix:{{project}}.sock -m 007 wsgi:application
[Install]
WantedBy=multi-user.target
```
After we create this file, we need to enable it, so that it starts when the server boots:
```py
sudo systemctl start {{project}}
sudo systemctl enable {{project}}
```
After running these lines, you should see your {{project}}.sock file in your project, on the same level as server.py. If not, you probably have a typo in the systemd service unit file.

## nginx

Now, we just need to configure nginx to handle requests made by the server. Let's create a new file in sites-available.
```py
sudo vim /etc/nginx/sites-available/{{project}}
```
In this file, we will need the following:
```
server {
    listen 80;
    server_name {{your public ip}};
    location / {
        include proxy_params;
        proxy_pass http://unix:/home/{{username}}/{{repo name}}/{{project}}.sock;
    }
}
```
Now, we need to link this nginx configuration to our sites-enabled directory.
```py
sudo ln -s /etc/nginx/sites-available/{{project}} /etc/nginx/sites-enabled
```
Test nginx for errors:
```py
sudo nginx -t
```
If we get a message saying that everything is (syntactically) ok, then we can remove the nginx default site display from directory sites-enabled and restart nginx with its new configuration:
```py
sudo rm /etc/nginx/sites-enabled/default
sudo systemctl restart nginx
```
Now, we should be able to navigate to your public ip and see your project!

To close the pipe to your deployed server, type:
```py
exit
```

# Servers

### What is a server?

We just learned a little bit about what a server is, including the idea that a server is simply a computer like the one you're using now. Your computer, however, is designed to be able to handle many things, from graphics rendering to storage, video playback and much more. On the other hand, a server's sole purpose is to handle requests and send back some sort of response. In order to do so, a server is designed with much more processing speed, storage, and RAM.

If you visit  [www.codingdojo.com](http://www.codingdojo.com/)  your computer will make a request to Coding Dojo's server. Once your request reaches the server, the server will respond by sending back files that can be interpreted by your browser. You may remember the types of files that can be interpreted by any modern browser: HTML, CSS and JavaScript. In addition, of course, browsers can display images, audio files, and video.

### Web Server Components

Let's look more closely at what's happening on the server side when the client makes a request.

1.  **Web Server**  - The web server receives a request from the client. The webserver asks the logic unit to retrieve some content.
2.  **Application**  - The logic unit receives requests from the web server. Its job is to run appropriate segments of your code according to the request's instructions. If that code requires information from the database, the logic unit will retrieve that data before organizing it and sending back a response to the web server.
3.  **Database**  - The Database is simply a file or a container for document storage like your computer's hard-drive. Its sole purpose is to store files, update files, and retrieve files according to instructions received from the interpreter.

Now that we understand what a web server does, let's build one!


## The Process Manager: Green Unicorn

In general, the process manager performs the following roles:

1.  Restart the app automatically if it crashes.
2.  Gain insights into runtime performance and resource consumption.
3.  Modify settings dynamically to improve performance.
4.  Load Balancing

Green Unicorn, AKA Gunicorn, performs these roles by acting as an intermediary between incoming requests and your Flask app. While you were testing your app on your local machine, it was ok to use Flask's built-in, light-weight testing server, but that server wasn’t designed to be used in a deployment environment.

Gunicorn, on the other hand, is designed to handle incoming requests that will need to be routed to the interpreter. This includes any app route you created. We’ll learn more about our other server, Nginx, which will be serving static files such as images.

Gunicorn needs a way to communicate with our app. This is done with a `wsgi.py` file. What you need to know is that your  `wsgi.py`  file is the glue that connects the Gunicorn server to your Flask app. It’s how Gunicorn knows where to look for all that good code you wrote!

**Note:**  How WSGI works, what it is, and why it’s needed is a bit outside our scope here. In order to truly understand what WSGI does, you’ll need to dig into some more complex topics. To try to explain it briefly here would be a disservice. As always, when you read about or hear of something new, be curious. Go out there and learn more. A good place to start is by reading the  [Python docs on the topic](https://www.python.org/dev/peps/pep-3333/).

Chances are that when you deploy an app you’ve been developing in a local environment, you need to use some kind of process manager, regardless of the technology stack. Some common combinations include Unicorn for Rails, pm2 for NodeJS, and Apache for PHP.

There are three basic functions you will need to set up when you add Gunicorn to your project. To add this functionality, Gunicorn needs some instructions on how to do the following:

-   Which socket to connect to
-   What to do if a process fails
-   How many workers to set up

Armed with these instructions, Gunicorn takes over the job of ensuring that your app keeps running if an error occurs, directing traffic to the appropriate port, and running concurrent processes. In short, Gunicorn makes sure your deployment server runs more smoothly.

# Setup

Before we create our server we have to do some setup first. Let's get started!

Today you will be deploying a full stack Flask application. When you are finished, your virtual machine will be set up to serve any Flask project. This will enable you to make an easy swap with a new project, for example, your belt exam. We'll show you how later.

In this first section, you will be navigating around on your local machine. If you are using Unix (Mac), or Linux, these commands are for you. If you are on Windows, you will want to use git bash in order for these commands to run properly.

## Step 1: Getting Started

Get started by activating your project's virtual environment.

Once you have activated your virtual environment, cd into your project directory. You will now save all of your installed pip modules into a .txt file. Later, we will use this file to install all of the required pip modules on our remote machine with a single command.
```py
pip freeze > requirements.txt
```
**In your text editor, open your requirements.txt file and, if they exist, remove pygraphviz, pydot and anything with MySQL in it. These modules can be tricky to install and require additional installations, so we remove them now to prevent problems later.**

## Step 2: Committing

**Important!**

We’re about to initialize a new git repo. Your git repo must be initialized within the outer project folder. This is the same level as your  `server.py`  file. If you  `ls`  and don’t see  `server.py`, you are in the wrong place. Double check your location before you initialize your repo.

First we’ll create a  `.gitignore`  file.
```py
touch .gitignore
```
As the name implies, your gitignore file tells git to ignore any files, directories, etc. you include in the file. In this case, we’re instructing git to ignore all files with the extension “pyc”. If you placed your virtual environment in this folder, we will ignore that as well. In your gitignore file,  `venv/`  should be replaced with the name of your virtual environment.

Open your  `.gitignore`  file in your text editor and add the lines:
```py
  *.pyc
  venv/
```
We know this is familiar, but here’s a reminder of how to initialize a new repo:
```py
  > git init
  > git add --all
  > git commit -m "initial commit"
```
Create a new github repo and, back in terminal run these commands, replacing the repo url with your own.
```py
  > git remote add origin https://github.com/AnnaBNana/flask_courses.git
  > git push origin master
```
Once you login to AWS and set up a cloud server, you’ll be pulling code from your GitHub repository.


# EC2 | Intro

While there are many services out there that help with application deployment, we'll be using Amazon EC2. This service provides easily scalable servers and storage space in the cloud that makes deployment easy. Also, the lowest-tier servers are free.

## Getting Started

Before we get started, make sure you have signed up for AWS Free Tier. If you haven't, go to this link  [http://aws.amazon.com/free/](http://aws.amazon.com/free/)and sign up. AWS requires you to provide a Credit Card during sign up, but don't worry; AWS will only charge you if you purchase non-free services. AWS will not charge you upon signing up.

## Road Map

1.  #### Launch an Amazon EC2 Instance
    
    We are going to be renting some space on a computer owned by Amazon. We have been using our own computer, localhost, to host our applications for us. Our computer was not designed to be a server, it was designed to be a client. Amazon has some powerful computers that can run multiple high traffic applications so we will be renting a small corner of a very large and powerful server computer.
    
    Note: In this chapter, we will demonstrate how to run a free instance. Amazon EC2 offers up to 1 year of free use so that programmers like us can enjoy the free service.
    
2.  #### Connect to our EC2 instance
    
    Now that we've rented our server space, how do we access it? What do we mean by access? It's just like when you open up your terminal and access the files in your own computer. Fortunately, we can use our own terminal to connect to the computer that we bought. It is as if we are accessing the terminal from that computer.
    
3.  #### Installation
    
    Your EC2 instance has only the operating system installed. In order to get our project up and running we'll have to install the necessary software. We will replicate the development environment from your computer on the server so that the application will run remotely just as it does locally.
    
4.  #### Point
    
    We are going to register our domain name to point to the IP address of this computer that we bought from Amazon. Now whenever someone requests our domain name, the request will look at the address book, and know which IP address to go to.

# Step 3: Creating an EC2 server instance

> Note: You’ll need an AWS account, which you can sign up for  [here](http://aws.amazon.com/). It’s free for a year, so long as you don’t have more than 1 (free-tier) instance up at a time!

1.  Login to AWS Console at  [https://aws.amazon.com/](https://aws.amazon.com/)

----------

3.  Once you have logged in you will see your dashboard page:  
    ![dashboard ec2](https://s3.amazonaws.com/General_V88/boomyeah/company_209/chapter_3227/handouts/chapter3227_7755_2-ec2.png)

----------

5.  Launch a new instance from the EC2 Dashboard, as shown below:  
    ![launch instance](https://s3.amazonaws.com/General_V88/boomyeah/company_209/chapter_3227/handouts/chapter3227_7756_3-launch-instance.png)

----------

7.  Select  _Ubuntu Server 16.04_  option.  
    ![select server](https://s3.amazonaws.com/General_V88/boomyeah2015/codingdojo/curriculum/content/chapter/04_ubuntu_1604.png)

----------

9.  Select  _t2.micro_  option and click  _Review and Launch_  
    ![select review and launch](https://s3.amazonaws.com/General_V88/boomyeah/company_209/chapter_3227/handouts/chapter3227_7758_5-review-launch.png)

----------

### Security settings

1.  Click the  _Edit security groups_  link in the lower right corner  
    ![edit security groups](https://s3.amazonaws.com/General_V88/boomyeah/company_209/chapter_3227/handouts/chapter3227_7759_6-edit-sec-groups.png)

----------

3.  SSH option should be there already. Reset SSH source from the dropdown menu to MyIP. This is the ip address of your current location. If you go home, for example, you will have to set this again to get it to be your home ip.  
    ![edit ssh rule](https://s3.amazonaws.com/General_V88/boomyeah/company_209/chapter_3227/handouts/chapter3227_7760_7-add-rule.png)

----------

5.  Click the add a rule button twice to add HTTP and HTTPS, source set to  _Anywhere_, and then click  **_Review and Launch:_**  
    ![add http and https rules](https://s3.amazonaws.com/General_V88/boomyeah/company_209/chapter_3227/handouts/chapter3227_7761_8-completed-rules.png)

----------

7.  You’ll be asked to create a key file. This is what will let us connect and control the server from our local machine.
    
    Name your pem key whatever makes the most sense to you. The image below shows the pem key name as "django_pem", but "flask_pem" would be a smarter choice. Give it a generic name, not the name of your project, as we will be re-using this instance.
    
    The key will automatically be saved to your downloads folder when you click Download Key Pair, but you will want to move it. See the next item for more information on this critical step.  
    ![download pem key](https://s3.amazonaws.com/General_V88/boomyeah/company_209/chapter_3227/handouts/chapter3227_7762_9-download-pem.png)
    

----------

9.  This next part is very important! Put your pem key in a file that has no chance of  **_EVER_**  being pushed to github. You should not send this file via email, or in any other way make it publicly available:  
    ![choose safe location for pem key](https://s3.amazonaws.com/General_V88/boomyeah/company_209/chapter_3227/handouts/chapter3227_7754_1-pem-key-folder-path.png)
    

----------

11.  After launching your instance, you will see a rather confusing screen with some information, as shown below. In order to move on, scroll to the bottom of the page and confirm that you would like to view your instance.  
    ![click view instance at bottom of page](https://s3.amazonaws.com/General_V88/boomyeah/company_209/chapter_3227/handouts/chapter3227_7763_10-view-instance.png)
    

----------

13.  Once you have several instances running, you will want to be able to identify what your different instances are for. We have the option of naming our instance, so let’s do so now by clicking on our instance’s name column as shown.  
    ![name your instance](https://s3.amazonaws.com/General_V88/boomyeah/company_209/chapter_3227/handouts/chapter3227_7764_11-name-instance.png)

# Step 4: Connecting to your remote server

Back in your terminal, cd to the folder that holds the key file you just downloaded.

> cd /projects/AWS

Now we’re ready to use our .pem file to connect to the AWS instance! In your AWS console, click connect and use the supplied code in your terminal (PC users: use a bash terminal to do this).

Back in your AWS console click the connect button at the top of your screen here:

![connect to instance button](https://s3.amazonaws.com/General_V88/boomyeah/company_209/chapter_3227/handouts/chapter3227_7765_12-connect.png)

A popup will appear with instructions on how to connect. The commands in red boxes are the ones you should run.

**If you are a Mac user:**

Run the chmod command in your terminal.

**If you are a Windows user:**

SSH is not built into windows. The easiest solution is to use Git Bash or another bash terminal. The other solution requires the installation of other 3rd-party software, an SSH client. If you wish to do so, we recommend PuTTY.

**Everyone:**

Copy and paste the line starting with ssh (below) and paste the text into your terminal.

![ssh command pop up](https://s3.amazonaws.com/General_V88/boomyeah/company_209/chapter_3227/handouts/chapter3227_7766_13-connect-pop.png)

----------

You might have to type yes and wait for a few seconds or up to a minute before you are connected, but if all goes well, you should be on your Ubuntu cloud server. Your terminal should show something like this in the far left of your prompt:
```
ubuntu@54.162.31.253:~$ #Commands you write appear here
```

# Step 5: Server Configuration

Now we are going to set up our remote server for deployment. Our server is nothing more than a small allocated space on someone else’s larger computer (in this case, the big computer belongs to Amazon!). That space has an installed operating system, just like your computer. In this case, we are using a distribution of Linux called Ubuntu, version 16.04.  

## Create a user:

We should have a non-root user who also has root privileges. Let's create one now! In the example, our user will be named "kermit", but you may use whatever name you like.
```
sudo adduser kermit              // This will ask you to create a password. Make it secure!
                                 // You may then fill in your information, or press <enter> for default
sudo usermod -aG sudo kermit     // this will give the user root privileges
su - kermit                      // switch to the user kermit, your terminal prompt will indicate the change
```
## Server configuration:

Although we have linux, our new computer is otherwise empty. Let’s change that so we can start building a server capable of providing content that the rest of the world can access. In order to do so, we have to install some key programs first. First, let’s install python, python dev, pip, nginx, and git

In the terminal:
```py
sudo apt-get update
sudo add-apt-repository ppa:jonathonf/python-3.6    [press ENTER when prompted]
sudo apt-get update
sudo apt-get install python3.6 -y
sudo apt-get install python3-pip python3.6-dev nginx git -y
sudo apt-get update
sudo pip3 install virtualenv
```
## mySQL

Next, we will need to install our mySQL server:
```
sudo apt-get update
sudo apt-get install mysql-server                      // answer Yes when prompted!
```
A pop up will ask you to set your password. Type it in carefully! If you make it different from the password you use on your local machine, remember that you will have to update your mysqlconnection file in your Flask project.

Next, we will need to set up the database that our project will need. This can easily be done by going to MySQL Workbench and reverse engineering your desired database, then forward engineering it.

**1. Reverse engineer**

![](https://s3.amazonaws.com/General_V88/boomyeah2015/codingdojo/curriculum/content/chapter/Screen_Shot_2018-07-18_at_6.29.42_PM.png)

**2. Forward engineer**

We may filter out tables that we do not want forward engineered. Here, we are only going to process the tables in the simpleWall database. We excluded the tables from the emailVal and register databases by selecting them and clicking the right arrow.

![](https://s3.amazonaws.com/General_V88/boomyeah2015/codingdojo/curriculum/content/chapter/Screen_Shot_2018-07-18_at_6.31.25_PM.png)  

**3. Copy the script**

When MySQL Workbench asks you to review the script, that's when you can copy it!

![](https://s3.amazonaws.com/General_V88/boomyeah2015/codingdojo/curriculum/content/chapter/Screen_Shot_2018-07-18_at_6.32.04_PM.png)  

  

Now, in our deployed server, we can open the mysql shell by typing:
```
mysql -u root -p                                       // provide your mysql password when prompted
```
This is where you may run SQL queries! Including the code that will create your database for you! Just paste the script that you copied from MySQL Workbench, and it will create your database. You may verify that the database was created with:
```
SHOW DATABASES;
```
When you are ready to leave the mysql shell, type:
```
exit
```
## Get your project!

Now, we are going to clone our project that we want to deploy into our server and cd into it.
```
git clone {{ url copied from github project }}
cd {{ project }}
```
Make sure your project looks exactly like you remember it, and now let's make a virtual environment. The  `~/myRepoName$` prompt in the code snippets provided is to ensure that you know that you should be in your project when running these commands.

## Virtualenv and install the necessary Python modules
```
~/myRepoName$ virtualenv venv --python=python3.6          // create the environment and call it venv
~/myRepoName$ source venv/bin/activate                    // activate the environment
(venv) ~/myRepoName$ pip install -r requirements.txt      // install everything that requirements.txt says you need
(venv) ~/myRepoName$ pip install gunicorn                 // install gunicorn
(venv) ~/myRepoName$ pip install {{anything you need that was not already in requirements.txt}}
```

### VIM

If you have used VIM before, skip to the next tab.

VIM is a terminal based file editor. We will use it to change the necessary files in order to get our project running. In the following instructions, you'll be using the  `vim`command to enter the editor. The  `vim`  command can be used either to edit existing files or create and open a new blank file. Once you have entered the editor interface, press  `i`  to enter INSERT mode. You should see  `**–INSERT–**`  at the bottom left corner of your terminal. Now use your arrow keys to move the cursor to where you want to edit and make your changes.

Once you are done, press the  `esc`  key to exit INSERT mode. Type a colon to enter the vim command interface. You should now see a colon at the bottom left corner of your terminal. Now, type  `wq`  and press  `return`  to write (save) and quit.

If you want to quit without saving, type  `q!`  after the colon.

If you'd like to save without quitting, type  `w`  after the colon.


# Step 6: Gunicorn

Now, we need a wsgi.py file, which will help Gunicorn, our process manager, know how to interact with the application. We will use vim as our text editor to make our files.
```py
(venv) ~/myRepoName$ vim wsgi.py                     // this will open the new, empty file for us
```
We will need the following code in our wsgi.py file (this assumes that you named your server file server.py, if you named it something different you will have to put that name in place of  `server`  in the code below):
```py
from server import app as application
if __name__ == "__main__":
    application.run()
```
Now, we need to direct Gunicorn to our project's wsgi.py file, which is the entry point to our application.  
```py
(venv) ~/myRepoName$ gunicorn --bind 0.0.0.0:5000 wsgi:application
```
If your Gunicorn process ran correctly, you will see something like the following printed to the terminal:
```py
[2016-12-27 05:45:56 +0000] [8695] [INFO] Starting gunicorn 19.6.0
[2016-12-27 05:45:56 +0000] [8695] [INFO] Listening at: http://0.0.0.0:5000 (8695)
[2016-12-27 05:45:56 +0000] [8695] [INFO] Using worker: sync
[2016-12-27 05:45:56 +0000] [8700] [INFO] Booting worker with pid: 8700
```
If you have any error messages, read them carefully - you may need to install anything that was not already included in your requirements.txt file. Run the command again, reading your error messages, until you get the output you see above.

If that looks good, you may shut it down with ctrl + C, because we're still not done!  

Deactivate the virtual environment with:
```py
(venv) ~/myRepoName$ deactivate
```
Now, we need a systemd service unit file. This will automatically start Gunicorn when the server boots.

**A word on naming conventions:** Wherever you see  `{{project}}`, replace it with the name you call your Flask project. It does not matter what you choose, as long as you are consistent. We suggest choosing something short and easy to remember. Wherever you see  `{{repo name}}`, replace that with the name of your GitHub repo. It will be the same name as the directory that is created when you git clone your repo. It could well be that your repo name and your project name are the same.
```
sudo vim /etc/systemd/system/{{project}}.service
```
In this file you just created, we will need the following (everywhere where you see  {{username}}, replace that with the username you created for your server):
```
[Unit]
Description=Gunicorn instance to serve {{project}}
After=network.target
[Service]
User={{username}}
Group=www-data
WorkingDirectory=/home/{{username}}/{{repo name}}
Environment="PATH=/home/{{username}}/{{repo name}}/venv/bin"
ExecStart=/home/{{username}}/{{repo name}}/venv/bin/gunicorn --workers 3 --bind unix:{{project}}.sock -m 007 wsgi:application
[Install]
WantedBy=multi-user.target
```
After we create this file, we need to enable it, so that it starts when the server boots:
```
sudo systemctl start {{project}}
sudo systemctl enable {{project}}
```
After running these lines, you should see your {{project}}.sock file in your project, on the same level as server.py. If not, you probably have a typo in the systemd service unit file.

# Step 7: Nginx

Now, we just need to configure nginx to handle requests made by the server. Let's create a new file in sites-available.
```
sudo vim /etc/nginx/sites-available/{{project}}
```
In this file, we will need the following:
```
server {
    listen 80;
    server_name {{your public ip}};
    location / {
        include proxy_params;
        proxy_pass http://unix:/home/{{username}}/{{repo name}}/{{project}}.sock;
    }
}
```
Now, we need to link this nginx configuration to our sites-enabled directory.
```
sudo ln -s /etc/nginx/sites-available/{{project}} /etc/nginx/sites-enabled
```
Test nginx for errors:
```
sudo nginx -t
```
If we get a message saying that everything is (syntactically) ok, then we are almost done!

# Step 8: Wrapping Up

We will remove the Nginx default site display from directory sites-enabled, by running the following in your terminal.

sudo rm /etc/nginx/sites-enabled/default

Now, all that is left to do is restart your Nginx server.

sudo service nginx restart

If your server restarted correctly, you will see the new command line, and your app is deployed! Go to the public domain and your app should be there.

If you see anything other than your app, review your server file for errors.

To exit the remote server, type:

exit

## Common errors and how to find them:

-   502, bad gateway: there is a problem in your code. Hint: any error starting with 5 indicates a server error
-   Your Gunicorn process won’t start: Check your .service file; typos and wrong file paths are common mistakes
-   Your NGINX restart fails: Check your NGINX file in the sites-available directory. Common problems include typos and forgetting to insert your project name where indicated.
-   Make sure the URL requested is correct (example if your root route is /home, make sure you put /home after the IP)

# Step 9: Reconnecting

Remember how we said that we would have to change our security settings every time our IP changes? The bad news is that this will happen often. The good news is that it’s easy to change those settings, if you know where to look.

1.  In your AWS console, with your instance selected, scroll down to view some options. Next to security groups, you will see launch-wizard. Click it!  
    ![security groups](https://s3.amazonaws.com/General_V88/boomyeah/company_209/chapter_3227/handouts/chapter3227_7767_14-security-groups.png)
2.  Now you just have to update the IP connected to the instance. In the next window you will see something like this at the bottom of your screen. Click the inbound tab, and then select edit.  
    ![edit security groups](https://s3.amazonaws.com/General_V88/boomyeah/company_209/chapter_3227/handouts/chapter3227_7768_15-edit-groups.png)
3.  Now, all that is left to do is let AWS automatically change our IP to the new one. Do this by selecting the dropdown in the SSH row, under source, and select MyIP (it is already selected, but doing so again will refresh your IP to the current one). Once this is done, click save. You’re ready to SSH into your instance again!  
    ![update groups](https://s3.amazonaws.com/General_V88/boomyeah/company_209/chapter_3227/handouts/chapter3227_7769_16-update-security-groups.png)


