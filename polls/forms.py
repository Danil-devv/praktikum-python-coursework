from django import forms
from .models import Poll, Question, Choice

class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['title']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'question_type']

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text']

class QuestionChoiceForm(forms.Form):
    question_form = QuestionForm()
    choice_formset = forms.modelformset_factory(Choice, form=ChoiceForm, extra=1)
