import datetime
from django.db import models
from django.db.models import Max
#from django.core.urlresolvers import reverse

class ShellTests(object):
    """
    Manual setup of the database from the shell, recreate data like this:
    from survey.models import ShellTests
    s = ShellTests()
    s.setUp()
    """
    def setUp(self):
        # three surveys for yesterday, today and tomorrow
        today = datetime.date.today()
        oneday = datetime.timedelta(1)
        yesterday = today - oneday
        tomorrow = today + oneday
        Survey.objects.all().delete()
        Survey.objects.create(title="Yesterday", opens=yesterday, closes=yesterday)
        Survey.objects.create(title="Today", opens=today, closes=today)
        Survey.objects.create(title="Tomorrow", opens=tomorrow, closes=tomorrow)

        # survey for Television Trends, Chapter 7
        s = Survey.objects.create(title="Television Trends", opens=today, closes=tomorrow)
        q1 = Question(question='What is your favorite TV show?', survey = s)
        q1.save()
        q2 = Question(question='How many new shows will you try this Fall?', survey = s)
        q2.save()
        s.save()
        Answer.objects.create(answer='Comedy',question=q1)
        Answer.objects.create(answer='Drama',question=q1)
        Answer.objects.create(answer='Reality',question=q1)
        Answer.objects.create(answer='Hardly any: I already watch too much TV!',question=q2)
        Answer.objects.create(answer='Maybe 3-5',question=q2)
        Answer.objects.create(answer='I am a TV fiend, I will try them all at least once!',question=q2)

        # the survey for winning answers test
        from django.core.management import call_command
        call_command("loaddata", "survey/fixtures/test_winning_answers.json")

        # the surveys for the home view
        today = datetime.date.today()

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

class SurveyManager(models.Manager):
    def completed(self):
        return self.filter(closes__lt=datetime.date.today())

    def active(self):
        return self.filter(opens__lte=datetime.date.today()).filter(closes__gte=datetime.date.today())

    def upcoming(self):
        return self.filter(opens__gt=datetime.date.today())

class Survey(models.Model):
    title = models.CharField(max_length=60)
    opens = models.DateField()
    closes = models.DateField(blank=True)

    objects = SurveyManager()

    def save(self, **kwargs):
        if not self.pk and self.opens and not self.closes:
            self.closes = self.opens + datetime.timedelta(7)
        super(Survey, self).save(**kwargs)

    def __unicode__(self):
        return '%s' % self.title

    @models.permalink
    def get_absolute_url(self):
        # see https://docs.djangoproject.com/en/dev/ref/models/instances/#django.db.models.permalink
        # the permalink decorator is a high-level wrapper for reverse, which would be used like this:
        #return reverse('survey_detail', args= (self.pk,))
        # using a permalink for a URLconf entry with keyword arguments
        #return ('znb_blog_category_detail', (), {'slug': self.slug})
        # using a permalink for a URLconf entry with position arguments
        return ('survey_detail', (self.pk,))

class Question(models.Model):
    question = models.CharField(max_length=200)
    survey = models.ForeignKey(Survey)

    def winning_answers(self):
        max_votes = self.answer_set.aggregate(Max('votes')).values()[0]
        if max_votes and max_votes > 0:
            rv = self.answer_set.filter(votes=max_votes)
        else:
            rv = self.answer_set.none()
        return rv

    def __unicode__(self):
        return u'%s: %s' % (self.survey, self.question)

class Answer(models.Model):
    answer = models.CharField(max_length=200)
    question = models.ForeignKey(Question)
    votes = models.IntegerField(default=0)

    def __unicode__(self):
        return self.answer
