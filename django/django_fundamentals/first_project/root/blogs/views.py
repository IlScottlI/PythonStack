
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse


def index(request):
    return HttpResponse("placeholder to later display a list of all blogs")


def root(request):
    return redirect("/blogs")


def blogs(request):
    return HttpResponse("<h1>Placeholder to later display a list of all blogs</h1>")


def new(request):
    return HttpResponse("<h1>Placeholder to display a new form to create a new blog</h1>")


def create(request):
    return redirect('/')


def view(request, number):
    return HttpResponse(f"<h1>Placeholder to display blog number: {number}</h1>")


def edit(request, number):
    return HttpResponse(f"<h1>Placeholder to edit blog {number}</h1>")


def destroy(request, number):
    return redirect('/blogs')


def return_json(request):
    response = JsonResponse({"title": "My First Blog", "content": "It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like)."})
    # Just wanted to ensure the correct Content-type was sent to the browser.
    response['Content-type'] = 'application/json'
    return response
