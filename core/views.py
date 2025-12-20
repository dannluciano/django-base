from functools import wraps

from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse
from extra_settings.models import Setting

from core.tasks import send_email

from .forms import ContactForm, UserCreationForm


def with_template(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        context = view_func(request, *args, **kwargs)
        context["logo"] = Setting.get("SITE_LOGO")
        if isinstance(context, dict):
            context["base_template"] = "main.html" if request.htmx else "base.html"
            return render(request, context.pop("template"), context)
        return context

    return wrapper


@with_template
def home(request):
    return {"template": "core/home.html"}


@with_template
def about(request):
    return {"template": "core/about.html"}


@with_template
def contact(request):
    form = ContactForm()

    if request.POST:
        form = ContactForm(request.POST)
        if form.is_valid():
            sender_name = form.cleaned_data["sender_name"]
            sender_email = form.cleaned_data["sender_email"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]

            send_email.enqueue(subject, message, sender_name, sender_email)
            messages.add_message(
                request, messages.SUCCESS, "Obrigado pela sua mensagem."
            )

            return redirect(reverse("contact"))
        else:
            return {"template": "core/contact.html", "form": form}
    else:
        return {"template": "core/contact.html", "form": form}


def signup(request):
    if request.htmx:
        base_template = "main.html"
    else:
        base_template = "base.html"
    if request.user.is_authenticated:
        return redirect(reverse("home"))
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                login(request, user)
                return redirect(reverse("home"))
            else:
                return redirect(reverse("login"))
        else:
            form = UserCreationForm(request.POST)
            context = {"base_template": base_template, "form": form}
        return render(request, "core/signup.html", context)
    else:
        form = UserCreationForm()
        context = {"base_template": base_template, "form": form}
        return render(request, "core/signup.html", context)
