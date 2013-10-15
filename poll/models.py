from django.db import models
from django.contrib.auth.models import User
from markdown import markdown
from taggit.managers import TaggableManager
from django.conf import settings

# Create your models here.

class Question(models.Model):
    content_markdown = models.TextField(max_length=255)
    content_markup = models.TextField(max_length=255)
    created_by = models.ForeignKey(User, null=True)
    published_time = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager()
    
    class Meta:
        ordering = ['-published_time']
    
    def save(self): 
        self.content_markup = markdown(self.content_markdown, ['codehilite']) 
        super(Question, self).save()
        
    def __unicode__(self):
        return self.content_markdown
    
class Choice(models.Model):
    question = models.ForeignKey(Question)
    content_markdown = models.TextField(max_length=255)
    content_markup = models.TextField(max_length=255)
    
    def save(self): 
        self.content_markup = markdown(self.content_markdown, ['codehilite']) 
        super(Choice, self).save()    
        
    def __unicode__(self):
        return self.content_markdown    

class Answer(models.Model):
    question = models.ForeignKey(Question)
    user = models.ForeignKey(User)
    answer_time = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.question
 
# class UserProfile(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL)
#     date_of_birth = models.DateField(null=True)
#     gender = models.CharField(max_lengh=255)
#     location = models.CharField(max_length=255)  
#     bio = models.TextField(max_length=255)
#     # avatar
        
class BinaryAnswer(Answer):
    pass
    
class MCQAnswer(Answer):
    pass