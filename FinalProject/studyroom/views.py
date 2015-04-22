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
from socialnetwork.views import *
from socialnetwork.models import *
from socialnetwork.forms import *
from studyroom.models import *
from studyroom.forms import *
from socialnetwork.s3 import s3_upload, s3_delete

# Used to generate a one-time-use token to verify a user's email address
from django.contrib.auth.tokens import default_token_generator

# Used to send mail from within Django
from django.core.mail import send_mail

from django.core import serializers
from django.http import HttpResponse
import json
import datetime
from dateutil.tz import *
from django.utils import timezone
from django.http import Http404
from django.db.models import F
import traceback

def get_default_context(request):
    user_id = request.user.id
    student = Student.objects.get(user=request.user)
    context = {}
    context['notifications'] = student.notifications
    context['classes'] = student.classes.all()
    context['user_id'] = request.user.id
    context['student'] = student
    context['studygroups'] = student.groups.all()
    if(len(student.notifications.all()) > 0):
        context['notif_count'] = len(student.notifications.all())
    return context

@login_required
def show_modal(request, error=None):
	student = Student.objects.get(user=request.user)
	studyRoomForm = StudyGroupForm(None,user=student)
	context = get_default_context(request)
	context['studygroupform'] = studyRoomForm
	if error != None:
		context["error"] = error
	return render(request, 'socialnetwork/map.html', context)



@login_required
@transaction.atomic
def upvotePostStudygroup(request, id, upvote):
    post = Post.objects.get(id=id)
    print post.upvoters.all()
    student = Student.objects.get(user=request.user)
    if (student not in post.upvoters.all()) and int(upvote) == 1:
        post.upvoters.add(student)
        post.upvotes += int(upvote)
    elif student not in post.downvoters.all() and int(upvote) == -1:        
        post.downvoters.add(student)
        post.upvotes += int(upvote)
    elif student in post.upvoters.all() and int(upvote) == -1:
        post.upvoters.remove(student)
        post.upvotes += int(upvote)
    elif student in post.downvoters.all() and int(upvote) == 1:
        post.downvoters.remove(student)
        post.upvotes += int(upvote)
    
    post.save()
    return show_post_studygroup(request, id)


@login_required
def map_studygroups(request, id):
    # # Sets up list of just the logged-in user's (request.user's) items

    user_id = request.user.id
    student = Student.objects.get(user=request.user)
    context = get_default_context(request)
    context["user_id"] = user_id
    context["student"] = student
    context["classes"] = student.classes.all()
    context['studygroup_id'] = id
    # # For now we'll use 15437
    # current_class = "15437"
    # context = {'user_id' : user_id, 'current_class' : current_class, "classes" : student.classes.all()}
    # context['form'] = PostForm()
    # context['comment_form'] = CommentForm()
    # return render(request, 'socialnetwork/index.html', context)
    return render(request, "socialnetwork/map-selector.html", context)


@login_required
def add_studygroup(request):
	user = request.user
	student = Student.objects.get(user=user)
	studygroupform = StudyGroupForm(request.POST)
	
	if not studygroupform.is_valid():
		return home(request, "You need to provide a name, course, location, start time and end time!")
	try:
		print studygroupform.cleaned_data["course"]
		course = Classroom.objects.get(id=studygroupform.cleaned_data["course"])
	except Classroom.DoesNotExist:
		course = None
	if course == None: 
		return home(request, "You are not in that class")
	if student not in course.students.all():
		return home(request, "You are not in that class")

	studygroup = StudyGroup(name=studygroupform.cleaned_data['name'],
							owner=student,
							active=True,
							classroom=course,
							course=course.name,
							location_name=studygroupform.cleaned_data['location_name'],
							private=studygroupform.cleaned_data['private'])
	studygroup.save()
	studygroup.members.add(student)
	studygroup.start_time = datetime.datetime.strptime(request.POST['startTime'], "%m/%d/%Y %I:%M %p").replace(tzinfo=tzlocal())
	studygroup.end_time = datetime.datetime.strptime(request.POST['endTime'], "%m/%d/%Y %I:%M %p").replace(tzinfo=tzlocal())
	studygroup.save()
	instructions = "\n Owner: {1} \nStart Time: {2} \nEnd Time: {3} \n\nWelcome to {0}. \n This is a studyroom for {4}. Join to view all posts. ".format(studygroup.name, studygroup.owner.user.first_name + " " + studygroup.owner.user.last_name,\
		request.POST['startTime'], request.POST['endTime'], studygroupform.cleaned_data['course'])
	post = Post(text=instructions, title="Studyroom Welcome Post")
	
	post.student = student
	post.upvotes = 0
	post.studygroup = studygroup
	post.save()
	studygroup.save()
	return map_studygroups(request, studygroup.id)
# Create your views here.

import traceback

@login_required
def set_map_studygroup(request):
	
	try:
		student = Student.objects.get(user_id=int(request.POST['user']))
		studygroup = StudyGroup.objects.get(id = request.POST['id'])
		if student == studygroup.owner:
			
			studygroup.location_latitude = request.POST['lat']
			studygroup.location_longitude = request.POST['lng']

			studygroup.save()
	except Exception:
		print "Error in set_map_studygroup"
		print traceback.format_exc()
	return HttpResponse()


def default_studygroup(student):
    return student.natural_key() + " is studying"

import traceback
@login_required
@transaction.atomic
def set_map_studygroup_default(request):
	if request.method == 'POST':
		try:
			course = request.POST['course']
			print "HERE"
			if Classroom.objects.filter(name = course).count() != 0:
				print "AFTER IF"
				student  = Student.objects.get(user_id =request.POST['id'])
				classroom = Classroom.objects.get(name=course)
				if student not in classroom.students.all():
					return home(request, "You are not in this class!")
				studygroup = StudyGroup(name=  default_studygroup(student),
									owner= student,
									active=True,
									classroom = classroom,
									course=request.POST['course'],
									location_name= "Check Pin",private=False)
				studygroup.location_latitude = request.POST['lat']
				studygroup.location_longitude = request.POST['lng']
				studygroup.save()
				studygroup.end_time += datetime.timedelta(hours=6)
				instructions = "\n Owner: {1} \nStart Time: {2}  \n\nWelcome to {0}. \n This is a studyroom for {3}. Join to view all posts. ".format(studygroup.name, studygroup.owner.user.first_name + " " + studygroup.owner.user.last_name,\
				studygroup.start_time.strftime("%m/%d/%Y %I:%M %p"), course)
				post = Post(student = student, upvotes = 0, text=instructions, title="Studyroom Welcome Post", studygroup = studygroup)
				post.save()
				studygroup.posts.add(post)
				studygroup.members.add(student)
				studygroup.save()

		except Exception:
			print "Error in set_map_studygroup_default"
			print traceback.format_exc()
		return HttpResponse()
	elif request.method == 'GET':
		try:
			now = datetime.datetime.now().replace(tzinfo=tzlocal())
			student  = Student.objects.get(user_id =request.GET['id'])
			studygroups = StudyGroup.objects.filter(owner=student, name= default_studygroup(student) , start_time__lte = now, end_time__gte = now)
			studygroups.delete()


		except Exception:
			print "Error in set_map_studygroup_default"
			print traceback.format_exc()



@login_required
def get_studygroups(request, user_id):
	courses = [cls.name for cls in Student.objects.get(user_id=user_id).classes.all()]
	now = datetime.datetime.now().replace(tzinfo=tzlocal())
	# start_time__lte = now, <-- add to only show groups which are in progress
	inactive_studygroups = StudyGroup.objects.filter(end_time__gte=now, start_time__gte=now, course__in = courses, active = True)
    #[elem for elem in li if li.count(elem) == 1]

	for sg in inactive_studygroups.all():
		sg.active = False
		sg.save()
	studygroups = StudyGroup.objects.filter(end_time__gte=now, course__in = courses)

	response_text = serializers.serialize('json', studygroups, use_natural_foreign_keys=True)
	return HttpResponse(response_text , content_type="application/json")

@login_required
@transaction.atomic
def add_post_studygroup(request, id):
	student = Student.objects.get(user=request.user)
	studygroup = StudyGroup.objects.get(id=id)
	if student not in studygroup.members.all():
		return home(request, "You arent in this studygroup")
	errors = []
	form = PostForm(request.POST, request.FILES)
	if(form.is_valid()):
		post = Post(text=form.cleaned_data['text'], title=form.cleaned_data['title'])
		
		
		post.studygroup = studygroup
		post.student = student
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
	

@login_required
def show_post_studygroup(request, id):
	user_id = request.user.id
	student = Student.objects.get(user=request.user)
	current_post = Post.objects.get(id=id)
	posts = current_post.studygroup.posts.order_by('-date')
	current_studygroup = current_post.studygroup
	context = get_default_context(request)
	context['current_studygroup'] = current_studygroup
	
	if student in current_studygroup.members.all():
		context['current_post'] = current_post
		context['posts'] = posts
		context['is_member'] = True
	else:
		context['current_post'] = posts[posts.count()-1]
		context['is_member'] = False

	context['is_owner'] = (student == current_studygroup.owner)
	context['form'] = PostForm()
	context['in_studygroup'] = True
	context['comment_form'] = CommentForm()
	context['students'] = current_post.studygroup.members
	context['studygroups'] = student.groups.all()
	exclude_pks = []
	for stu in current_studygroup.members.all():
		exclude_pks.append(stu.pk)
	context['class_students'] = current_studygroup.classroom.students.exclude(pk__in=exclude_pks)
	# context['class_students'] = current_studygroup.classroom.students.all()
	print current_studygroup.id
	if current_post.attachment_url:
		context['attachment_url'] = current_post.attachment_url
		context['attachment_name'] = current_post.attachment_name
		print current_post.attachment_url
	return render(request, 'socialnetwork/studygroup.html', context)

def in_studygroup(student, studygroup):
	if studygroup.members.objects.filter(id = student.id).count() != 0:
		return True
	else:
		False

def in_class(student, classroom):
	if classroom.students.objects.filter(id = student.id).count() != 0:
		return True
	else:
		False

@login_required
def change_studygroup(request, id):
	try:
	    user_id = request.user.id
	    student = Student.objects.get(user=request.user)
	    posts = StudyGroup.objects.get(pk=id).posts.all()
	   
	    current_post = posts[:1].get()
	     #+ name + ". This is a place of learning. Life is short."
	    # context = {'current_post' : current_post, 'current_class' : current_class, 'user_id' : user_id, 'current_class' : name, "classes" : student.classes.all(), "posts" : posts}
	    # context['form'] = PostForm()
	    # context['comment_form'] = CommentForm()
	    return show_post_studygroup(request, current_post.id )
	except ObjectDoesNotExist:
		raise Http404("StudyGroup does not exist")

@login_required
def add_comment(request, id):
	form = CommentForm(request.POST, request.FILES)
	post = Post.objects.get(id=id)
	student = Student.objects.get(user=request.user)
	#form.cleaned_data["text"]
	form.is_valid()
	new_comment = Comment(text=form.cleaned_data["text"], student=student, upvotes=0)
	new_comment.save()
	if form.cleaned_data['attachment']:
	    url = s3_upload(form.cleaned_data['attachment'], new_comment.id)
	    new_comment.attachment_url = url
	    if form.cleaned_data['attachment_name']:
	        new_comment.attachment_name = form.cleaned_data['attachment_name']
	    else:
	        new_comment.attachment_name = post.title
	    new_comment.save()
	post.comments.add(new_comment)
	post.save()
	class_name = post.classroom

	# Notification function
	notif_text = request.user.get_full_name() + " commented on your post"
	notif_link = '/studyroom/show_post_studygroup/' + str(post.id)
	notify(request, post.student.id, notif_text, notif_link)

	return show_post_studygroup(request, post.id)


@login_required
@transaction.atomic
def remove_person_studygroup(request, id):
    student = Student.objects.get(user = request.user)
    studygroup = StudyGroup.objects.get(id=id)
    studygroup.members.remove(student)
    studygroup.save()
    if student == studygroup.owner:
    	print "OWNER IS DELETING"
    	studygroup.delete()
    
    return home(request)

@login_required
@transaction.atomic
def add_person_studygroup(request, id):
    student = Student.objects.get(user = request.user)
    studygroup = StudyGroup.objects.get(id=id)
    studygroup.members.add(student)
    studygroup.save()
    return change_studygroup(request, studygroup.id)

@login_required
@transaction.atomic
def send_invites(request):
	queryDict = request.POST
	myDict = dict(queryDict.iterlists())
	print myDict
	invite_list = list(set(myDict['invites[]']))
	studygroup_id = myDict['studygroup_id'][0]
	print studygroup_id
	print invite_list
	print invite_list[0]
	studygroup = StudyGroup.objects.get(id=studygroup_id)
	# Notify each invited student
	for stu_id in invite_list:
		student = Student.objects.get(id=stu_id)
		notif_text = request.user.get_full_name() + " has invited you to " + studygroup.name
		notif_link = '/socialnetwork/add_person_studygroup/' + studygroup_id
		notify(request, stu_id, notif_text, "", yes_link=notif_link, no_link="")

 	
 	return HttpResponse()
	
@login_required
def add_to_studygroup(request, studygroup_id, student_id):
	studygroup = StudyGroup.objects.get(id=studygroup_id)
	student = Student.objects.get(id=student_id)
	studygroup.members.add(student)
	return change_studygroup(request, studygroup_id)

@login_required
def request_to_be_added(request, id):
	context = get_default_context(request)
	studygroup = StudyGroup.objects.get(id=id)
	user = request.user
	notif_link = "/studyroom/add_to_studygroup/" + str(id) + "/" + str(user.id)
	notif_text = user.first_name + " " + user.last_name + " wants to join your studygroup " + studygroup.name + ". Click the link to accept!"
	notify(request, studygroup.owner.id, notif_text, "", yes_link=notif_link, no_link="")
	return home(request)
