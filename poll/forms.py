from pagedown.widgets import AdminPagedownWidget 
from django import forms
from models import Question, Choice, Answer

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        widgets = {'content_markdown': AdminPagedownWidget(),}
        exclude = ('content_markup', 'content_rawtext',)
        
class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        widgets = {'content_markdown': AdminPagedownWidget(),}
        exclude = ('content_markup', 'content_rawtext',)
        
class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        exclude = ('user',)