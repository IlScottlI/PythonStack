from django.shortcuts import render, HttpResponse

# Create your views here.


def index(request):

    return render(request, 'index.html')


def result(request):

    context = {
        'request': request,
        'backto': '/'

    }
    return render(request, 'index-1.html', context)
