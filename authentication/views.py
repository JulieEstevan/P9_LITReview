from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.conf import settings

from . import forms


def signup_page(request):
    """Render the signup page."""
    form = forms.SignupForm()
    if request.method == "POST":
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, "authentication/signup.html", {"form": form})
