from django.http import HttpResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from extra_views import InlineFormSet, CreateWithInlinesView, UpdateWithInlinesView, NamedFormsetsMixin
from extra_views.generic import GenericInlineFormSet
import os, json, reversion
from reversion.helpers import generate_patch_html
from django.forms.formsets import all_valid
from datetime import datetime, date, time
from django.db.models import Sum, Count, Max, Min

from django.contrib.auth.models import User
from poll.models import Question, Choice, Answer, UserProfile
from datetime import datetime
from poll.forms import QuestionForm, AnswerForm, ChoiceForm, QuestionChoiceFormset, QuestionSearchForm, \
                       UserEditForm
from itertools import tee, izip

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)

class ChoiceInline(InlineFormSet):
    model = Choice
    form_class = ChoiceForm

class PollUpdateView(NamedFormsetsMixin, UpdateWithInlinesView):
    model = Question
    form_class = QuestionForm
    inlines = [ChoiceInline,]
    inlines_names = ['choices']

class PollCreateView(NamedFormsetsMixin, CreateWithInlinesView):
    model = Question
    form_class = QuestionForm
    inlines = [ChoiceInline,]
    inlines_names = ['choices']

    def forms_valid(self, form, inlines):
        form.instance.created_by = self.request.user
        return super(PollCreateView, self).forms_valid(form, inlines)

class PollDeleteView(DeleteView):
    model = Question
    success_url = reverse_lazy('polls_index')

class IndexView(ListView):
    model = Question
    context_object_name = 'questions'
    paginate_by = 3
    form_class = QuestionSearchForm
    template_name = 'poll/question_list.html'
    
    def get_queryset(self):
        questions = Question.objects.all()
	    
        if self.request.GET:
            form = self.form_class(self.request.GET)
        else:
            form = self.form_class()
	    
	    # Handle different possible orderings of question list
	    if 'sortby' in self.request.GET:
	        questions = questions.sorted_by(self.request.GET['sortby'])
	    
        if 'tag' in self.kwargs:
            tag_list = self.kwargs['tag'].split('+')
            questions = questions.filter(tags__name__in=tag_list).distinct()
        if form.is_valid():
            questions = questions.filter(content_rawtext__icontains=form.cleaned_data['keyword'])
        return questions

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        if 'sortby' in self.request.GET:
            context['sort_by'] = "&sortby=%s" % self.request.GET['sortby']
        if self.request.GET:
            context['search_form'] = self.form_class(self.request.GET)
        else: 
            context['search_form'] = self.form_class()
        
        questions = Question.objects.all()
        today_min = datetime.combine(date.today(), time.min)
        today_max = datetime.combine(date.today(), time.max)
        context['stats'] = {}
        context['stats']['total'] = questions.count()
        context['stats']['today'] = questions.filter(published_time__range=(today_min, today_max)).count()
        context['stats']['answered'] = questions.filter(choices__answers__isnull=False).count()
        
        return context

class UserListView(ListView):
    model = User
    context_object_name = 'users'
    paginate_by = 10
    template_name = 'poll/user_list.html'
    #form_class = QuestionSearchForm
    
    #def get_queryset(self):
    #    form = self.form_class(self.request.GET)
    #    users = User.objects.all()
    #    if form.is_valid():
    #        return users.filter(content_rawtext__icontains=form.cleaned_data['keyword'])
    #    return users

    #def get_context_data(self, **kwargs):
    #    context = super(IndexView, self).get_context_data(**kwargs)
    #    if self.request.GET:
    #        context['search_form'] = QuestionSearchForm(self.request.GET)
    #    else: 
    #        context['search_form'] = QuestionSearchForm()
    #    return context

class PollDetailView(DetailView):
    model = Question
    context_object_name = 'question'

    def get_context_data(self, **kwargs):
        context = super(PollDetailView, self).get_context_data(**kwargs)
        context['pie_data'] = [[', '.join(choice.content_rawtext.splitlines()), choice.num_votes()] for choice in self.get_object().choices.all()]
        context['versions'] = reversion.get_unique_for_object(self.get_object())
        return context
        
class PollRevisionDetailView(PollDetailView):
    template_name = 'poll/question_revision.html'

    def get_context_data(self, **kwargs):
        context = super(PollRevisionDetailView, self).get_context_data(**kwargs)
        context['diffs'] = []
        for a, b in pairwise(context['versions']):
            temp = {}
            temp['related'] = []
            for i, (c, d) in enumerate(zip(a.revision.version_set.all(), b.revision.version_set.all())):
                diff_patch = generate_patch_html(d, c, 'content_markdown', cleanup="semantic")
                if not i:
                    temp['primary'] = (diff_patch, c)
                else:
                    temp['related'].append((diff_patch, c))
            context['diffs'].append(temp)
        return context

class PollResultsView(DetailView):
    model = Question
    template_name = 'poll/question_result.html'
    context_object_name = 'question'

class UserDetailView(DetailView):
    model = User
    slug_field = 'username'
    template_name = 'poll/user_detail.html'
    context_object_name = 'user_detail'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class UserUpdateView(UpdateView):
    form_class = UserEditForm
    model = User
    slug_field = 'username'
    template_name = 'poll/user_edit.html'
    context_object_name = 'user_detail'

    def get_success_url(self):
        return reverse_lazy('user_detail', kwargs={'slug': self.kwargs['slug']})

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['form'] = UserEditForm(initial={'username': context['user_detail'].username,
						'email': context['user_detail'].email,
	                                        'first_name': context['user_detail'].first_name, 
						'last_name': context['user_detail'].last_name,
						'date_of_birth': context['user_detail'].userprofile.date_of_birth,
						'gender': context['user_detail'].userprofile.gender,
						'bio': context['user_detail'].userprofile.bio,})
        #context['action'] = reverse_lazy('user_detail', kwargs={'slug': context['user_detail'].username})
        return context

    def form_valid(self, form):
        # Manually specifying saving logic
        user = User.objects.get(username=self.kwargs['slug'])
	user.first_name = form.cleaned_data['first_name']
	user.last_name = form.cleaned_data['last_name']
	user.email = form.cleaned_data['email']
	#print form.cleaned_data
	user.save()

	# Save custom fields
	userprofile = UserProfile.objects.get(user=user)
        userprofile.date_of_birth = form.cleaned_data['date_of_birth']
	userprofile.gender = form.cleaned_data['gender']
	userprofile.bio = form.cleaned_data['bio']
	userprofile.save()
	return super(UserUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        #print "FORM INVALID"
        user = User.objects.get(username=self.kwargs['slug'])
        user.first_name = form.cleaned_data['first_name']
        #print "USER FIRST_NAME: " + user.first_name
	#print form.errors
	#print form.cleaned_data
	#print self.request.POST

        return super(UserUpdateView, self).form_invalid(form)



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

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AnswerCreateView, self).form_valid(form)
        
    def get_success_url(self):
        return reverse('poll_detail', args=(self.object.choice.question.id,))
        
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
