from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView

from messenger.forms import MessageForm
from messenger.models import Message


class HomeView(TemplateView):
    template_name = "messenger/home.html"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        num_messages = Message.objects.count()

        context["num_messages"] = num_messages

        if last_viewed_message_id := self.request.session.get("last_view_message"):
            try:
                last_viewed_message = Message.objects.get(pk=last_viewed_message_id)
                context["last_viewed_message"] = last_viewed_message
            except Message.DoesNotExist:
                del self.request.session["last_view_message"]

        return context


class MessageList(ListView):
    model = Message


class MessageDetail(DetailView):
    model = Message

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)

        self.request.session["last_view_message"] = obj.id

        return obj


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("messenger:message-list")

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)
