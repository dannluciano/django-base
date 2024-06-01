from django.urls import include, path

from .views import home, signup

urlpatterns = [
    path("", home, name="home"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/create/", signup, name="signup"),
]
