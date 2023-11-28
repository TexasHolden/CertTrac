from django import forms
from .models import Tutor, Takes, Session, Subtopic

class TutorForm(forms.ModelForm):
    class Meta:
        model = Tutor
        fields = [
            'first_name',
            'last_name',
            'email',
            'date_hired',
            'level',
            'logged_25_hours_level_1',
            'level_1_completion_date',
            'logged_25_hours_level_2',
            'review_level_1_completed',
            'level_2_completion_date',
        ]


class TutorLevelForm(forms.ModelForm):
    class Meta:
        model = Tutor
        fields = [
            #'first_name',
            #'last_name',
            'level',
            'level_1_completion_date',
            'level_2_completion_date',
        ]


class TakesForm(forms.ModelForm):
    class Meta:
        model = Takes
        fields = []


class SessionForm(forms.ModelForm):
    subtopic = forms.ModelChoiceField(queryset = Subtopic.objects.all(), to_field_name = 'name', label = 'Subtopic')
    semester = forms.CharField(widget=forms.TextInput())
    class Meta:
        model = Session
        fields = ['subtopic', 'semester', 'in_person_hours', 'async_hours']

    def __init__(self, *args, **kwargs):
        super(SessionForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs and kwargs['instance']:
            initial_subtopic_name = kwargs['instance'].subtopic.name
            self.initial['subtopic'] = initial_subtopic_name