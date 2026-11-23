import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponseBadRequest, HttpResponse
from django.contrib import messages
from django.utils import timezone
from django.utils.text import slugify
from apps.decks.forms import DeckForm, TagForm, FlashcardForm
from apps.decks.models import Deck, Tag, Flashcard
from apps.decks.services import apply_review

# DECKS
@login_required
def decks_page(request):
    show_archived = request.GET.get("show") == "archived"

    decks = (
        Deck.objects.filter(account=request.user, is_archive=show_archived)
        .select_related("tag")
        .order_by("name")
    )
    return render(request, "decks/deck_pages/decks.html", {
        "decks": decks,
        "show_archived": show_archived,
    })


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
    deck = get_object_or_404(Deck, pk=pk, account=request.user)
    deck.delete()
    messages.success(request, "Deck deleted.")
    return redirect("decks:decks_page")


@login_required
@require_POST
def archive_deck(request, pk):
    deck = get_object_or_404(Deck, pk=pk, account=request.user)
    deck.is_archive = not deck.is_archive
    deck.save()
    messages.success(request, "Deck archived." if deck.is_archive else "Deck unarchived.")
    return redirect("decks:decks_page")


# TAGS
@login_required
def tags_page(request):
    tags = Tag.objects.filter(account=request.user)
    return render(request, "decks/tag_pages/tags.html", {"tags":tags})


@login_required
def add_tag(request):
    if request.method == "POST":
        form = TagForm(request.POST, user=request.user)
        if form.is_valid():
            # Create tag form but don't save yet
            tag = form.save(commit=False)
            # Setting the deck user on back end to avoid attacks on frontend
            tag.account = request.user
            # Save to database
            tag.save()
            messages.success(request, "Tag Added.")
            return redirect("decks:tags_page")
    else:
        form = TagForm(user=request.user)
    return render(request, "decks/tag_pages/form.html", {"form":form})


@login_required
def edit_tag(request, pk):
    tag = get_object_or_404(Tag, pk=pk, account=request.user)
    if request.method == "POST":
        form = TagForm(request.POST, instance=tag, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Tag updated.")
            return redirect("decks:tags_page")

    else:
        form = TagForm(instance=tag, user=request.user)
    return render(request, "decks/tag_pages/form.html", {"form":form})


@login_required
@require_POST
def delete_tag(request, pk):
    tag = get_object_or_404(Tag, pk=pk, account=request.user)
    tag.delete()
    messages.success(request, "Tag deleted.")
    return redirect("decks:tags_page")


# FLASHCARD
@login_required
def deck_detail(request, deck_pk):
    # View all flashcard
    deck = get_object_or_404(Deck, pk=deck_pk, account=request.user)
    cards = Flashcard.objects.filter(deck=deck)
    return render(request, "decks/card_pages/deck-detail.html", {"deck": deck, "cards": cards})


@login_required
def review_deck(request, deck_pk):
    # Form of individual flashcard that would recieve a post with rating
    deck = get_object_or_404(Deck, pk=deck_pk, account=request.user)
    now = timezone.now()
    deck_cards = Flashcard.objects.filter(deck=deck)

    # real due cards first
    card = deck_cards.filter(next_review_at__lte=now).order_by("next_review_at").first()

    # pull in a learning card early if theres no due cards
    if card is None:
        card = (
            deck_cards
            .filter(state=Flashcard.State.LEARNING)
            .order_by("next_review_at")
            .first()
        )

    return render(request, "decks/card_pages/review.html", {"deck": deck, "card": card})


@login_required
@require_POST
def rate_card(request, card_pk):
    # Form of individual flashcard that would recieve a post with rating
    card = get_object_or_404(Flashcard, pk=card_pk, deck__account=request.user)

    try:
        rating = int(request.POST.get("rating", ""))
    except ValueError:
        return HttpResponseBadRequest("Invalid rating")
    if rating not in (1, 2, 3, 4):
        return HttpResponseBadRequest("Invalid rating")

    apply_review(card, rating)    
    return redirect("decks:review_deck", deck_pk=card.deck_id)


@login_required
@require_POST
def undo(request, deck_pk):
    # undo the previous card rate
    ...


@login_required
def add_card(request, deck_pk):
    # Individual card add
    deck = get_object_or_404(Deck, pk=deck_pk, account=request.user)
    if request.method == "POST":
        form = FlashcardForm(request.POST, deck=deck)
        if form.is_valid():
            card = form.save(commit=False)
            card.deck = deck
            card.save()
            messages.success(request, "Card Added.")
            return redirect("decks:deck_detail", deck_pk=deck_pk)
    else:
        form = FlashcardForm(deck=deck)
    
    return render(request, "decks/card_pages/form.html", {"form":form, "deck": deck})


@login_required
def edit_card(request, card_pk):
    # Edit specific card
    card = get_object_or_404(Flashcard, pk=card_pk, deck__account=request.user)
    deck = card.deck

    if request.method == "POST":
        form = FlashcardForm(request.POST, instance=card)
        if form.is_valid():
            form.save()
            messages.success(request, "Card updated.")
            return redirect("decks:deck_detail", deck_pk=deck.pk)
    else:
        form = FlashcardForm(instance=card)

    return render(request, "decks/card_pages/form.html", {"form": form, "deck": deck})


@login_required
@require_POST
def delete_card(request, card_pk):
    # Delete specific card
    card = get_object_or_404(Flashcard, pk=card_pk, deck__account=request.user)
    deck_id = card.deck_id
    card.delete()
    messages.success(request, "Card deleted.")
    return redirect("decks:deck_detail", deck_pk=deck_id)


@login_required
def import_flashcard(request, deck_pk):
    # Import CSV of flashcard
    return render(request, "decks/card_pages/import.html")


@login_required
def export_flashcard(request, deck_pk):
    # Create a CSV of flashcard and download
    deck = get_object_or_404(Deck, pk=deck_pk, account=request.user)
    cards = Flashcard.objects.filter(deck=deck.id)

    # File where th
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="{slugify(deck.name) or "deck"}.csv"'
    writer = csv.writer(response)

    # convert to csv
    for card in cards:
        choices_text = ";".join(card.choices) if card.choices else ""
        writer.writerow([card.question, card.answer, choices_text])
    
    return response

@login_required
def flashcard_generate(request, deck_pk):
    # Form with the desired file that will be used to create flashcard
    # it would return a CSV file from the AI
    return render(request, "decks/card_pages/generate.html")