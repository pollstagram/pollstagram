from django.http import HttpResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView
from django.http import HttpResponseRedirect
import os, json

from poll.models import Question, Answer
from poll.forms import QuestionForm, AnswerForm, QuestionChoiceFormset, QuestionSearchForm

class IndexView(ListView):
    model = Question
    context_object_name = 'questions'
    paginate_by = 3
    form_class = QuestionSearchForm
    
    def get_queryset(self):
        form = self.form_class(self.request.GET)
        if form.is_valid():
            return Question.objects.filter(content_rawtext__icontains=form.cleaned_data['keyword'])
        return Question.objects.all()

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        if self.request.GET:
            context['search_form'] = QuestionSearchForm(self.request.GET)
        else: 
            context['search_form'] = QuestionSearchForm()
        return context

class PollDetailView(DetailView):
    model = Question
    context_object_name = 'question'

class PollResultsView(DetailView):
    model = Question
    template_name = 'poll/question_result.html'
    context_object_name = 'question'

class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return self.render_to_json_response(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.choice.question.content_rawtext,
            }
            return self.render_to_json_response(data)
        else:
            return response

class AnswerCreateView(AjaxableResponseMixin, CreateView):
    form_class = AnswerForm
    model = Answer
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AnswerCreateView, self).form_valid(form)

class PollCreateView(CreateView):
    form_class = QuestionForm
    model = Question
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        context = self.get_context_data()
        question_choice_form = context['question_choice_formset']
        if question_choice_form.is_valid():
            self.object = form.save()
            question_choice_form.instance = self.object
            question_choice_form.save()
            return HttpResponseRedirect('/')
        else:
            return self.render_to_response(self.get_context_data(form=form))
            
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(PollCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['question_choice_formset'] = QuestionChoiceFormset(self.request.POST)
        else: 
            context['question_choice_formset'] = QuestionChoiceFormset()
        return context
        
def home(request):
    if 'search' in request.GET and 'keyword' in request.GET:
        keyword = request.GET['keyword']
        question_list = Question.objects.filter(content_rawtext__icontains = keyword)
    else:
        question_list =  Question.objects.all()
    # Only display a subset of questions each page (pagination)
    paginator = Paginator(question_list, 5)
    page = request.GET.get('page')
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        questions = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        questions = paginator.page(paginator.num_pages)

    return render(request, 'list.html', {'questions': questions,})
