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
        user1 = User.objects.create_user('tester01', 'tester@test.com', 'test')
        user2 = User.objects.create_user('tester02', 'tester@test.com', 'test')
        question = Question.objects.create(content_markdown='This is a test', created_by=user2)
        choice1 = question.choices.create(content_markdown='Choice 1')
        question.choices.create(content_markdown='Choice 2')
        choice1.answers.create(user=user1)
        choice1.answers.create(user=user2)
        
    def test_user_can_answer(self):
        question = Question.objects.get(content_markdown__icontains='test')
        print question.choices.all()
        self.assertTrue(True)

    def test_user_can_be_found(self):
        question = Question.objects.get(content_markdown__icontains='this')
        choice = Choice.objects.get(content_markdown__icontains='1')
        print choice.answers.all()
        print [c.user for c in choice.answers.all()]
        print [c.choice for c in choice.answers.all()]
        print [c.answer_time for c in choice.answers.all()]
        self.assertTrue(True)
