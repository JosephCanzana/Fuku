from django.http import HttpResponse
from django.shortcuts import render
from apps.accounts.forms import SignUpForm

# Create your views here.
def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            return HttpResponse("success")
        return HttpResponse("error")
    else:
        return render(request, "accounts/sign-up.html")

def login(request):
    return render(request, "accounts/login.html")
