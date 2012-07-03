from django import forms
#from survey.models import Question

class QuestionVoteForm(forms.Form):
    answer = forms.ModelChoiceField(widget=forms.RadioSelect, 
                                    queryset=None, 
                                    empty_label=None,
                                    error_messages={'required': 'Please select an answer below:'})

    def __init__(self, question, *args, **kwargs):
        super(QuestionVoteForm, self).__init__(*args, **kwargs)
        self.fields['answer'].queryset = question.answer_set.all()
        self.fields['answer'].label = question.question
        self.error_class = PlainErrorList


from django.forms.util import ErrorList


class PlainErrorList(ErrorList):
    def __unicode__(self):
        return u'%s' % ' '.join([e for e in self])

        
