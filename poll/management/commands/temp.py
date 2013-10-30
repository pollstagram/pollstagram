from django.core.management.base import BaseCommand, CommandError
from poll.models import Question, Choice, Answer
from voting.models import Vote
from django.contrib.auth.models import User
from voting.models import Vote
from reversion.helpers import generate_patch_html
import pprint, reversion
from itertools import tee, izip
from django.db.models import Sum, Count, Max, Min
from random import randrange

class Dummy(object):
    pass

dummy = Dummy()
dummy.field_dict = {}
dummy.field_dict['content_markdown'] = ''

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)

class Command(BaseCommand):
        
    def handle(self, *args, **options):
        
        questions = Question.objects.all()
        for i in xrange(100):
            user, created = User.objects.get_or_create(username='tester{num}'.format(num=i), first_name='Tester', last_name='Number {num}'.format(num=i),  email='tester{num}@test.com'.format(num=i), password='test')
            for question in questions:
                Vote.objects.record_vote(question, user, randrange(2)-1)
                num_choices = question.choices.count()
                choice = question.choices.all()[randrange(num_choices)]
                Answer.objects.get_or_create(choice=choice, user=user)
        exit(0)
        
        # q = Question.objects.get(pk=24)
        # choices = q.choices.all()
        # user = User.objects.get(pk=1)
        # a = Answer.objects.get_or_create(user=user, choice=choices[0])[0]
        # print a.choice.question.choices.exclude(answers=a).filter(answers__user=user)
        # # a.full_clean()
        # b = Answer.objects.get_or_create(user=user, choice=choices[2])[0]
        # print b.choice.question.choices.exclude(answers=b).filter(answers__user=user)
        # # b.full_clean()
        # print b.choice.question.choices.filter(answers__user=user)
        # exit(0)
        questions = Question.objects.all()
        print questions[0].choices.answers.all()
        exit(0)
        unanswered = questions.filter(choices__answers__isnull=True).aggregate(Count('choices__answers'))
        print unanswered
        exit(0)
        
        q = Question.objects.get(pk=27)
        context = {}
        context['versions'] = reversion.get_unique_for_object(q)
        print dir(context['versions'][0].revision)
        exit(0)
        print context['versions'][0].revision.date_created
        context['diffs'] = []

        for a in context['versions'][-1].revision.version_set.all():
            print generate_patch_html(dummy, a, 'content_markdown', cleanup="semantic")
            
        for i, (a, b) in enumerate(pairwise(reversed(context['versions']))):
            temp = {}
            temp['related'] = []
            for j, (c, d) in enumerate(zip(a.revision.version_set.all(), b.revision.version_set.all())):
                diff_patch = generate_patch_html(c, d, 'content_markdown', cleanup="semantic")
                if not j:
                    temp['primary'] = (diff_patch, d)
                else:
                    temp['related'].append((diff_patch, d))
            context['diffs'].append(temp)
        
        pprint.pprint(context)
        exit(0)
        q = Question.objects.get(pk=24)
        for i, (a, b) in enumerate(pairwise(reversed(reversion.get_unique_for_object(q)))):
            for c, d in zip(a.revision.version_set.all(), b.revision.version_set.all()):
                print generate_patch_html(c, d, 'content_markdown', cleanup="semantic")
        
        exit(0)
        d = reversion.get_unique_for_object(q)[0]
        print d.revision.version_set.all()
        exit(0)
        a, b = reversion.get_unique_for_object(q)[0:2]
        print dir(b)
        print a.object_version.object.choices.all()
        print b.object_version.object.choices.all()
        
        print generate_patch_html(a, b, 'content_markdown', cleanup="semantic")
        # pprint.pprint([(q.content_markdown, q.tags.all()) for q in Question.objects.get(pk=2).tags.similar_objects()])
        #         print Question.objects.filter(tags__name='trivia')
        #         q = Question.objects.get(pk=23)
        #         print dir(reversion.get_unique_for_object(q)[0].object_repr)
        #         u = User.objects.get(pk=1)
        #         c = Choice.objects.get(pk=7)
        #         q = Question.objects.get(pk=2)
        #         print q.results
        #         print q.user_has_answered(u)
        #         print c.percent_all_votes()
        #         print Vote.objects.get_score(q)
        #         qs = Question.objects.all()