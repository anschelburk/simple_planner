from django import forms
from .models import ListItem

class ListForm(forms.ModelForm):
    class Meta:
        model = ListItem
        fields = ['name']
