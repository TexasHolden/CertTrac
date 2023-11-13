from django import forms
from .models import Tutor, Takes

class TutorForm(forms.ModelForm):
    class Meta:
        model = Tutor
        fields = '__all__'


class TakesForm(forms.ModelForm):
    class Meta:
        model = Takes
        fields = '__all__'
        #widgets = {
            #'tutor': forms.Select(attrs={'class': 'form-control'}),
            #'subtopic': forms.Select(attrs={'class': 'form-control'}),
        #}


class TutorSearchForm(forms.Form):
    search_query = forms.CharField(max_length=100, label='Search for a Tutor')



class SearchTakesForm(forms.Form):
    tutor = forms.CharField(max_length=100)
    subtopic = forms.CharField(max_length=100)
    date = forms.DateField()
