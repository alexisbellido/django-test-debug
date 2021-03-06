from django.conf.urls import patterns, include, url

urlpatterns = patterns('survey.views',
    url(r'^$', 'home', name='survey_home'),
    url(r'^(?P<pk>\d+)/$', 'survey_detail', name='survey_detail'),
    url(r'^thanks/(?P<pk>\d+)/$', 'survey_thanks', name='survey_thanks'),
)
