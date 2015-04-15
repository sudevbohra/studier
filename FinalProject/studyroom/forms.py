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

class StudyGroupPostForm(forms.Form):
    text = forms.CharField(max_length=300, widget = forms.Textarea)
    title = forms.CharField(max_length=300)
    attachment = forms.FileField(required=False, label="Attachment")
    attachment_name = forms.CharField(max_length=200, required=False)
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(PostForm, self).clean()
        # We must return the cleaned data we got from our parent.
        return cleaned_data

    def clean_attachment(self):
        attachment = self.cleaned_data['attachment']
        if not attachment:
            return None
        if attachment.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError('File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
        return attachment