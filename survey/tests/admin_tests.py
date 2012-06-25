import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import close_connection
from django.core import signals
from django.core.handlers.wsgi import WSGIHandler
from django.conf import settings
import twill
TWILL_TEST_HOST = 'twilltest'
from StringIO import StringIO


def reverse_for_twill(named_url):
    return 'http://' + TWILL_TEST_HOST + reverse(named_url)


class AdminTest(TestCase):
    def setUp(self):
        self.username = 'survey_admin'
        self.pw = 'pwpwpw'
        self.user = User.objects.create_user(self.username, '', self.pw)
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()
        self.assertTrue(self.client.login(username=self.username, password=self.pw), "Logging in user %s, pw %s failed." % (self.username, self.pw))


class AdminSurveyTwillTest(AdminTest):
    def setUp(self):
        super(AdminSurveyTwillTest, self).setUp()
        self.old_propagate = settings.DEBUG_PROPAGATE_EXCEPTIONS
        settings.DEBUG_PROPAGATE_EXCEPTIONS = True
        signals.request_finished.disconnect(close_connection)
        twill.set_output(StringIO())
        twill.add_wsgi_intercept(TWILL_TEST_HOST, 80, WSGIHandler)
        self.browser = twill.get_browser()
        self.browser.go(reverse_for_twill('admin:index'))
        twill.commands.formvalue(1, 'username', self.username)
        twill.commands.formvalue(1, 'password', self.pw)
        self.browser.submit()
        twill.commands.find('Welcome')

    def tearDown(self):
        self.browser.go(reverse_for_twill('admin:logout'))
        twill.remove_wsgi_intercept(TWILL_TEST_HOST, 80)
        signals.request_finished.connect(close_connection)
        settings.DEBUG_PROPAGATE_EXCEPTIONS = self.old_propagate

    def testAddSurveyError(self):
        self.browser.go(reverse_for_twill('admin:survey_survey_add'))
        twill.commands.formvalue(1, 'title', 'Time Traveling')
        twill.commands.formvalue(1, 'opens', str(datetime.date.today()))
        twill.commands.formvalue(1, 'closes', str(datetime.date.today() - datetime.timedelta(1)))
        self.browser.submit()
        twill.commands.url(reverse_for_twill('admin:survey_survey_add'))
        twill.commands.find("Opens date cannot come after closes date.")

    def testAddSurveyOK(self):
        self.browser.go(reverse_for_twill('admin:survey_survey_add'))
        twill.commands.formvalue(1, 'title', 'Not Time Traveling')
        twill.commands.formvalue(1, 'opens', str(datetime.date.today()))
        twill.commands.formvalue(1, 'closes', str(datetime.date.today()))
        self.browser.submit()
        twill.commands.url(reverse_for_twill('admin:survey_survey_changelist') + '$')


class AdminSurveyTest(AdminTest):
    def tearDown(self):
        self.client.logout()

    #def testOne(self):
    #    self.assertEqual(1, 1)

    def testAddSurveyError(self):
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
