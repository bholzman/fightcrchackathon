from django.shortcuts import render
from django.http import HttpResponse
import json
from .models import Greeting, CRCTrials

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html', {'trials': json.dumps(CRCTrials().trials)})


def welcome(request):
    return render(request, 'welcome.html', {'trials': json.dumps(CRCTrials().trials)})


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

