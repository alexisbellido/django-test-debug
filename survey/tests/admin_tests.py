import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.handlers.wsgi import WSGIHandler
import twill
TWILL_TEST_HOST = 'twilltest'
twill.add_wsgi_intercept(TWILL_TEST_HOST, 80, WSGIHandler)

def reverse_for_twill(named_url):
    return 'http://' + TWILL_TEST_HOST + reverse(named_url)

class AdminSurveyTest(TestCase):
    def setUp(self):
        self.username = 'survey_admin'
        self.pw = 'pwpwpw'
        self.user = User.objects.create_user(self.username, '', self.pw)
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()
        self.assertTrue(self.client.login(username=self.username, password=self.pw), "Logging in user %s, pw %s failed." % (self.username, self.pw))

    def setDown(self):
        self.client.logout()

    #def testOne(self):
    #    self.assertEqual(1, 1)

    def testAddSurveyError(self):
        print reverse_for_twill('admin:survey_survey_add')
        post_data = {
            'title': u'Time Traveling',
            'opens': datetime.date.today(),
            'closes': datetime.date.today() - datetime.timedelta(1),
            'question_set-TOTAL_FORMS': 0,
            'question_set-INITIAL_FORMS': 0,
        }

        response = self.client.post(reverse('admin:survey_survey_add'), post_data)
        self.assertContains(response, "Opens date cannot come after closes date.")

    def testAddSurveyOK(self):
        post_data = {
            'title': u'Time Traveling',
            'opens': datetime.date.today(),
            'closes': datetime.date.today(),
            'question_set-TOTAL_FORMS': 0,
            'question_set-INITIAL_FORMS': 0,
        }
        response = self.client.post(reverse('admin:survey_survey_add'), post_data)
        self.assertRedirects(response, reverse('admin:survey_survey_changelist'))
