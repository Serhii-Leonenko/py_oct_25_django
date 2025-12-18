import logging

from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.db import transaction
from django.urls import reverse_lazy
from django.views import generic, View

from users.forms import SignUpForm
from users.services.email_service import EmailService
from users.services.token_service import user_token_activation

logger = logging.getLogger(__name__)


class SignUpView(generic.FormView):
    form_class = SignUpForm
    template_name = "registration/sign_up.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        with transaction.atomic():
            form.instance.is_active = False
            user = form.save()

            schema = self.request.scheme  # http or https
            domain = get_current_site(
                self.request
            ).domain  # example.com or 127.0.0.1:8000
            token = user_token_activation.make_token(user)

            try:
                EmailService.send_activation_email(
                    user=user, schema=schema, domain=domain, token=token
                )
                messages.success(self.request, "Check your email")
            except Exception as error:
                logger.error(error, exc_info=True)

                raise

        return super().form_valid(form)


class ActivateView(View):
    def get(self, request, uid, token):
        # TODO implement activation logic
        ...
