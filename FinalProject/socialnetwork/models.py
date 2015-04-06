from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
	user = models.OneToOneField(User)
	# classes = models.ManyToManyField(Classroom, related_name='class', symmetrical='True')
	school = models.CharField(blank=True, max_length=430)
	major = models.CharField(blank=True, max_length=430)
	interests = models.CharField(blank=True, max_length=430)
	linkedin = models.CharField(blank=True, max_length=430)
	friends = models.ManyToManyField('self', related_name='follows', symmetrical='False')
	picture_url = models.CharField(blank=True, max_length=256)
	answer_rating = models.IntegerField(blank=True, null=True)
	collab_rating = models.IntegerField(blank=True, null=True)
	endorsements = models.CharField(blank=True, max_length=430)
	age = models.IntegerField(blank=True) 
	def __unicode__(self):
		return 'Student(id=' + str(self.id) + ')'

class Comment(models.Model):
	text = models.CharField(max_length=160, null=True)
	student = models.ForeignKey(Student, null=True)
	date = models.DateTimeField(blank=True, auto_now_add=True, null=True)
	upvotes = models.IntegerField(blank=True, default=0)
	def __unicode__(self):
		return self.text
	def natural_key(self):
		return(self.text, self.date, self.username)

class Documents(models.Model):
	name = models.CharField(blank=True, max_length=40)
	documents_url = models.CharField(blank=True, max_length=150)
	upvotes = models.IntegerField(blank=True)
	owner = models.OneToOneField(Student)

class Classroom(models.Model):
	name = models.CharField(blank=True, max_length=40)
	students = models.ManyToManyField(Student, related_name='classes', symmetrical='True')
	documents = models.ManyToManyField(Documents)

	def __unicode__(self):
		return self.name

class Post(models.Model):
	group_name = models.CharField(blank=True, max_length=40)
	location = models.CharField(blank=True, max_length=40)
	text = models.CharField(max_length=160)
	student = models.ForeignKey(Student)
	date = models.DateTimeField(auto_now_add=True)
	comments = models.ManyToManyField(Comment)
	upvotes = models.IntegerField(blank=True, default=0)
	classroom = models.ForeignKey(Classroom, null=True, related_name='posts')

	def __unicode__(self):
		return self.text
	def natural_key(self):
		return(self.user, self.id)

	
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
	def __unicode__(self):
		return 'StudyGroup(id=' + str(self.id) + ", owner=" + str(self.owner) + ')'

