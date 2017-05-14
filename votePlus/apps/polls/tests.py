import datetime
from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse
from .models import Question, Choice

class QuestionMethodTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() should return False for questions published with a 
        future date
        :return: True or False
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertEqual(future_question.was_published_recently(), False)


    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() should return False for question
        whose pub_date is older than 1 day
        :return: 
        """
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date=time)
        self.assertEqual(old_question.was_published_recently(), False)


    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() should return True for questions whose
        pub_date is within the last day
        :return: 
        """
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_question = Question(pub_date=time)
        self.assertEqual(recent_question.was_published_recently(), True)

def create_question(question_text, days):
    """
    creates a question with the given 'question_text' published the given number of
    'days' offset to now (negative for questions published in the past, positive for questions
    that are yet to be published)
    :param question_text: 
    :param days: 
    :return: 
    """
    time = timezone.now() + datetime.timedelta(days=day)
    return Question.objects.create(question_text=question_text,
                                   pub_date=time)


class QuestionViewTests(TestCase):
    def test_index_view_with_no_question(self):
        """
        if no question available, an appropriate message should be displayed
        :return: 
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_a_past_question(self):
        """
        questions with a pub_date in the past should be displayed on the index page
        :return: 
        """
        create_question(question_text='Best OS for developers', days=-30)
        response =self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
                response.context['latest_question_list'],
                ['<Question:Best OS for developers' ]
                )

    def test_index_view_with_a_future_question(self):
        """
        Questions with a pub_date in the future should not be displayed on the index page
        :return: 
        """
        create_question(question_text='What language will be popular in 2020', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available",
                            status_code=200)

        self.assertQuerysetEqual(response.context['latest_question_list'], [])


class ChoiceMethodTests(TestCase):
    pass