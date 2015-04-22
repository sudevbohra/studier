from django import forms
from django.contrib.auth.models import User
from socialnetwork.models import *
from django.forms.widgets import SplitDateTimeWidget
from datetime import datetime


class StudyGroupForm(forms.ModelForm):

	class Meta:
		model = StudyGroup
		name = models.CharField(blank=True, max_length=40)
		exclude = ['location_latitude', 'location_longitude', 'owner', 'members', 'active', 'course', 'classroom']

	def __init__(self, *args, **kwargs):
		if 'user' in kwargs:
			user = kwargs.pop('user')
		else: 
			user = None
		super(StudyGroupForm, self).__init__(*args, **kwargs)
		if user != None:
			self.fields['course'] = forms.ModelChoiceField(queryset=Classroom.objects.filter(students__id=user.id))
		else:
			self.fields['course'] = forms.CharField(max_length=10)

	def clean(self):
		cleaned_data = super(StudyGroupForm, self).clean()
		return cleaned_data

	