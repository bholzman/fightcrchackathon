from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
import json
import os
import sendgrid
from sendgrid.helpers.mail import Email, Content, Mail

from .models import Greeting, CRCTrials


# Create your views here.
@ensure_csrf_cookie
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html', {'trials': json.dumps(CRCTrials().trials)})


def welcome(request):
    return render(request, 'welcome.html', {'trials': json.dumps(CRCTrials().trials)})


def faq(request):
    return render(request, 'faq.html', {'trials': json.dumps(CRCTrials().trials)})

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})


def send_trial_closed_email(request):
    if request.method == 'POST':
        drug_name = request.POST.get('drug')
        nct = request.POST.get('nct', 'No NCT# available')
        user = request.POST.get('user')

        sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
        from_email = Email("fightcrchackathon@gmail.com")
        subject = 'User reports trial "{}" has closed'.format(drug_name)
        to_email = Email(os.environ.get('CLOSED_TRIAL_EMAIL'))
        message = "User '{}' reports that trial '{}' (NCT #: {}) has closed.".format(
            user, drug_name, nct)
        content = Content("text/plain", message)
        mail = Mail(from_email, subject, to_email, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        return HttpResponse(response.body)
