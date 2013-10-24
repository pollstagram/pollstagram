"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from poll.models import Question, Choice, Answer
from django.contrib.auth.models import User

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

class UserAnswerTest(TestCase):
    def setUp(self):
        User.objects.create_user('tester01', 'tester@test.com', 'test')
        user2 = User.objects.create_user('tester02', 'tester@test.com', 'test')
        question = Question.objects.create(content_markdown='This is a test', created_by=user2)
        question.choices.create(content_markdown='Choice 1')
        question.choices.create(content_markdown='Choice 2')
        
    def test_user_can_answer(self):
        question = Question.objects.get(content_markdown__icontains='test')
        print question.choices.all()
        self.assertTrue(True)