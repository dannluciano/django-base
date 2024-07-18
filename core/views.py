from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse

from core.tasks import send_email

from .forms import ContactForm, UserCreationForm


def home(request):
    if request.htmx:
        base_template = "main.html"
    else:
        base_template = "base.html"
    context = {"base_template": base_template}
    return render(request, "core/home.html", context)


def about(request):
    if request.htmx:
        base_template = "main.html"
    else:
        base_template = "base.html"
    context = {"base_template": base_template}
    return render(request, "core/about.html", context)


def contact(request):
    if request.htmx:
        base_template = "main.html"
    else:
        base_template = "base.html"

    form = ContactForm()
    context = {"base_template": base_template, "form": form}

    if request.POST:
        form = ContactForm(request.POST)
        context["form"] = form
        if form.is_valid():
            sender_name = form.cleaned_data["sender_name"]
            sender_email = form.cleaned_data["sender_email"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]

            send_email.enqueue(subject, message, sender_name, sender_email)

            return redirect(reverse("contact"))
        else:
            return render(request, "core/contact.html", context)
    else:
        return render(request, "core/contact.html", context)


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
