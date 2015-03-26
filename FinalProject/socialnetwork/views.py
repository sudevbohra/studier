from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

# Django transaction system so we can use @transaction.atomic
from django.db import transaction

from socialnetwork.models import *
from socialnetwork.forms import RegistrationForm

# Used to generate a one-time-use token to verify a user's email address
from django.contrib.auth.tokens import default_token_generator

# Used to send mail from within Django
from django.core.mail import send_mail

from django.core import serializers
from django.http import HttpResponse

# Create your views here.

#login_required
def home(request):
    # Sets up list of just the logged-in user's (request.user's) items
    return render(request, 'socialnetwork/index.html', {})

@transaction.atomic
def register(request):
    context = {}

    # Just display the registration form if this is a GET request
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'socialnetwork/register.html', context)

    form = RegistrationForm(request.POST)
    context['form'] = form

    errors = []
    context['errors'] = errors

    # Checks the validity of the form data
    if not form.is_valid():
        return render(request, 'socialnetwork/register.html', context)

    # Creates the new user from the valid form data
    new_user = User.objects.create_user(username=form.cleaned_data['email'],
                                        password=form.cleaned_data['password1'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'],
                                        email=form.cleaned_data['email'])
    
    # Mark the user as inactive to prevent login before email confirmation.
    new_user.is_active = True
    new_user.save()

    
    new_user = authenticate(username=request.POST['email'], \
                            password=request.POST['password1'])
    
    new_profile = Student(user=new_user, age=0,
                        school=form.cleaned_data['school'],
                        major=form.cleaned_data['major'])
    new_profile.save()

#     # Generate a one-time use token and an email message body
#     token = default_token_generator.make_token(new_user)

#     email_body = """
# Welcome to Social Network!  Please click the link below to
# verify your email address and complete the registration of your account:
#   http://%s%s
# """ % (request.get_host(), 
#        reverse('confirm', args=(new_user.username, token)))

#     send_mail(subject="Verify your email address",
#               message= email_body,
#               from_email="psrivast@andrew.cmu.edu",
#               recipient_list=[new_user.email])

#     context['email'] = form.cleaned_data['email']

    # Logs in the new user
    login(request, new_user)

    return render(request, 'socialnetwork/index.html', context)
