from pagedown.widgets import AdminPagedownWidget, PagedownWidget 
from django.forms import Form, ModelForm, Textarea, CharField, TextInput, RadioSelect, extras
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User
from registration.forms import RegistrationForm
from django import forms

from models import Question, Choice, Answer

# Set arguments to widgets
GENDER_CHOICES = (('Male', 'Male'), ('Female', 'Female'))
YEARS = [year for year in range(2014, 1910, -1)]

class UserProfileForm(RegistrationForm):
    # For now, manually specify each additional form field
    # Note: look into using ModelForm for this, I'm not sure
    # how to integrate ModelForm with django-registration
    first_name = forms.CharField(min_length=2, max_length=20)
    last_name = forms.CharField(min_length=2, max_length=20)
    date_of_birth = forms.DateField(widget=extras.SelectDateWidget(years=YEARS))
    gender = forms.CharField(widget=RadioSelect(choices=GENDER_CHOICES))
    bio = forms.CharField(max_length=255, widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        # TEMP: test changing size of input boxes here (not sure if 
        # this is the best place to do it)
        self.fields['username'].widget.attrs['class'] = 'RegistrationTextInput'
	self.fields['email'].widget.attrs['class'] = 'RegistrationTextInput'
	self.fields['password1'].widget.attrs['class'] = 'RegistrationTextInput'
	self.fields['password2'].widget.attrs['class'] = 'RegistrationTextInput'
	self.fields['first_name'].widget.attrs['class'] = 'RegistrationTextInput'
	self.fields['last_name'].widget.attrs['class'] = 'RegistrationTextInput'
	self.fields['date_of_birth'].widget.attrs['class'] = 'RegistrationDateInput'
	self.fields['bio'].widget.attrs['class'] = 'RegistrationTextAreaInput'

class UserEditForm(forms.ModelForm):
    first_name = forms.CharField(min_length=2, max_length=20)
    last_name = forms.CharField(min_length=2, max_length=20)
    date_of_birth = forms.DateField(widget=extras.SelectDateWidget(years=YEARS))
    gender = forms.CharField(widget=RadioSelect(choices=GENDER_CHOICES))
    bio = forms.CharField(max_length=255, widget=forms.Textarea)

    class Meta:
        model = User
        exclude = ('username', 'password', 'last_login', 'date_joined', \
                   'user_permissions', 'is_staff', 'is_active', 'is_superuser', \
                   'groups',)

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        #self.fields['username'].widget = forms.HiddenInput()
	#self.fields['password'].widget = forms.HiddenInput()
	#self.fields['last_login'].widget = forms.HiddenInput()
        
	#self.fields['username'].required = False
	#self.fields['password'].required = False
	#self.fields['password2'].required = False
	#print self.fields


class QuestionSearchForm(Form): 
    keyword = CharField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Search', 'type': 'text'}))

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ('content_markdown', 'tags')
        widgets = {
            'content_markdown': AdminPagedownWidget(),
            'tags': TextInput(attrs={'class': 'form-control', 'placeholder': 'Tags', 'type': 'text'}),
        }

class ChoiceForm(ModelForm):
    class Meta:
        model = Choice
        fields = ('content_markdown',)
        widgets = {'content_markdown': Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Input choice...'}),}

class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        exclude = ('user',)
        
QuestionChoiceFormset = inlineformset_factory(Question, Choice, form=ChoiceForm, extra=2)
