from django.utils import timezone
from django.db import models
from django.conf import settings


class Tag(models.Model):
    """
    Tags to categorize the decks
    """
    name = models.CharField(max_length=100)
    account = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        constraints =[
            models.UniqueConstraint(fields=["name", "account"], name="unique_tag_per_account")
        ]

    def __str__(self):
        return self.name


class Deck(models.Model):
    """
    Deck is the holder of related tags
    """
    name = models.CharField(max_length=100)
    is_archive = models.BooleanField(default=False)
    account = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class Flashcard(models.Model):
    """
    Each card keeps its own SM2 state
    CSV FORMAT for import: "question","answer","multiple;choices;is;seperated"
    """
    question = models.TextField()
    answer = models.TextField()
    choices = models.JSONField(null=True, blank=True)

    # SM2 Variables
    # Successful review in a row, reset at 0 when review fails
    repetition_count = models.PositiveIntegerField(default=0)
    # Use to calculate how fast interval grows
    ease_factor = models.FloatField(default=2.5)
    # Days until the next review
    interval = models.PositiveIntegerField(default=0)

    # Learning state
    class State(models.TextChoices):
        NEW = "new", "New"
        LEARNING = "learning", "Learning"
        REVIEW = "review", "Review"
    state = models.CharField(max_length=10, choices=State.choices, default=State.NEW)
    # Position in the learning steps empty unless the state is learning
    step = models.PositiveIntegerField(null=True, blank=True)

    # When the card is next due
    next_review_at = models.DateTimeField(default=timezone.now)

    # Deleting the deck would delete all of it's card
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)

    def __str__(self):
        return self.question[:50]