from .models import ListItem, Publisher, Book
from django import forms
from django.forms import inlineformset_factory

class ListItemBaseForm(forms.ModelForm):
    class Meta:
        model = ListItem
        fields = ["list_name", "content"]

    def __init__(self, list_name, *args, **kwargs):
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

### TEMP

class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = ['name']

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title']

BookFormSet = inlineformset_factory(Publisher, Book, form=BookForm, extra=1, can_delete=True)