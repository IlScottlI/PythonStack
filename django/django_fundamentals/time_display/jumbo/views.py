from django.shortcuts import render
from time import gmtime, strftime
import datetime


def index(request):
    context = {
        "time": strftime("%I:%M %p", gmtime()),
        "datetime": datetime.datetime.now(),
        "day": datetime.datetime.now().strftime("%d"),
        "month": datetime.datetime.now().strftime("%b"),
        "year": datetime.datetime.now().strftime("%Y"),

    }
    print(context)
    return render(request, 'index.html', context)
