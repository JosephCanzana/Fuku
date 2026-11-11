from django.http import HttpResponse
from django.shortcuts import render, redirect
from apps.accounts.forms import SignUpForm, LoginForm
from apps.accounts.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


# Create your views here.
def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data.get("username"),
                email=form.cleaned_data.get("email"),
                password=form.cleaned_data["password"]
            )
            return redirect("accounts:user_dashboard")
    else:
        form = SignUpForm()

    return render(request, "accounts/sign-up.html", {"form":form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            return redirect("accounts:user_dashboard")
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})


@require_POST
def logout_view(request):
    logout(request)
    return redirect("accounts:login")

@login_required
def user_dashboard(request):
    return render(request, "accounts/user-dashboard.html")