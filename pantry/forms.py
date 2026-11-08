from django import forms

from .models import FoodItem


class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ["name", "category", "quantity", "expiry_date", "notes"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Greek yogurt", "autofocus": True}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "expiry_date": forms.DateInput(format="%Y-%m-%d", attrs={"class": "form-control", "type": "date"}),
            "notes": forms.TextInput(attrs={"class": "form-control", "placeholder": "Optional, e.g. top shelf of the fridge"}),
        }
