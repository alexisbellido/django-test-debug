import datetime
from django.test import TestCase
from django.db import IntegrityError
from survey.models import Survey

class SurveySaveTest(TestCase):
    def testClosesAutoset(self):
        pass
