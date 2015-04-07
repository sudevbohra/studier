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
	return render(request, 'socialnetwork/map.html', {'studygroupform' : studyRoomForm})

def add_studyroom(request):
	studygroupform = StudyGroupForm(request.POST)
	user = request.user
	student = Student.objects.get(user=user)
	studygroupform.isValid()
	studygroup = StudyGroup(name=user.first_name,
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

class StudyGroup(models.Model):
	name = models.CharField(blank=True, max_length=40)
	owner = models.OneToOneField(Student)
	members = models.ManyToManyField(Student, related_name='member')
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()
	active = models.BooleanField(default=True)
	course = models.CharField(max_length = 10)
	topic = models.CharField(max_length=100)
	description = models.CharField(max_length=255)
	location_room = models.CharField(max_length=50)
	location_name = models.CharField(max_length=255)
	location_latitude = models.FloatField()
	location_longitude  = models.FloatField()