from django.db import models

from django.contrib.auth.models import User
from socialnetwork.models import *



class StudyGroup(models.Model):
	name = models.CharField(blank=True, max_length=40)
	owner = models.ForeignKey(Student, related_name="studygroups")
	members = models.ManyToManyField(Student, related_name='member')
	start_time = models.DateTimeField(auto_now_add=True)
	end_time = models.DateTimeField(auto_now_add=True)
	active = models.BooleanField(default=True)
	course = models.CharField(max_length = 10)
	topic = models.CharField(max_length=100)
	description = models.CharField(max_length=255)
	location_room = models.CharField(max_length=50)
	location_name = models.CharField(max_length=255)
	location_latitude = models.DecimalField(blank=True, null= True, default=40.4430939,max_digits=30,decimal_places=20)
	location_longitude  = models.DecimalField(blank=True, null= True, default=-79.942309,max_digits=30,decimal_places=20)
	def __unicode__(self):
		return 'StudyGroup(id=' + str(self.id) + ", owner=" + str(self.owner) + ')'


class StudyGroupPost(models.Model):
	group_name = models.CharField(blank=True, max_length=40)
	location = models.CharField(blank=True, max_length=40)
	text = models.CharField(max_length=4000)
	student = models.ForeignKey(Student)
	date = models.DateTimeField(auto_now_add=True)
	comments = models.ManyToManyField(Comment)
	upvotes = models.IntegerField(blank=True, default=0)
	studygroup = models.ForeignKey(StudyGroup, null=True, related_name='posts')
	title = models.CharField(max_length=200)
	attachment_url = models.CharField(blank=True, max_length=256)
	attachment_name = models.CharField(blank=True, max_length=200)
	def __unicode__(self):
		return self.text
	def natural_key(self):
		return(self.user, self.id)
# Create your models here.
