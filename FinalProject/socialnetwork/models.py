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


class StudyGroup(models.Model):
    owner = models.OneToOneField(Student)
    members = models.ManyToManyField(Student)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    active = models.BooleanField()
    course = models.CharField(max_length = 10)
    topic = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    location_room = models.CharField(max_length=50)
    location_name = models.CharField(max_length=255)
    location_latitude = models.FloatField()
    location_longitude  = models.FloatField()
    def __unicode__(self):
		return 'StudyGroup(id=' + str(self.id) + ", owner=" + str(self.owner) + ')'
