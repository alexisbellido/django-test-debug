import datetime
from django.test import TestCase
from django.db import IntegrityError
from survey.models import Survey

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
