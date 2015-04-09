from django import forms
from django.contrib.auth.models import User
from studyroom.models import *
from django.forms.widgets import SplitDateTimeWidget
from datetime import datetime

# def getTime():
# 	return datetime.now()

# def get3Hours():
# 	return datetime.now() + timedelta(hours=3)

class StudyGroupForm(forms.ModelForm):
	# start_time = forms.DateTimeField(default=getTime())
	# end_time = forms.DateTimeField(default=get3Hours())

	class Meta:
		model = StudyGroup
		name = models.CharField(blank=True, max_length=40)
		exclude = ['location_latitude', 'location_longitude', 'owner', 'members', 'active']

	def clean(self):
		cleaned_data = super(StudyGroupForm, self).clean()
		return cleaned_data

