from pagedown.widgets import AdminPagedownWidget 
from django import forms
from models import Question

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        widgets = {'content_markdown': AdminPagedownWidget(),}
        exclude = ['content_markup',]