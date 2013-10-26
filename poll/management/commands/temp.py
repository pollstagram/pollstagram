from django.core.management.base import BaseCommand, CommandError
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