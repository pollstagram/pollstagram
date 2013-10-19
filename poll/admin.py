from django.contrib import admin
from poll.models import Question, Choice, Answer
from poll.forms import QuestionForm, ChoiceForm

class ChoiceInline(admin.TabularInline):
    model = Choice
    form = ChoiceForm
    extra = 2

class QuestionAdmin(admin.ModelAdmin):
    form = QuestionForm
    readonly_fields = ('published_time',)
    fieldsets = [
        (None,               {'fields': ['content_markdown', 'tags',]}),
        ('Date information', {'fields': ['published_time'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('content_markdown', 'published_time')
    list_filter = ['published_time']
    search_fields = ['content_rawtext']
    date_hierarchy = 'published_time'
    
    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()

class ChoiceAdmin(admin.ModelAdmin):
    form = ChoiceForm

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Answer)