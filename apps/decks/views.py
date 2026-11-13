from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


# DECKS
@login_required
def decks_page(request):
    return render(request, "decks/deck_pages/decks.html")


@login_required
def add_deck(request):
    return render(request, "decks/deck_pages/form.html")


@login_required
def edit_deck(request, pk):
    return render(request, "decks/deck_pages/form.html")


@login_required
@require_POST
def delete_deck(request, pk):
    return render(request, "decks/deck_pages/decks.html")


@login_required
@require_POST
def archive_deck(request, pk):
    return render(request, "decks/deck_pages/decks.html")


@login_required
def update_deck_tag(request):
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
