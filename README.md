# PantryPal

A small Django app that tracks what is in your kitchen, shows what to eat first,
and keeps count of what you used up versus tossed.

Stack: Python, Django, SQLite, HTML, CSS, Bootstrap 5, JavaScript.

## Run it

    python -m venv venv
    venv\Scripts\activate          (Windows)   |   source venv/bin/activate  (Mac/Linux)
    pip install -r requirements.txt
    python manage.py makemigrations pantry
    python manage.py migrate
    python manage.py createsuperuser   (optional, for /admin)
    python manage.py runserver

Open http://127.0.0.1:8000/

## Features
- Add, edit, delete food items with an expiry date
- "Use these first" tiles for what expires soonest
- Colour status: fresh, use soon (3 days or less), expired
- Filter by category and status, plus instant JavaScript search
- "Used up" and "Toss" buttons that build a small waste history
- Django admin panel at /admin
