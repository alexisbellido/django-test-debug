from django.http import HttpResponse

def home(request):
    return HttpResponse("This is the home page. w00t!")

def survey_detail(request, pk):
    return HttpResponse("This is the survey detail page for survey with pk=%s" % pk)
