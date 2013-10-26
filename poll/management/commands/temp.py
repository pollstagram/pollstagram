from dango.core.management.base import BaseCommand, CommandError
from poll.models import Question, Choice, Answer
from django.contrib.auth.models import User
from voting.models import Vote
import pprint, reversion

class Command(BaseCommand):
    def handle(self, *args, **options):
        pprint.pprint([(q.content_markdown, q.tags.all()) for q in Question.objects.get(pk=2).tags.similar_objects()])
        print Question.objects.filter(tags__name='trivia')
        q = Question.objects.get(pk=23)
        print dir(reversion.get_unique_for_object(q)[0].object_repr)
        u = User.objects.get(pk=1)
        c = Choice.objects.get(pk=7)
        q = Question.objects.get(pk=2)
        print q.results
        print q.user_has_answered(u)
        print c.percent_all_votes()
        print Vote.objects.get_score(q)
        qs = Question.objects.all()