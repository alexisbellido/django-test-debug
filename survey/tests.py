import datetime
from django.test import TestCase
from django.db import IntegrityError
from survey.models import Survey

class SurveySaveTest(TestCase):
    t = "New Year's Resolutions"
    sd = datetime.date(2009, 12, 28)

    def testClosesAutoset(self):
        pass

    def testClosesHonored(self):
        pass

    def testClosesReset(self):
        pass

    def testTitleOnly(self):
        pass
