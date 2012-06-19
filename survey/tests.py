import datetime
from django.test import TestCase
from django.db import IntegrityError
from survey.models import Survey, Question

class SurveySaveTest(TestCase):
    t = "New Year's Resolutions"
    sd = datetime.date(2009, 12, 28)

    def testClosesAutoset(self):
        """Tests for the Survey override method"""
        s = Survey.objects.create(title=self.t, opens=self.sd)
        self.assertEqual(s.closes, datetime.date(2010, 1, 4),
            "closes not autoset to 7 days after opens, expected %s but got %s" % (datetime.date(2010, 1, 4), s.closes))

    def testClosesHonored(self):
        """Verify closes is autoset correctly"""
        s = Survey.objects.create(title=self.t, opens=self.sd, closes=self.sd)
        self.assertEqual(s.closes, self.sd)

    def testClosesReset(self):
        """Verify closes is honored if specified"""
        s = Survey.objects.create(title=self.t, opens=self.sd)
        s.closes = None
        self.assertRaises(IntegrityError, s.save)

    def testTitleOnly(self):
        """Verify closes is only autoset during initial create"""
        self.assertRaises(IntegrityError, Survey.objects.create, title=self.t)

class QuestionWinningAnswersTest(TestCase):

    fixtures = ['test_winning_answers.json']

    def testClearWinner(self):
        q = Question.objects.get(question='Clear Winner')
        wa_qs = q.winning_answers()
        self.assertEqual(wa_qs.count(), 1)
        winner = wa_qs[0]
        self.assertEqual(winner.answer, 'Max Votes')

    def testTwoWayTie(self):
        q = Question.objects.get(question='2-Way Tie')
        wa_qs = q.winning_answers()
        self.assertEqual(wa_qs.count(), 2)
        for winner in wa_qs:
            self.assertTrue(winner.answer.startswith('Max Votes'))

    def testNoResponses(self):
        q = Question.objects.get(question='No Responses')
        wa_qs = q.winning_answers()
        self.assertEqual(wa_qs.count(), 0)

    def testNoAnswers(self):
        q = Question.objects.get(question='No Answers')
        wa_qs = q.winning_answers()
        self.assertEqual(wa_qs.count(), 0)

class SurveyManagerTest(TestCase):
    def setUp(self):
        today = datetime.date.today()
        oneday = datetime.timedelta(1)
        yesterday = today - oneday
        tomorrow = today + oneday
        Survey.objects.all().delete()
        Survey.objects.create(title="Yesterday", opens=yesterday, closes=yesterday)
        Survey.objects.create(title="Today", opens=today, closes=today)
        Survey.objects.create(title="Tomorrow", opens=tomorrow, closes=tomorrow)

    def testOne(self):
        self.assertEqual(1+1, 2)
