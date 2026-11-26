from django.db.models import Count, Q
from django.utils import timezone
from django.shortcuts import render, redirect
from apps.accounts.forms import SignUpForm, LoginForm
from apps.accounts.models import User
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from apps.decks.models import Deck


# Create your views here.
def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data.get("username"),
                email=form.cleaned_data.get("email"),
                password=form.cleaned_data["password"]
            )

            login(request, user)
            return redirect("accounts:user_dashboard")
    else:
        form = SignUpForm()

    return render(request, "accounts/sign-up.html", {"form":form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            messages.info(request, f"Welcome back {form.user.username}!")
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
    now = timezone.now()
    decks = Deck.objects.filter(account=request.user).annotate(
        card_count=Count("flashcard"),
        due_count=Count("flashcard", filter=Q(flashcard__next_review_at__lte=now)),
    )
    return render(request, "accounts/user-dashboard.html", {
        "decks": decks,
        "deck_count": len(decks),
        "total_cards": sum(d.card_count for d in decks),
        "total_due": sum(d.due_count for d in decks),
    })