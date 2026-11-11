import re
from django import forms
from apps.accounts.models import User

class SignUpForm(forms.Form):
    username = forms.CharField(max_length=100, min_length=4)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data["username"]
        # If identical username already exist
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Username already exist")

        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Email is already used")

        return email

    def clean_password(self):
        password = self.cleaned_data["password"]

        # atleast 8 letters, one capital, one small letter, one numerical
        pattern = r"(?=.*[A-Za-z])(?=.*\d).{8,}"
        if not re.fullmatch(pattern, password):
            raise forms.ValidationError("The password is not strong enough")

        return password

    def clean(self):
        # initial clean
        cleaned = super().clean()

        # my custom clean and validation
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Confirm password and password is not same.")

        return cleaned
