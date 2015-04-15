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
	try:
		course = Classroom.objects.get(name=studygroupform.cleaned_data["course"])
	except Classroom.DoesNotExist:
		course = None
	if course == None: 
		return show_modal(request, "You are not in that class")
	if student not in course.students.all():
		return show_modal(request, "You are not in that class")
	if 'datetime' not in request.POST:
		return show_modal(request, "Please enter a time and date")
	print request.POST['datetime']
	studygroup = StudyGroup(name=studygroupform.cleaned_data['name'],
							owner=student,
							active=True,
							course=studygroupform.cleaned_data['course'],
							topic=studygroupform.cleaned_data['topic'],
							description=studygroupform.cleaned_data['description'],
							location_room=studygroupform.cleaned_data['location_room'],
							location_name=studygroupform.cleaned_data['location_name'])
	instructions = "Welome to the Class. No Posts exist yet. Add some posts using the button on the left!"
	post = Post(text=instructions, title="Instructions")
	post.studygroup = studygroup
	post.student = student
	post.upvotes = 0
	post.save()
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

@login_required
@transaction.atomic
def add_post_studygroup(request, name):
	errors = []
	form = StudyGroupPostForm(request.POST, request.FILES)
	if(form.is_valid()):
		post = Post(text=form.cleaned_data['text'], title=form.cleaned_data['title'])
		student = Student.objects.get(user=request.user)
		studygroup = StudyGroup.objects.get(name=name)
		post.studygroup = studygroup
		post.student = student
		post.location = name
		post.upvotes = 0
		post.save()
		if form.cleaned_data['attachment']:
		    url = s3_upload(form.cleaned_data['attachment'], post.id)
		    post.attachment_url = url
		    if form.cleaned_data['attachment_name']:
		    	post.attachment_name = form.cleaned_data['attachment_name']
		    else:
		    	post.attachment_name = post.title
		    post.save()
	return show_post_studygroup(request, post.id)
	else:
		print 'FORM NOT VALID'
	return change_studygroup(request, name)

@login_required
def show_post_studygroup(request, id):
	user_id = request.user.id
	student = Student.objects.get(user=request.user)
	current_post = Post.objects.get(id=id)
	posts = current_post.studygroup.posts.all()
	current_class = current_post.classroom
	context = {'current_post' : current_post, 'current_class' : current_class, 'user_id' : user_id, "classes" : student.classes.all(), "posts" : posts}
	context['form'] = PostForm()
	context['comment_form'] = CommentForm()
	context['students'] = current_class.students
	if current_post.attachment_url:
		context['attachment_url'] = current_post.attachment_url
		context['attachment_name'] = current_post.attachment_name
		print current_post.attachment_url
	return render(request, 'socialnetwork/studygroup.html', context)

@login_required
def change_studygroup(request, name):
    user_id = request.user.id
    student = Student.objects.get(user=request.user)
    posts = StudyGroup.objects.get(name=name).posts.all()
    current_class = name
    try:
        current_post = posts[:1].get()
    except Exception:
        current_post = "Welcome to the Classroom " #+ name + ". This is a place of learning. Life is short."
    # context = {'current_post' : current_post, 'current_class' : current_class, 'user_id' : user_id, 'current_class' : name, "classes" : student.classes.all(), "posts" : posts}
    # context['form'] = PostForm()
    # context['comment_form'] = CommentForm()
    return show_post_studygroup(request, current_post.id)

