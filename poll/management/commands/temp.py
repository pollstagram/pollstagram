from django.core.management.base import BaseCommand, CommandError
from poll.models import Question, Choice, Answer

class Command(BaseCommand):
    def handle(self, *args, **options):
        q = Question.objects.get(pk=1)
        print q.total_answers()