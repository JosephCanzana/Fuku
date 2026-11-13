from django.shortcuts import render

# Create your views here.
def decks_page(request):
    return render(request, "decks/decks.html")


def tags_page(request):
    return render(request, "decks/tags.html")