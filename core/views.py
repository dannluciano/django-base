from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import UserCreationForm


def home(request):
    return render(request, "core/home.html", {})


def signup(request):
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
        return render(request, "core/signup.html", {"form": form})
    else:
        form = UserCreationForm()
        return render(request, "core/signup.html", {"form": form})
