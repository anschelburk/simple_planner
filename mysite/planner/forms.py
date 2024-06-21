from .models import ListItem
from django import forms

class ListItemBaseForm(forms.ModelForm):
    class Meta:
        model = ListItem
        fields = ["list_name", "content"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].label = ""
        self.fields["list_name"] = forms.CharField(initial='Enter List Title')
        self.fields["list_name"].label = ""

class ListItemUpdateForm(ListItemBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].widget = forms.TextInput(
            attrs={
                "hx-put": "/update_item/{pk}/",
                "hx-trigger": "blur changed",
                "hx-target": "this",
                "placeholder": "Enter item here...",
            }
        )
        # list_name is already set and doesn't need updating so remove
        # it from fields to avoid validation (form.is_valid) issues
        if 'list_name' in self.fields:
            del self.fields['list_name']
