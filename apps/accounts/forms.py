import re
from django import forms
from apps.accounts.models import User
from django.db.models import Q
from django.contrib.auth import authenticate

class SignUpForm(forms.Form):
    username = forms.CharField(max_length=100, min_length=4)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data["username"]
        # If identical username already exist
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Username already exist.")

        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Email already used.")

        return email

    def clean_password(self):
        password = self.cleaned_data["password"]

        errors = []

        if len(password) < 8:
            errors.append("Use at least 8 characters.")
        if not re.search(r"[A-Za-z]", password):
            errors.append("Include at least one letter.")
        if not re.search(r"\d", password):
            errors.append("Include at least one number.")

        if errors:
            raise forms.ValidationError(errors)

    def clean(self):
        # initial clean
        cleaned = super().clean()

        # my custom clean and validation
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Passwords don't match. Please retype it.")

        return cleaned

class LoginForm(forms.Form):
    identification = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned = super().clean()
        identification = cleaned.get("identification")
        password = cleaned.get("password")

        if identification and password:
            user = User.objects.filter(
                Q(username__iexact=identification) | Q(email__iexact=identification)
            ).first()

            authenticated = authenticate(username=user.username, password=password) if user else None
            if authenticated is None:
                raise forms.ValidationError("Invalid username/email or password.")
            self.user = authenticated

        return cleaned
