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
from django_countries import CountryField
from registration.signals import user_registered
import datetime

# Create your models here.

class Question(models.Model):
    content_markdown = models.TextField(max_length=255, verbose_name=u'Content (markdown)')
    content_markup = models.TextField(max_length=255)
    content_rawtext = models.TextField(max_length=255)
    created_by = models.ForeignKey(User, related_name='questions')
    published_time = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager(blank=True)
    
    class Meta:
        ordering = ['-published_time']

    @staticmethod
    def sorted_by(criterion):
        if criterion == 'mostpopular':
            sorted_qs = sorted(Question.objects.all(), \
	                       key=lambda q: Vote.objects.get_score(q), \
			       reverse=True)
	else:
	    sorted_qs = Question.objects.all()
        return sorted_qs
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.choices.count() < 2:
            raise ValidationError('Each question must have 2 or more choices')
    
    def _ratings(self):
        """
        'score'     aggregated upvote/downvote score
        'num_votes' total number of votes
        """
        return Vote.objects.get_score(self)
    
    def save(self, *args, **kwargs):
        self.content_markup = markdown(self.content_markdown, ['codehilite'])
        self.content_rawtext = ''.join(BeautifulSoup(self.content_markup).findAll(text=True))
        super(Question, self).save(*args, **kwargs)

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

    def get_absolute_url(self):
        return u'/polls/{pk}/'.format(pk=self.id)    
        
    def __unicode__(self):
        return self.content_rawtext
    
    results = property(_results)
    ratings = property(_ratings)
    
class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices')
    content_markdown = models.TextField(max_length=255, verbose_name=u'Content (markdown)')
    content_markup = models.TextField(max_length=255)
    content_rawtext = models.TextField(max_length=255)
    
    def num_votes(self, _filter={}):
        if 'gender' in _filter:
            answers_filtered = [answer for answer in self.answers.all() \
	                        if answer.user.userprofile.gender == _filter['gender']]
            return answers_filtered
        return self.answers.count()
    
    def percent_all_votes(self):
        return 100*self.num_votes()/float(self.question.results['answers__count'])
    
    def user_has_chosen(self, user):
        return self.answers.filter(user=user).exists()
            
    def save(self, *args, **kwargs):
        self.content_markup = markdown(self.content_markdown, ['codehilite'])
        self.content_rawtext = ''.join(BeautifulSoup(self.content_markup).findAll(text=True))
        super(Choice, self).save(*args, **kwargs)    
        
    def __unicode__(self):
        return self.content_rawtext

class Answer(models.Model):
    choice = models.ForeignKey(Choice, related_name='answers')
    user = models.ForeignKey(User)
    answer_time = models.DateTimeField(auto_now_add=True)
    
    def user_has_answered_question(self):
        return self.choice.question.choices.exclude(answers=self).filter(answers__user=self.user).exists()
    
    # def clean(self):
    #     from django.core.exceptions import ValidationError
    #     if self.choice.question.choices.exclude(answers=self).filter(answers__user=self.user).exists():
    #         raise ValidationError('User has already voted for this question!')
    
    def get_absolute_url(self):
        return u'/polls/{pk}/results'.format(pk=self.choice.question.id)

    def __unicode__(self):
        return u'"{choice}" chosen by "{user}" at {time}'.format(choice=unicode(self.choice), user=unicode(self.user), time=self.answer_time)

class UserProfile(models.Model):
     user = models.OneToOneField(settings.AUTH_USER_MODEL, \
                                 related_name='userprofile')
     date_of_birth = models.DateField(null=True)
     gender = models.CharField(max_length=7)
     country = CountryField()  
     bio = models.TextField(max_length=255)
     avatar = models.FileField(upload_to='avatars')

     def __unicode__(self):
         return self.user
 
def user_registered_callback(sender, user, request, **kwargs):
    # Save first and last name for user (not 
    # saved by default)
    user.first_name = request.POST['first_name']
    user.last_name = request.POST['last_name']
    user.save()

    # Save custom user fields
    profile = UserProfile(user = user)
    birth_year = request.POST['date_of_birth_year']
    birth_month = request.POST['date_of_birth_month']
    birth_day = request.POST['date_of_birth_day']
    profile.date_of_birth = datetime.date(int(birth_year), 
                                          int(birth_month), 
					  int(birth_day))
    profile.gender = request.POST['gender']
    profile.bio = request.POST['bio']
    # Model handles saving of file to filesystem automatically
    # saves to upload_to argument
    print request.POST
    print request.FILES
    profile.avatar = request.FILES['avatar']
    profile.save()

user_registered.connect(user_registered_callback)
