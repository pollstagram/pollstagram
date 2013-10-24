from django.db import models
from django.db.models import Sum, Count, Max, Min
from django.contrib.auth.models import User
from markdown import markdown
from taggit.managers import TaggableManager
from django.conf import settings
from BeautifulSoup import BeautifulSoup
from django.db.models.signals import post_save
from voting.models import Vote
import math

# Create your models here.

class Question(models.Model):
    content_markdown = models.TextField(max_length=255, verbose_name=u'Content (markdown)')
    content_markup = models.TextField(max_length=255)
    content_rawtext = models.TextField(max_length=255)
    created_by = models.ForeignKey(User, related_name='questions')
    published_time = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager()
    
    class Meta:
        ordering = ['-published_time']
    
    def _ratings(self):
        """
        'score'     aggregated upvote/downvote score
        'num_votes' total number of votes
        """
        return Vote.objects.get_score(self)
    
    def save(self):
        self.content_markup = markdown(self.content_markdown, ['codehilite'])
        self.content_rawtext = ''.join(BeautifulSoup(self.content_markup).findAll(text=True))
        super(Question, self).save()

    def _results(self):
        """
        'answers__count'     total number of answers
        'num_answers__max'  number of answers of the most chosen answer of the question
        'num_answers__min'  number of answers of the least chosen answer of the question
        """
        result = self.choices.aggregate(Count('answers'))
        result.update(self.choices.annotate(num_answers=Count('answers')).aggregate(Max('num_answers'), Min('num_answers')))
        return result
        
    def user_has_answered(self, user):
        return self.choices.filter(answers__user=user).exists()
        
    def choice_entropy(self):
        N = self.results['answers__count']
        ps = [c.num_votes()/float(N) for c in self.choices.all()]
        return sum([-p*math.log(p) for p in ps if p])
        # choises = Choise.object.filter(question = self.id)
        
    def last_active(self):
        pass    
        
    def __unicode__(self):
        return self.content_rawtext
    
    results = property(_results)
    ratings = property(_ratings)
    
class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices')
    content_markdown = models.TextField(max_length=255, verbose_name=u'Content (markdown)')
    content_markup = models.TextField(max_length=255)
    content_rawtext = models.TextField(max_length=255)
    
    def num_votes(self):
        return self.answers.count()
    
    def percent_all_votes(self):
        return 100*self.num_votes()/float(self.question.results['answers__count'])
    
    def user_has_chosen(self, user):
        return self.answers.filter(user=user).exists()
            
    def save(self):
        self.content_markup = markdown(self.content_markdown, ['codehilite'])
        self.content_rawtext = ''.join(BeautifulSoup(self.content_markup).findAll(text=True))
        super(Choice, self).save()    
        
    def __unicode__(self):
        return self.content_rawtext

class Answer(models.Model):
    choice = models.ForeignKey(Choice, related_name='answers')
    user = models.ForeignKey(User)
    answer_time = models.DateTimeField(auto_now_add=True)
    
    def get_absolute_url(self):
        return u'/polls/{pk}/results'.format(pk=self.choice.question.id)

    def __unicode__(self):
        return u'"{choice}" chosen by "{user}" at {time}'.format(choice=unicode(self.choice), user=unicode(self.user), time=self.answer_time)

class UserProfile(models.Model):
     user = models.OneToOneField(settings.AUTH_USER_MODEL)
     date_of_birth = models.DateField(null=True)
     gender = models.CharField(max_length=255)
     location = models.CharField(max_length=255)  
     bio = models.TextField(max_length=255)
     # TODO: avatar??
# 
# def create_user_profile(sender, instance, created, **kwargs):  
#      if created:  
#          profile, created = UserProfile.objects.get_or_create(user=instance)   
# 
# post_save.connect(create_user_profile, sender=User) 
        
class BinaryAnswer(Answer):
    pass
    
class MCQAnswer(Answer):
    pass
