from pagedown.widgets import AdminPagedownWidget, PagedownWidget 
from django.forms import ModelForm, Textarea
from django.forms.models import inlineformset_factory

from models import Question, Choice, Answer

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ('content_markdown', 'tags')
        widgets = {'content_markdown': AdminPagedownWidget(),}

class ChoiceForm(ModelForm):
    class Meta:
        model = Choice
        fields = ('content_markdown',)
        widgets = {'content_markdown': Textarea(attrs={'rows':3, 'cols':10}),}
        

class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        exclude = ('user',)
        
QuestionChoiceFormset = inlineformset_factory(Question, Choice, form=ChoiceForm, extra=2)