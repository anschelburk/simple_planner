from .models import ListItem
from django import forms

class ListItemBaseForm(forms.ModelForm):
    class Meta:
        model = ListItem
        fields = ["content"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].label = ""


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