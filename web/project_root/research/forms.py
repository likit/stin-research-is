from django import forms
from .models import Project


class ProjectSearchForm(forms.Form):
    query = forms.CharField()