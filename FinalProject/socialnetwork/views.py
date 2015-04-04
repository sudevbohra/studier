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
from socialnetwork.forms import RegistrationForm, EditForm

# Used to generate a one-time-use token to verify a user's email address
from django.contrib.auth.tokens import default_token_generator

# Used to send mail from within Django
from django.core.mail import send_mail

from django.core import serializers
from django.http import HttpResponse

# Create your views here.

@login_required
def home(request):
    # Sets up list of just the logged-in user's (request.user's) items
    user_id = request.user.id
    student = Student.objects.get(user=request.user)
    # For now we'll use 15437
    current_class = "15437"
    print (student.classes.all())
    return render(request, 'socialnetwork/index.html', {'user_id' : user_id, 'current_class' : current_class, "classes" : student.classes.all()})


@login_required
def map(request):
    return render(request, "socialnetwork/map.html", {})

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

    
    new_user = authenticate(username=form.cleaned_data['email'], \
                            password=form.cleaned_data['password1'])
    
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

    # return render(request, 'socialnetwork/index.html', context)
    return redirect(reverse('home'))

@login_required
def profile(request, id):
	user = get_object_or_404(User, id=id)
	full_name = user.get_full_name()
	student = Student.objects.get(user=user)
	school = student.school
	major = student.major
	return render(request, 'socialnetwork/profile.html', {'full_name' : full_name, 'student' : student, 'school' : school, 'major' : major})

@login_required
@transaction.atomic
def edit(request):
    try:
        if request.method == 'GET':
            profile = Student.objects.get(user=request.user)
            form = EditForm()
            context = { 'profile': profile, 'form': form }
            return render(request, 'socialnetwork/edit.html', context)
    
        profile = Student.objects.get(user=request.user)
        form = EditForm(request.POST, request.FILES, instance=profile)
        #print form
        if not form.is_valid():
           context = { 'profile': profile, 'form': form }
           return render(request, 'socialnetwork/edit.html', context)
        profile = form.save()
        print form.cleaned_data

        # Update first and last name of the User
        user = request.user
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.save()

        # form = EditForm(instance=entry)
        context = {
            'message': 'Profile updated.',
            'profile':   profile,
            'form':    form,
        }
        #return render(request, 'socialnetwork/profile.html', context)
        return redirect('/socialnetwork/profile/' + str(request.user.id))
    except Student.DoesNotExist:
        context = { 'message': 'Record with id={0} does not exist'.format(id) }
        return render(request, 'socialnetwork/edit.html', context)

@login_required
def map(request):
    # Sets up list of just the logged-in user's (request.user's) items
    user_id = request.user.id
    return render(request, 'socialnetwork/map.html', {'user_id' : user_id})

@login_required
@transaction.atomic
def add_class(request):
	try:
		student = Student.objects.get(user=request.user)
		classObj = Classroom.objects.get(name=request.POST['course_id']).students.add(student)
		return redirect(reverse('home'))
	except Classroom.DoesNotExist:
		new_class = Classroom(name=request.POST['course_id'])
		new_class.save()
		new_class.students.add(student)
		return redirect(reverse('home'))
	# if not (Classroom.objects.filter(name=request.POST['course_id']).count):
	# 	new_class = Classroom(name=request.POST['course_id'])
	# 	new_class.save()
	# 	new_class.students.add(student)
	# 	return redirect(reverse('home'))
	# student = Student.objects.get(user=request.user)
	# classObj = Classroom.objects.get(name=request.POST['course_id']).students.add(student)
	# return redirect(reverse('home'))


@login_required
@transaction.atomic
def remove_class(request, name):
	student = Student.objects.get(user = request.user)
	classObj = Classroom.objects.get(name=name)
	classObj.students.remove(student)
	classObj.save()
	return redirect(reverse('home'))

@login_required
@transaction.atomic
def add_post(request, name):
	errors = []
	# Creates a new item if it is present as a parameter in the request
	if not 'post' in request.POST or not request.POST['post']:
		errors.append('You must enter an item to add.')
		print "FUCK"
	else:
		student = Student.objects.get(user=request.user)
		new_post = Post(text=request.POST['post'], student=student, upvotes=0, location=name)
		new_post.save()
	return redirect(reverse('home'))

@login_required
@transaction.atomic
def add_comment(request, id):
	errors = []
	if not 'item' in request.POST or not request.POST['item']:
		errors.append('You must enter an item to add.')
	else:
		post = Post.objects.get(id=id)
        student = Student.objects.get(user=request.user)
        new_comment = Comment(text=request.POST['item'], student=student, upvotes=0)
        new_comment.save()
        post.comments.add(new_comment)
	return redirect(reverse('home'))