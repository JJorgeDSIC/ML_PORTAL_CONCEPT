from django import forms

class TrainingFileForm(forms.Form):
    docfile = forms.FileField()

class TestFileForm(forms.Form):
    docfile = forms.FileField()
