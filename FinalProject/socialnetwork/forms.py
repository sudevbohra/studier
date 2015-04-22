from django import forms

from django.contrib.auth.models import User
from models import *

MAX_UPLOAD_SIZE = 2500000

def get_schools():
    schools = open('colleges.txt', 'r')
    choices = []
    for school in schools:
        school = school.strip()
        schoolTuple = (school)
        statusTuple = (schoolTuple, schoolTuple)
        choices.append(statusTuple)

    schools.close()
    return tuple(choices)

class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=20)
    last_name  = forms.CharField(max_length=20)
    #school = forms.CharField(max_length=20, choices=get_schools())

    #school = forms.ChoiceField(choices=CHOICE, widget=forms.Select())
    major = forms.CharField(max_length=40)
    email = forms.CharField(max_length = 30)
    password1 = forms.CharField(max_length = 200,
                                 label='Password', 
                                 widget = forms.PasswordInput())
    password2 = forms.CharField(max_length = 200, 
                                 label='Confirm password',  
                                 widget = forms.PasswordInput())
    school = forms.CharField(max_length=150)


    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['school'] = forms.ChoiceField(
            choices=get_schools() )

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(RegistrationForm, self).clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # We must return the cleaned data we got from our parent.
        return cleaned_data

    # Customizes form validation for the username field.
    def clean_email(self):
        # Confirms that the username is not already present in the
        # User model database.
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("Must provide an email")
        if User.objects.filter(email__exact=email):
            raise forms.ValidationError("Username is already taken.")
        if not ".edu" in email:
            raise forms.ValidationError("Must be a .edu email address")

        # We must return the cleaned data we got from the cleaned_data
        # dictionary
        return email

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if not password:
            raise forms.ValidationError("Please enter a password")
        if len(password) < 8:
            raise forms.ValidationError("Must use longer password")
        return password

    def clean_password2(self):
        password = self.cleaned_data.get('password2')
        if not password:
            raise forms.ValidationError("Please enter to confirm password")
        if len(password) < 8:
            raise forms.ValidationError("Must use longer password")
        return password

class EditForm(forms.ModelForm):
    first_name = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'placeholder': 'Search'}))
    last_name  = forms.CharField(max_length=20, required=False)
    school = forms.CharField(max_length=20, required=False)
    major = forms.CharField(max_length=40, required=False)
    picture = forms.FileField(required=False, label='Change picture')
    class Meta:
        model = Student
        exclude = ('user', 'interests', 'linkedin', 'friends', 'picture_url', 'answer_rating', 'collab_rating', 'endorsements', 'age', 'notifications')

    def clean(self):
        cleaned_data = super(EditForm, self).clean()
        return cleaned_data

    def save(self, commit=True):
        return super(EditForm, self).save(commit=commit)

    def clean_picture(self):
        picture = self.cleaned_data['picture']
        if not picture:
            return None
        # if not picture.content_type or not picture.content_type.startswith('image'):
        #     raise forms.ValidationError('File type is not image')
        if picture.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError('File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
        return picture

class PostForm(forms.Form):
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
    # class Meta:
    #     model = Post
    #     exclude = {'group_name', 'location', 'student', 'date', 'comments', 'upvotes', 'classroom'}

class CommentForm(forms.Form):
    text = forms.CharField(max_length=300)
    attachment = forms.FileField(required=False, label="Attachment")
    attachment_name = forms.CharField(max_length=200, required=False)

    def clean(self):
        cleaned_data = super(CommentForm, self).clean()
        return cleaned_data

    def clean_attachment(self):
        attachment = self.cleaned_data['attachment']
        print self.cleaned_data['attachment']
        if not attachment:
            return None
        if attachment.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError('File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
        return attachment

