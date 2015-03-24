from django.db import models

class Student(models.Model):
	user = models.OneToOneField(User)
	#How to do list of courses?
	courses = models.ManyToManyField('self', related_name='course', symmetrical='False')
	school = models.CharField(blank=True, max_length=430)
	major = models.CharField(blank=True, max_length=430)
	interests = models.CharField(blank=True, max_length=430)
	linkedin = models.CharField(blank=True, max_length=430)
	friends = models.ManyToManyField('self', related_name='follows', symmetrical='False')
	picture_url = models.CharField(blank=True, max_length=256)
	answer_rating = models.CharField(blank=True, max_length=430)
	collab_rating = models.CharField(blank=True, max_length=430)
	endorsements = models.CharField(blank=True, max_length=430)
	def __unicode__(self):
		return 'Student(id=' + str(self.id) + ')'
