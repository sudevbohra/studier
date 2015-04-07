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
from socialnetwork.forms import *
from studyroom.models import *
from studyroom.forms import *

# Used to generate a one-time-use token to verify a user's email address
from django.contrib.auth.tokens import default_token_generator

# Used to send mail from within Django
from django.core.mail import send_mail

from django.core import serializers
from django.http import HttpResponse

def show_modal(request):
	studyRoomForm = StudyGroupForm()
	user_id = request.user.id
	student = Student.objects.get(user=request.user)
	context = {}
	context["user_id"] = user_id
	context["student"] = student
	context['studygroupform'] = studyRoomForm
	context['classes'] = student.classes.all()
	return render(request, 'socialnetwork/map.html', context)

def add_studygroup(request):
	studygroupform = StudyGroupForm(request.POST)
	user = request.user
	student = Student.objects.get(user=user)
	studygroupform.isValid()
	studygroup = StudyGroup(name=studygroupform.cleaned_data['name'],
							owner=student,
							start_time=studygroupform.cleaned_data['start_time'],
							end_time= studygroupform.cleaned_data['end_time'],
							active=True,
							course=studygroupform.cleaned_data['course'],
							topic=studygroupform.cleaned_data['topic'],
							description=studygroupform.cleaned_data['description'],
							location_room=studygroupform.cleaned_data['location_room'],
							location_name=studygroupform.cleaned_data['location_name'])
	studygroup.save()
	return redirect(reverse('home'))
# Create your views here.
