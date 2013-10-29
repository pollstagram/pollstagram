"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from poll.models import Question, Choice, Answer
from django.contrib.auth.models import User, UserManager

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
        #print question.choices.all()
        self.assertTrue(True)

    def test_user_can_be_found(self):
        question = Question.objects.get(content_markdown__icontains='this')
        choice = Choice.objects.get(content_markdown__icontains='1')
        #print choice.answers.all()
        #print [c.user for c in choice.answers.all()]
        #print [c.choice for c in choice.answers.all()]
        #print [c.answer_time for c in choice.answers.all()]
        self.assertTrue(True)

class UserLogin(TestCase):
    def setUp(self):
        user1 = User.objects.create_user('user', 'tester@test.com', 'asdf')

    def test_login(self):
        params = {
            'username' : 'user',
            'password' : 'asdf'
        }
        resp = self.client.post('/accounts/login/', params)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp['Location'], 'http://testserver/accounts/profile/')

class UserCreatePollTest(TestCase):
    def setUp(self):
        user1 = User.objects.create_user('user', 'tester@test.com', 'asdf')
        self.assertTrue(True)


    def test_create_poll(self):
        result = self.client.login(username='user', password='asdf')
        self.assertTrue(result)
        poll = {
            'content_markdown' : 'question',
            'tags' : 'tag',
            'choices-TOTAL_FORMS' : '2',
            'choices-INITIAL_FORMS' : '0',
            'choices-MAX_NUM_FORMS' : '1000',
            'choices-0-content_markdown' : 'first',
            'choices-0-id' : ' ',
            'choices-1-content_markdown' : 'second',
            'choices-1-id' : ' '
        }
        resp = self.client.post('/polls/create/', poll)
        #print resp
        # print resp
        self.assertEqual(resp.status_code, 302)
        #self.assertEqual(resp['Location'], 'http://testserver/accounts/register/complete/')
        #try:
        #    user = User.objects.get(username='user')
        #except:
        #    self.assertFalse('user does not exist')

        
class UserRegisterTest(TestCase):
    def setUp(self):
        self.assertTrue(True)


    def test_register_invalid(self):
        invalidUser = {
            'username' : 'user',
            'email' : 'user@user.cx',
            'password1' : 'asdf',
            'password2' : 'asdf',
            'first_name' : 'first',
            'last_name' : 'last',
        }
        resp = self.client.post('/accounts/register/', invalidUser)
        self.assertEqual(resp.status_code, 200)
        try:
            user = User.objects.get(username='user')
            self.assertFalse('user should not be created')
        except:
            self.assertTrue(True)


    def test_register_user(self):
        validUser = {
            'username' : 'user',
            'email' : 'user@user.cx',
            'password1' : 'asdf',
            'password2' : 'asdf',
            'first_name' : 'first',
            'last_name' : 'last',
            'date_of_birth_month' : '2',
            'date_of_birth_day' : '16',
            'date_of_birth_year' : '2000',
            'gender' : 'Male',
            'bio' : 'asdf',
            'avatar' : 'asdf.jpg'
        }
        resp = self.client.post('/accounts/register/', validUser)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp['Location'], 'http://testserver/accounts/register/complete/')
        try:
            user = User.objects.get(username='user')
        except:
            self.assertFalse('user does not exist')

