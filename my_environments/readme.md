Creating Virtual Environments

python -m venv <Environment-Name>

# Example

# python -m venv flask-env

<Environment-Name>\Scripts\activate.bat

# Example

# flask-env\Scripts\activate.bat

<h1>django Commands ( Must be in the project folder with the manage.py file) </h1>

Create a new project

# django-admin startproject project_namep

Create a new app

# python manage.py startapp app_name

Change Directory

# cd app_name

Run django server

# python manage.py runserver

Change Directory (Back a folder)

# cd ..\..\

Run this to get migrations ready

# python manage.py makemigrations

Run this to view static files

# python manage.py migrate
