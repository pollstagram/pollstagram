from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from poll.models import UserProfile
from poll.models import Question, Choice, Answer
from poll.forms import QuestionForm, ChoiceForm
import reversion

class ChoiceInline(admin.TabularInline):
    model = Choice
    form = ChoiceForm
    extra = 2

class QuestionAdmin(reversion.VersionAdmin):
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

class ChoiceAdmin(reversion.VersionAdmin):
    form = ChoiceForm

# Define an inline admin descriptor for the UserProfile model
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'userprofile'

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Answer)
# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
