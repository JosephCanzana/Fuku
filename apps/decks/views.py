from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from apps.decks.forms import DeckForm
from apps.decks.models import Deck

# DECKS
@login_required
def decks_page(request):
    decks = Deck.objects.filter(account=request.user, is_archive=False).order_by("name")
    return render(request, "decks/deck_pages/decks.html", {"decks": decks})


@login_required
def add_deck(request):
    if request.method == "POST":
        form = DeckForm(request.POST, user=request.user)
        if form.is_valid():
            # Create deck form but don't save yet
            deck = form.save(commit=False)
            # Setting the deck user on back end to avoid attacks on frontend
            deck.account = request.user
            # Save to database
            deck.save()
            messages.success(request, "Deck saved.")
            return redirect("decks:decks_page")
    else:
        form = DeckForm(user=request.user)
    return render(request, "decks/deck_pages/form.html", {"form": form})


@login_required
def edit_deck(request, pk):
    deck = get_object_or_404(Deck, pk=pk, account=request.user)
    if request.method == "POST":
        form = DeckForm(request.POST, instance=deck, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "The Deck is updated")
            return redirect("decks:decks_page")
    else:
        form = DeckForm(instance=deck, user=request.user)
    return render(request, "decks/deck_pages/form.html", {"form":form, "deck":deck})


@login_required
@require_POST
def delete_deck(request, pk):
    return render(request, "decks/deck_pages/decks.html")


@login_required
@require_POST
def archive_deck(request, pk):
    return render(request, "decks/deck_pages/decks.html")


# TAGS
@login_required
def tags_page(request):
    return render(request, "decks/tag_pages/tags.html")


@login_required
def add_tag(request):
    return render(request, "decks/tag_pages/form.html")


@login_required
def edit_tag(request, pk):
    return render(request, "decks/tag_pages/form.html")


@login_required
@require_POST
def delete_tag(request, pk):
    return render(request, "decks/tag_pages/tags.html")
