from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse


# Create your views here.
def index(request):

    if request.user.is_authenticated:
        return render(request, 'mylifemate/index.html')
    else:
        return redirect('Login')

def handleSignUp(request):
    if request.method == "POST":
        email = (request.POST["email"] or "").strip().lower()
        username = (request.POST["email"] or "").strip().lower()
        password = request.POST["password"] or ""
        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = request.POST["fname"] or ""
        myuser.save()
        return redirect("Login")
    return render(request, 'mylifemate/signup.html')

def handleLogin(request):
    if request.method == "POST":
        username = (request.POST["email"] or "").strip().lower()
        password = request.POST["password"] or ""
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("HomePage")
    return render(request, 'mylifemate/login.html')

def handleLogout(request):
    logout(request)
    return redirect("HomePage")