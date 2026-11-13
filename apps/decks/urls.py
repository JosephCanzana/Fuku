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
]