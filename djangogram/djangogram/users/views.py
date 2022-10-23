from audioop import reverse
from http.client import HTTPResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from .forms import signUpForm


def main(request):
    if request.method == "GET":
        return render(request, "users/main.html")

    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("posts:index"))
        else:
            return render(request, "users/main.html")


def signup(request):

    if request.method == "GET":

        form = signUpForm()
        return render(request, "users/signup.html", {"form": form})

    elif request.method == "POST":
        form = signUpForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("posts:index"))

    return render(request, "users/main.html")
