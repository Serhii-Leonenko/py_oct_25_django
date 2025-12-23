from .base import *

SECRET_KEY = "django-insecure-xpo@31^gc88k8wq*#qm)4fyfi4inhozb)i7!4@6+day3$5_+sx"

DEBUG = True

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
