from django.core.management.base import BaseCommand, CommandError
from poll.models import Question, Choice, Answer
from django.contrib.auth.models import User
from voting.models import Vote

class Command(BaseCommand):
    def handle(self, *args, **options):
        u = User.objects.get(pk=1)
        c = Choice.objects.get(pk=7)
        q = Question.objects.get(pk=2)
        print q.results
        print q.user_has_answered(u)
        print c.percent_all_votes()
        print Vote.objects.get_score(q)
        qs = Question.objects.all()