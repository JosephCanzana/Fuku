from django import forms
from apps.decks.models import Deck, Tag, Flashcard
from apps.decks.services import parse_choices

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
        # exclue duplicate check if editing
        if Deck.objects.filter(account=self.user, name__iexact=name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("You already have a deck with this name.")

        return name


class TagForm(forms.ModelForm):
    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    class Meta:
        model = Tag
        fields = ["name"]
        labels = {"name": "Tag name"}
        widgets = {
            "name": forms.TextInput(attrs={"class": "input-primary", "placeholder": "e.g Physics"})
        }

    def clean_name(self):
        name = self.cleaned_data["name"]
        # exclue duplicate check if editing
        if Tag.objects.filter(account=self.user, name__iexact=name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("You already have a tag with this name.")

        return name


class FlashcardForm(forms.ModelForm):
    choices = forms.CharField(
        required=False,
        label="Choices",
        help_text="Separate with semicolons, e.g. Paris;London;Rome",
        widget=forms.TextInput(attrs={"class": "input-primary"}),
    )

    class Meta:
        model = Flashcard
        fields = ["question", "answer", "choices"]
        widgets = {
            "question": forms.Textarea(attrs={"class": "textarea-primary", "placeholder": "Question"}),
            "answer": forms.Textarea(attrs={"class": "textarea-primary", "placeholder": "Answer"})
        }

    def __init__(self, *args, deck=None, **kwargs):
        super().__init__(*args, **kwargs)
        # On edit the card already know its deck
        self.deck = self.instance.deck if self.instance.pk else deck
        # When editing, turn the stored list back into "a;b;c"
        if self.instance.pk and self.instance.choices:
            self.initial["choices"] = ";".join(self.instance.choices)

    def clean_choices(self):
        return  parse_choices(self.cleaned_data["choices"])


class ImportForm(forms.Form):
    file = forms.FileField(
        label="CSV file",
        help_text="Columns: question, answer, choices (separated by semicolons).",
        widget=forms.ClearableFileInput(attrs={"accept": ".csv"}),
    )

    def clean_file(self):
        file = self.cleaned_data["file"]

        if not file.name.lower().endswith(".csv"):
            raise forms.ValidationError("Please upload a .csv file.")

        try:
            file.read().decode("utf-8-sig")
        except UnicodeDecodeError:
            raise forms.ValidationError("File must be UTF-8 text.")
        finally:
            file.seek(0)

        return file