# Django Starter (apps/ + Tailwind)

Deskripsi singkat setup Django dengan:
- apps/ folder
- config/settings/base,dev,staging, prod
- switch environment memakai DJANGO_ENV

- django-tailwind integrasi

=== Struktur ===
.
manage.py
apps/
config/settings/
    __init__.py
    base.py
    dev.py
    staging.py
    prod.py

=== Switch Env (config/settings/__init__.py) ===
import os
env = os.getenv("DJANGO_ENV", "dev")

if env == "prod":
    from .prod import *
elif env == "staging":
    from .staging import *
else:
    from .dev import *
 
=== Set apps/ as root (base.py) ===
import sys
import pathlib

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent.parent
APPS_DIR = BASE_DIR / "apps"
sys.path.insert(0, str(APPS_DIR))

## Buat app baru
python manage.py startapp blog apps/blog

## Daftarkan ke INSTALLED_APPS (base.py)
INSTALLED_APPS = [
    "blog",
]

=== Django Tailwind ===
pip install django-tailwind

INNSTALLED_APPS += ["tailwind"]
TAILWIND_APP_NAME = "theme"

python manage.py tailwind init
python manage.py tailwind install
python manage.py tailwind start

## Load Tailwind di template
{ {% load tailwind_tags %}
{ {% tailwind_css %}

## Run server
python manage.py runserver
