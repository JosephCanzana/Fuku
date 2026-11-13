from django.urls import path
from . import views

app_name = "decks"

urlpatterns = [
    path("decks/", views.decks_page, name="decks_page"),
    path("tags/", views.tags_page, name="tags_page"),
]