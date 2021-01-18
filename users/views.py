from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView
from . import forms
from django.contrib.auth import authenticate, login, logout
import os
import requests
from . import models
# Create your views here.

class LoginView(View):

    def get(self, request): #if request.method == "GET"
        form = forms.LoginForm(initial={'email':'itn@las.com'})
        ctx = {
            'form':form,
        }
        return render(request, "users/login.html", ctx)

    def post(self, request): #elif request.method == "POST"
        form = forms.LoginForm(request.POST)
        print(form) 
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)
            if user is not None:
                print("된겨?")
                login(request, user)
                return redirect(reverse("core:home"))
        ctx={
            'form':form,
        }
        return render(request, "users/login.html", ctx)

       
def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

    initial = {
        "first_name":"kiyun",
        "last_name":"kim",
        "email":"kiyoon9390@gmail.com",
    }

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            print("된겨?")
            login(self.request, user)
        return super().form_valid(form)


def github_login(request):
    client_id = os.environ.get("GH_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"
    return redirect(f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user")

class GithubException(Exception):
    pass

def github_callback(request):
    try: 
        client_id = os.environ.get("GH_ID")
        client_secret = os.environ.get("GH_SECRET")
        code = request.GET.get('code', None)
        if code is not None :
            result = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept":"application/json"}
            )
            result_json = result.json()
            error = result_json.get('error', None)
            if error is not None:
                raise GithubException()
            else:
                access_token = result_json.get("access_token")
                profile_request = requests.get(f"https://api.github.com/user", 
                headers={"Authorization":f"token {access_token}",
                        "Accept":"application/json",}
                )
                profile_json = profile_request.json()
                username = profile_json.get('login', None)
                if username is not None:
                    name = profile_json.get('name')
                    email = profile_json.get('email')
                    bio = profile_json.get('bio')
                    try:
                        user = models.User.objects.get(email=email)
                        if user.login_method == models.User.LOGIN_GH:
                            #user trying to log in
                            login(request, user)
                        else:
                            raise GithubException()
                    except models.User.DoesNotExist:
                        new_user = models.User.objects.create(email=email, first_name=name, username=email, bio=bio, login_method=models.User.LOGIN_GH)
                        new_user.set_unusable_password()
                        new_user.save()
                        login(request, new_user)
                    return redirect(reverse("core:home"))

                else:
                    raise GithubException()

        else:
            raise GithubException()
    except GithubException:
        return redirect(reverse("users:login"))