from django import forms
from django.contrib.auth.models import User
from studyroom.models import *
from django.forms.widgets import SplitDateTimeWidget

class StudyGroupForm(forms.ModelForm):
	start_time = forms.DateTimeField(widget=SplitDateTimeWidget)
	end_time = forms.DateTimeField(widget=SplitDateTimeWidget)

	class Meta:
		model = StudyGroup
		name = models.CharField(blank=True, max_length=40)
		exclude = ['location_latitude', 'location_longitude', 'owner', 'members', 'active']
	def clean(self):
		cleaned_data = super(StudyGroupForm, self).clean()
		return cleaned_data

