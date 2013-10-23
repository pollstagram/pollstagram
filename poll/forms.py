from pagedown.widgets import AdminPagedownWidget, PagedownWidget 
from django.forms import Form, ModelForm, Textarea, CharField, TextInput
from django.forms.models import inlineformset_factory

from models import Question, Choice, Answer

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