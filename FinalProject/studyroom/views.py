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
import json

@login_required
def show_modal(request, error=None):
	studyRoomForm = StudyGroupForm()
	user_id = request.user.id
	student = Student.objects.get(user=request.user)
	context = {}
	context["user_id"] = user_id
	context["student"] = student
	context['studygroupform'] = studyRoomForm
	context['classes'] = student.classes.all()
	if error != None:
		context["error"] = error
	return render(request, 'socialnetwork/map.html', context)

@login_required
def map_studygroups(request, studygroup_id):
    # # Sets up list of just the logged-in user's (request.user's) items
    user_id = request.user.id
    student = Student.objects.get(user=request.user)
    context = {}
    context["user_id"] = user_id
    context["student"] = student
    context["classes"] = student.classes.all()
    context['studygroup_id'] = studygroup_id
    # # For now we'll use 15437
    # current_class = "15437"
    # context = {'user_id' : user_id, 'current_class' : current_class, "classes" : student.classes.all()}
    # context['form'] = PostForm()
    # context['comment_form'] = CommentForm()
    # return render(request, 'socialnetwork/index.html', context)
    return render(request, "socialnetwork/map-selector.html", context)


@login_required
def add_studygroup(request):
	studygroupform = StudyGroupForm(request.POST)
	user = request.user
	student = Student.objects.get(user=user)
	studygroupform.is_valid()
	if studygroupform.cleaned_data["course"] not in student.classes.all():
		return show_modal(request, "You are not in that class")
	studygroup = StudyGroup(name=studygroupform.cleaned_data['name'],
							owner=student,
							active=True,
							course=studygroupform.cleaned_data['course'],
							topic=studygroupform.cleaned_data['topic'],
							description=studygroupform.cleaned_data['description'],
							location_room=studygroupform.cleaned_data['location_room'],
							location_name=studygroupform.cleaned_data['location_name'])
	studygroup.save()
	return map_studygroups(request, studygroup.id)
# Create your views here.


@login_required
def set_map_studygroup(request):
	
	try:
		studygroup = StudyGroup.objects.get(id = request.POST['id'])
		studygroup.location_latitude = request.POST['lat']
		studygroup.location_longitude = request.POST['lng']
		studygroup.save()
	except Exception:
		print "Error in set_map_studygroup"
	return HttpResponse()

@login_required
def get_studygroups(request, user_id):
	courses = [cls.name for cls in Student.objects.get(user_id=user_id).classes.all()]
	studygroups = StudyGroup.objects.filter(course__in = courses)
    #[elem for elem in li if li.count(elem) == 1]
	response_text = serializers.serialize('json', studygroups, use_natural_foreign_keys=True)
	return HttpResponse(response_text , content_type="application/json")
