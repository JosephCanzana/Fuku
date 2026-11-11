from django.http import HttpResponse
from django.shortcuts import render
from apps.accounts.forms import SignUpForm
from apps.accounts.models import User

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
            return HttpResponse("success")
    else:
        form = SignUpForm()

    return render(request, "accounts/sign-up.html", {"form":form})

def login(request):
    return render(request, "accounts/login.html")
