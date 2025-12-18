from django.urls import path

from messenger.views import HomeView, MessageList, MessageDetail, MessageCreateView

app_name = "messenger"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("messages/", MessageList.as_view(), name="message-list"),
    path("messages/<int:pk>/", MessageDetail.as_view(), name="message-detail"),
    path("messages/create/", MessageCreateView.as_view(), name="message-create"),
]
