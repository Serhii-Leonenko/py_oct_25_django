from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("messenger.urls", namespace="messenger")),
    path("users/", include("users.urls", namespace="users")),
] + debug_toolbar_urls()
