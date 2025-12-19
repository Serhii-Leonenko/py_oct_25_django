import logging

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.db import transaction
from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.views import generic, View

from users.forms import SignUpForm
from users.services.email_service import EmailService
from users.services.token_service import user_token_activation

User = get_user_model()

logger = logging.getLogger(__name__)


class SignUpView(generic.FormView):
    form_class = SignUpForm
    template_name = "registration/sign_up.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form: SignUpForm):
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
    def get(self, request: HttpRequest, uid: str, token: str):
        try:
            uid = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None:
            if user.is_active:
                messages.info(request, "Your account is already activated.")

                return redirect("users:login")

            if user_token_activation.check_token(user, token):
                user.is_active = True
                user.save()

                messages.success(
                    request,
                    "Thank you for confirming your email. You can now login to your account.",
                )
                return redirect("users:login")

        return render(request, "registration/activation_invalid.html")


class UserListView(generic.ListView):
    model = User


class UserListPartialView(generic.ListView):
    template_name = "users/partials/user_list_partial.html"

    def get_queryset(self):
        queryset = User.objects.all()

        if search := self.request.GET.get("search"):
            queryset = queryset.filter(
                Q(username__icontains=search)
                | Q(email__icontains=search)
                | Q(first_name__icontains=search)
                | Q(last_name__icontains=search)
            )

        return queryset
