from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def home(request):
    return render(request, "home/home.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("dashboard"))
        else:
            return render(request, "home/login.html", {
                "message": "Invalid Credentials !!"
            })
    
    return render(request, "home/login.html")

def logout_view(request):
    logout(request)
    return render(request, "home/login.html", {
        "message": "Logged Out !"
    })

def register_user(request):
    if request.method == 'POST':
        first_name = request.POST["firstname"]
        last_name = request.POST["lastname"]
        email = request.POST["email"]
        username = request.POST["username"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 == password2:
            # create user and authenticate 
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password1,
            )
            login(request, user)
            return HttpResponseRedirect(reverse('login'))
        else:
            return render(request, "home/register.html", {
                'message': 'Passwords do not match !!'
            })
    return render(request, "home/register.html")

