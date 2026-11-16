from django import forms
from apps.decks.models import Deck, Tag

class DeckForm(forms.ModelForm):
    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields["tag"].queryset = Tag.objects.filter(account=user)


    class Meta:
        model = Deck
        fields = ["name", "tag", "is_archive"]
        labels = {"name": "Deck name"}
        widgets = {
            "name": forms.TextInput(attrs={"class": "input-primary", "placeholder": "e.g. Biology"}),
            "tag": forms.Select(attrs={"class": "input-primary"}),
        }

    def clean_name(self):
        name = self.cleaned_data["name"]
        if Deck.objects.filter(account=self.user, name__iexact=name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("You already have a deck with this name.")

        return name


class TagForm(forms.ModelForm):
    ...