from django.contrib import admin

from .models import FoodItem


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "quantity", "expiry_date", "outcome")
    list_filter = ("category", "outcome")
    search_fields = ("name",)
