from .models import ListItem
from django import forms

class ListItemBaseForm(forms.ModelForm):
    class Meta:
        model = ListItem
        fields = ["content", "list_id"]

    def __init__(self, list_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].label = ""
        self.fields["list_id"] = forms.IntegerField(initial=list_id, widget=forms.HiddenInput())

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