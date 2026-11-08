from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import FoodItemForm
from .models import FoodItem


def item_list(request):
    today = timezone.localdate()
    soon_cutoff = FoodItem.soon_cutoff()

    active = FoodItem.objects.filter(outcome="active")

    counts = {
        "expired": active.filter(expiry_date__lt=today).count(),
        "soon": active.filter(expiry_date__gte=today, expiry_date__lte=soon_cutoff).count(),
        "fresh": active.filter(expiry_date__gt=soon_cutoff).count(),
        "used": FoodItem.objects.filter(outcome="used").count(),
        "tossed": FoodItem.objects.filter(outcome="tossed").count(),
    }

    # "Use these first": the three items that need attention soonest
    use_first = list(active.filter(expiry_date__lte=soon_cutoff)[:3])

    items = active
    q = request.GET.get("q", "").strip()
    status = request.GET.get("status", "")
    category = request.GET.get("category", "")

    if q:
        items = items.filter(name__icontains=q)
    if category:
        items = items.filter(category=category)
    if status == "expired":
        items = items.filter(expiry_date__lt=today)
    elif status == "soon":
        items = items.filter(expiry_date__gte=today, expiry_date__lte=soon_cutoff)
    elif status == "fresh":
        items = items.filter(expiry_date__gt=soon_cutoff)

    context = {
        "items": items,
        "use_first": use_first,
        "counts": counts,
        "categories": FoodItem.CATEGORIES,
        "q": q,
        "status": status,
        "category": category,
        "total_active": active.count(),
    }
    return render(request, "pantry/item_list.html", context)


def item_create(request):
    form = FoodItemForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        item = form.save()
        messages.success(request, f"Added {item.name}.")
        return redirect("pantry:list")
    return render(request, "pantry/item_form.html", {"form": form, "heading": "Add an item"})


def item_update(request, pk):
    item = get_object_or_404(FoodItem, pk=pk)
    form = FoodItemForm(request.POST or None, instance=item)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"Saved changes to {item.name}.")
        return redirect("pantry:list")
    return render(request, "pantry/item_form.html", {"form": form, "heading": f"Edit {item.name}"})


def item_delete(request, pk):
    item = get_object_or_404(FoodItem, pk=pk)
    if request.method == "POST":
        name = item.name
        item.delete()
        messages.success(request, f"Deleted {name}.")
        return redirect("pantry:list")
    return render(request, "pantry/item_confirm_delete.html", {"item": item})


@require_POST
def item_finish(request, pk, outcome):
    item = get_object_or_404(FoodItem, pk=pk)
    if outcome not in ("used", "tossed"):
        messages.error(request, "Unknown action.")
        return redirect("pantry:list")
    item.outcome = outcome
    item.save(update_fields=["outcome"])
    if outcome == "used":
        messages.success(request, f"{item.name} used up. Nothing wasted.")
    else:
        messages.warning(request, f"{item.name} tossed. It happens.")
    return redirect("pantry:list")
