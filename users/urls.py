from django.urls import path, include

from users.views import SignUpView, ActivateView, UserListView, UserListPartialView

app_name = "users"

urlpatterns = [
    path("", UserListView.as_view(), name="user-list"),
    path("partial/", UserListPartialView.as_view(), name="user-list-partial"),
    # auth
    path("sign-up/", SignUpView.as_view(), name="sign-up"),
    path("activate/<str:uid>/<str:token>/", ActivateView.as_view(), name="activate"),
    path("", include("django.contrib.auth.urls")),
]
