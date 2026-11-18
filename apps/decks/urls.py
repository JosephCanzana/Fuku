from django.urls import path
from . import views

app_name = "decks"

urlpatterns = [
    # Decks
    path("decks/", views.decks_page, name="decks_page"),
    path("decks/add/", views.add_deck, name="add_deck"),
    path("decks/<int:pk>/edit/", views.edit_deck, name="edit_deck"),
    path("decks/<int:pk>/delete/", views.delete_deck, name="delete_deck"),
    path("decks/<int:pk>/archive/", views.archive_deck, name="archive_deck"),

    # Tags
    path("tags/", views.tags_page, name="tags_page"),
    path("tags/add/", views.add_tag, name="add_tag"),
    path("tags/<int:pk>/edit/", views.edit_tag, name="edit_tag"),
    path("tags/<int:pk>/delete/", views.delete_tag, name="delete_tag"),

    # Flashcard
    path("decks/<int:deck_pk>/", views.deck_detail, name="deck_detail"),
    path("decks/<int:deck_pk>/review/", views.review_deck, name="review_deck"),
    path("decks/<int:deck_pk>/cards/add/", views.add_card, name="add_card"),
    path("decks/<int:deck_pk>/import/", views.import_flashcard, name="import_flashcard"),
    path("decks/<int:deck_pk>/export/", views.export_flashcard, name="export_flashcard"),
    path("decks/<int:deck_pk>/generate/", views.flashcard_generate, name="flashcard_generate"),
    path("decks/<int:deck_pk>/undo/", views.undo, name="undo"),

    path("cards/<int:card_pk>/edit/", views.edit_card, name="edit_card"),
    path("cards/<int:card_pk>/delete/", views.delete_card, name="delete_card"),
    path("cards/<int:card_pk>/rate/", views.rate_card, name="rate_card"),
]