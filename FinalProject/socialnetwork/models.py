from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class MyUser(models.Model):
	user = models.OneToOneField(User, related_name='user_set')
	bio = models.CharField(max_length=430)
	picture_url = models.FileField(blank=True, max_length=256, default="pictures/defaultImage.jpeg")
	age = models.IntegerField()

	def __unicode__(self):
		return self.bio

	def natural_key(self):
		return(self.user.username, self.user.id)