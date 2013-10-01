from django.contrib import admin
from poll.models import *

admin.site.register(Tag)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Vote)
admin.site.register(Answer)