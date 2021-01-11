from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView
from . import forms
from django.contrib.auth import authenticate, login, logout
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