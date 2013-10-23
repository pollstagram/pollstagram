from pagedown.widgets import AdminPagedownWidget, PagedownWidget 
from django.forms import Form, ModelForm, Textarea, CharField
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, ButtonHolder, Submit, Field

from models import Question, Choice, Answer

class QuestionSearchForm(Form):
    keyword = CharField()
    
    def __init__(self, *args, **kwargs):
        super(QuestionSearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'navbar-form navbar-right'
        self.helper.form_role = 'search'
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Div(
                Field('keyword'),
                css_id = 'form-group'
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='btn btn-default')
            )
        )

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