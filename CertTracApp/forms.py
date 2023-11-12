from django import forms
from .models import TutorHours

class TutorHoursForm(forms.ModelForm):
    class Meta:
        model = TutorHours
        fields = ['tutor', 'class_tutored', 'hours_tutored', 'date']
