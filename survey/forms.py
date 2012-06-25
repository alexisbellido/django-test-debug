from django import forms
#from survey.models import Question

class QuestionVoteForm(forms.Form):
    answer = forms.ModelChoiceField(widget=forms.RadioSelect)
    #answer = forms.ModelChoiceField(widget=forms.RadioSelect, queryset=Question.objects.all())

    def __init__(self, question, *args, **kwargs):
        super(QuestionVoteForm, self).__init__(*args, **kwargs)
        self.fields['answer'].queryset = question.answer_set.all()
