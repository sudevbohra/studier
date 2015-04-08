from django.db import models

from django.contrib.auth.models import User
from socialnetwork.models import *



class StudyGroup(models.Model):
	name = models.CharField(blank=True, max_length=40)
	owner = models.ForeignKey(Student)
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

# Create your models here.
