from datetime import timedelta
from django.utils import timezone
from apps.decks.models import Flashcard

AGAIN, HARD, GOOD, EASY = 1, 2, 3, 4
LEARNING_STEPS = [1, 6, 10]
QUALITY = {AGAIN: 1, HARD: 3, GOOD: 4, EASY: 5}
GRADUATING_INTERVAL = 1
EASY_INTERVAL = 4

def apply_review(card:Flashcard, rating:int):
    if card.state in (Flashcard.State.NEW, Flashcard.State.LEARNING):
        # Step based on rating
        step = card.step or 0

        # Again set step to 0
        if rating == AGAIN:
            step = 0
        # Good add 1 to the step
        elif rating == GOOD:
            step += 1
        # Hard stay on the same step
        # Easy automatically graduate the card
        if rating == EASY or step >= len(LEARNING_STEPS):
            # graduate: set state, clear step, set interval and count, due in days
            card.state = Flashcard.State.REVIEW
            card.step = None
            card.interval = EASY_INTERVAL if rating == EASY else GRADUATING_INTERVAL
            card.next_review_at = timezone.now() + timedelta(days=card.interval)
            card.repetition_count += 1
        else:
            # keep learning: set state, save step, due in LEARNING_STEPS[step] minutes
            card.state = Flashcard.State.LEARNING
            card.step = step
            card.next_review_at = timezone.now() + timedelta(minutes=LEARNING_STEPS[step])
    else:
        q = QUALITY[rating]
        d = 5 - q
        if rating == AGAIN:
            # Put the review card on learning again
            card.ease_factor = max(1.3, card.ease_factor - 0.2)
            card.state = card.State.LEARNING
            card.step = 0
            card.repetition_count = 0
            card.next_review_at = timezone.now() + timedelta(minutes=LEARNING_STEPS[0])
        else:
            # SM2 logic
            # How many days calculation
            if card.repetition_count == 0:
                card.interval = 1
            elif card.repetition_count == 1:
                card.interval = 6
            else:
                card.interval = round(card.interval * card.ease_factor)

            # increase the ease factor
            card.ease_factor = max(1.3, card.ease_factor + (0.1 - d * (0.08 + d * 0.02)))
            card.repetition_count += 1
            card.next_review_at = timezone.now() + timedelta(days=card.interval)

    # Save all changes
    card.save()