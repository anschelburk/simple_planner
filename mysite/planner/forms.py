from .models import ListItem
from django import forms

class ListItemBaseForm(forms.ModelForm):
    class Meta:
        model = ListItem
        fields = ["content", "list_name"]

    def __init__(self, list_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].label = ""
        self.fields["list_name"] = forms.IntegerField(initial=list_name, widget=forms.HiddenInput())

class ListItemUpdateForm(ListItemBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].widget = forms.TextInput(
            attrs={
                "hx-put": "/update_item/{id}/",
                "hx-trigger": "blur changed",
                "hx-target": "this",
                "placeholder": "Enter item here...",
            }
        )