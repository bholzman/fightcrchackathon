from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import ensure_csrf_cookie
import json
import os
import sendgrid
from sendgrid.helpers.mail import Email, Content, Mail

from .email import send_email
from .forms import ContactUsForm
from .models import CRCTrial, FAQ, MobileFAQ


# Create your views here.
@ensure_csrf_cookie
def index(request):
    return render(request, 'index.html', {'trials': CRCTrial.trials_json()})


def index_json(request):
    resp = HttpResponse(CRCTrial.trials_json())
    resp['Access-Control-Allow-Origin'] = '*'
    return resp


@ensure_csrf_cookie
def welcome(request):
    return render(request, 'welcome.html', {'trials': CRCTrial.trials_json()})


def _faq(request, model):
    faqs = model.objects.order_by('id').all()
    return render(request, 'faq.html', {'faqs': faqs})
    
def _faq_json(request, model):
    resp = HttpResponse(model.faq_json())
    resp['Access-Control-Allow-Origin'] = '*'
    return resp


def faq(request):
    return _faq(request, FAQ)


def faq_json(request):
    return _faq_json(request, FAQ)


def mobile_faq(request):
    return _faq(request, MobileFAQ)


def mobile_faq_json(request):
    return _faq_json(request, MobileFAQ)


def send_trial_closed_email(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        nct = request.POST.get('nct') or 'No NCT# available'

        response = send_email(
            'User reports trial "{}" has closed'.format(title),
            "User reports that trial '{}' ({}) has closed.".format(
                title, nct))

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
            response = send_email(
                'Feedback from Fight CRC Trials',
                message,
                reply_to=form.cleaned_data['email'])

            return HttpResponseRedirect('/')
    else:
        form = ContactUsForm()

    return render(request, 'contactus.html', {'form': form})
