import datetime
from django.test import TestCase
from survey.models import Survey

class SurveyHomeTest(TestCase):
    def setUp(self):
        today = datetime.date.today()
        Survey.objects.all().delete()

        d = today - datetime.timedelta(15)
        Survey.objects.create(title="Too Old", opens=d, closes=d)

        d += datetime.timedelta(1)
        Survey.objects.create(title="Completed 1", opens=d, closes=d)

        d = today - datetime.timedelta(1)
        Survey.objects.create(title="Completed 2", opens=d, closes=d)
        Survey.objects.create(title="Active 1", opens=d)
        Survey.objects.create(title="Active 2", opens=today)

        d = today + datetime.timedelta(1)
        Survey.objects.create(title="Upcoming 1", opens=d)

        d += datetime.timedelta(6)
        Survey.objects.create(title="Upcoming 2", opens=d)

        d += datetime.timedelta(1)
        Survey.objects.create(title="Too Far Out", opens=d)

    def testHome(self):
        from django.core.urlresolvers import reverse
        response = self.client.get(reverse('survey_home'))
        #self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Completed", count=2)
        self.assertContains(response, "Active", count=2)
        self.assertContains(response, "Upcoming", count=2)
        self.assertNotContains(response, "Too Old")
        self.assertNotContains(response, "Too Far Out")

    #def testOne(self):
    #    self.assertEqual(1, 1)
