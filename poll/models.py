from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Tag(models.Model):
    title = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.title

class Question(models.Model):
    title = models.CharField(max_length=255)
    content_markdown = models.TextField(blank=True)
    content_markup = models.TextField(blank=True)
    published_time = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, null=True, blank=True)
    
    def __unicode__(self):
        return self.title
    
class Choice(models.Model):
    question = models.ForeignKey(Question)
    content = models.TextField(max_length=255)    
    
    def __unicode__(self):
        return self.content    
        
class Vote(models.Model):
    question = models.ForeignKey(Question)
    user = models.ForeignKey(User)
    vote_time = models.DateTimeField(auto_now_add=True)
    positive = models.BooleanField()
    
    def __unicode__(self):
        return self.question
        
class Answer(models.Model):
    question = models.ForeignKey(Question)
    user = models.ForeignKey(User)
    answer_time = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.question
        
class BinaryAnswer(Answer):
    pass
    
class MCQAnswer(Answer):
    pass