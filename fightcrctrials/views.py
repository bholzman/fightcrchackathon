from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import ensure_csrf_cookie
import json
import os
import sendgrid
from sendgrid.helpers.mail import Email, Content, Mail

from .forms import ContactUsForm
from .models import Greeting, CRCTrial, FAQ


# Create your views here.
@ensure_csrf_cookie
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html', {'trials': CRCTrial.trials_json()})


def welcome(request):
    return render(request, 'welcome.html', {'trials': CRCTrial.trials_json()})


def faq(request):
    faqs = FAQ.objects.all()
    return render(request, 'faq.html', {'faqs': faqs})

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})


def _send_email(subject, message, reply_to=None):
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email('fightcrchackathon@gmail.com')
    to_email = Email(os.environ.get('FIGHT_CRC_EMAIL'))
    content = Content("text/plain", message)
    mail = Mail(from_email, subject, to_email, content)
    if reply_to is not None:
        mail.set_reply_to(Email(reply_to))
    return sg.client.mail.send.post(request_body=mail.get())


def send_trial_closed_email(request):
    if request.method == 'POST':
        drug_name = request.POST.get('drug')
        nct = request.POST.get('nct', 'No NCT# available')
        user = request.POST.get('user')

        response = _send_email(
            'User reports trial "{}" has closed'.format(drug_name),
            "User '{}' reports that trial '{}' (NCT #: {}) has closed.".format(
                user, drug_name, nct))

        return HttpResponse(response.body)


def contactus(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            message = (' First name: {}\n' 
                       ' Last name: {}\n'
                       ' Email: {}\n'
                       ' Role: {}\n'
                       ' Comment: {}'.format(
                form.cleaned_data['first_name'],
                form.cleaned_data['last_name'],
                form.cleaned_data['email'],
                form.cleaned_data['user_class'],
                form.cleaned_data['comment']))
            response = _send_email(
                'Feedback from Fight CRC Trials',
                message,
                reply_to=form.cleaned_data['email'])

            return HttpResponseRedirect('/')
    else:
        form = ContactUsForm()

    return render(request, 'contactus.html', {'form': form})
