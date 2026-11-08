from datetime import timedelta

from django.db import models
from django.utils import timezone

SOON_DAYS = 3  # items expiring within this many days count as "use soon"


class FoodItem(models.Model):
    CATEGORIES = [
        ("dairy", "Dairy & eggs"),
        ("produce", "Fruit & vegetables"),
        ("protein", "Meat & fish"),
        ("grains", "Grains & bakery"),
        ("packaged", "Packaged & snacks"),
        ("other", "Other"),
    ]
    OUTCOMES = [
        ("active", "In the kitchen"),
        ("used", "Used up"),
        ("tossed", "Tossed"),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORIES, default="other")
    quantity = models.PositiveIntegerField(default=1)
    expiry_date = models.DateField()
    notes = models.CharField(max_length=200, blank=True)
    outcome = models.CharField(max_length=10, choices=OUTCOMES, default="active")
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["expiry_date", "name"]

    def __str__(self):
        return self.name

    @property
    def days_left(self):
        return (self.expiry_date - timezone.localdate()).days

    @property
    def status(self):
        days = self.days_left
        if days < 0:
            return "expired"
        if days <= SOON_DAYS:
            return "soon"
        return "fresh"

    @property
    def days_label(self):
        days = self.days_left
        if days < -1:
            return f"Expired {abs(days)} days ago"
        if days == -1:
            return "Expired yesterday"
        if days == 0:
            return "Expires today"
        if days == 1:
            return "1 day left"
        return f"{days} days left"

    @classmethod
    def soon_cutoff(cls):
        return timezone.localdate() + timedelta(days=SOON_DAYS)
