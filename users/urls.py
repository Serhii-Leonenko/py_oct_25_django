from django.urls import path, include

from users.views import SignUpView, ActivateView

app_name = "users"

urlpatterns = [
    path("sign-up/", SignUpView.as_view(), name="sign-up"),
    path("activate/<str:uid>/<str:token>/", ActivateView.as_view(), name="activate"),
    path("", include("django.contrib.auth.urls")),
]
