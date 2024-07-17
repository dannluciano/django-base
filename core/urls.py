from django.urls import include, path

from .views import about, home, signup

urlpatterns = [
    path("", home, name="home"),
    path("about", about, name="about"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/create/", signup, name="signup"),
]
