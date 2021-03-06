from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.http import Http404
import datetime
from django.shortcuts import render_to_response, get_object_or_404
from survey.models import Survey
from survey.forms import QuestionVoteForm
from gen_utils.logutils import log_view, log_call
import logging
from django.db.models import F

@log_view
def home(request):
    #return HttpResponse("This is the home page. w00t!")
    today = datetime.date.today()
    active = Survey.objects.active()
    completed = Survey.objects.completed().filter(closes__gte = today - datetime.timedelta(14))
    upcoming = Survey.objects.upcoming().filter(opens__lte = today + datetime.timedelta(7))

    return render_to_response('survey/home.html',
            {'active_surveys': active,
             'completed_surveys': completed,
             'upcoming_surveys': upcoming},
            RequestContext(request)
            )

@log_view
def survey_thanks(request, pk):
    survey = get_object_or_404(Survey, pk=pk)
    return render_to_response('survey/thanks.html',
                              {'survey': survey},
                              RequestContext(request)
                              )

@log_view
def survey_detail(request, pk):
    survey = get_object_or_404(Survey, pk=pk)
    today = datetime.date.today()
    if survey.closes < today:
        #return HttpResponse('completed survey %s %s' % (survey.title, pk))
        return display_completed_survey(request, survey)
    elif survey.opens > today:
        raise Http404("%s does not open until %s; it is only %s" % (survey.title, survey.opens, today))
    else:
        #return HttpResponse('active survey %s %s' % (survey.title, pk))
        return display_active_survey(request, survey)

@log_call
def display_completed_survey(request, survey):
    return render_to_response('survey/completed_survey.html',
                              {'survey': survey},
                              RequestContext(request)
                              )

@log_call
def display_active_survey(request, survey):
    if request.method == 'POST':
        data = request.POST
    else:
        data = None

    qforms = []
    for i, q in enumerate(survey.question_set.all()):
        if q.answer_set.count() > 1:
            qforms.append(QuestionVoteForm(q, prefix=i, data=data))

    if request.method == 'POST':
        chosen_answers = []
        for qf in qforms:
            if not qf.is_valid():
                logging.debug("form failed validation: %r", qf.errors)
                break
            chosen_answers.append(qf.cleaned_data['answer'])
        else:
            for answer in chosen_answers:
                answer.votes = F('votes') + 1
                answer.save(force_update=True)
            #return HttpResponseRedirect(reverse('survey_home'))
            return HttpResponseRedirect(reverse('survey_thanks', args=(survey.pk,)))

    return render_to_response('survey/active_survey.html',
                              {'survey': survey, 'qforms': qforms},
                              context_instance = RequestContext(request),
                             )
