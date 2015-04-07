from django.db import models

from django.contrib.auth.models import User
from socialnetwork.models import *

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

# Create your models here.
