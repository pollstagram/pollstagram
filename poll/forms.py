from pagedown.widgets import AdminPagedownWidget, PagedownWidget 
from django.forms import Form, ModelForm, Textarea, CharField, TextInput, extras
from django.forms.models import inlineformset_factory
from registration.forms import RegistrationForm
from django import forms

from models import Question, Choice, Answer

class UserProfileForm(RegistrationForm):
    # For now, manually specify each additional form field
    # Note: look into using ModelForm for this, I'm not sure
    # how to integrate ModelForm with django-registration
    date_of_birth = forms.DateField(widget=extras.SelectDateWidget)
    gender = forms.CharField(max_length=255)
    bio = forms.CharField(max_length=255, widget=forms.Textarea)


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
