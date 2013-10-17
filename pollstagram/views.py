from django.http import HttpResponse
from django.shortcuts import render
from poll.models import Question, Answer
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, CreateView
import os

class IndexView(ListView):
    model = Question
    template_name = 'list.html'
    context_object_name = 'questions'

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
                'pk': self.object.pk,
            }
            return self.render_to_json_response(data)
        else:
            return response

class AnswerCreateView(AjaxableResponseMixin, CreateView):
    model = Answer
    success_url = reverse_lazy('home')

def home(request):
    if 'search' in request.GET and 'keyword' in request.GET:
        keyword = request.GET['keyword']
        results = Question.objects.filter(content_rawtext__icontains = keyword)
    else:
        results =  Question.objects.all()
    return render(request, 'list.html', {'questions': results,})