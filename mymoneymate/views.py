from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .models import Expense
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    transactions = Expense.objects.all()
    params = {"balance": 0, "income": 0, "expense": 0, "latest_expenses": transactions}
    # return HttpResponse(transactions)
    return render(request, 'mymoneymate/index.html', params)


def transactions(request):
    transactions = Expense.objects.all()
    params = {"expenses": transactions}
    return render(request, 'mymoneymate/transactions.html', params)


def goals(request):
    return render(request, 'mymoneymate/index.html')


def handleSignUp(request):
    if request.method == "POST":
        email = (request.POST["email"] or "").strip().lower()
        username = (request.POST["email"] or "").strip().lower()
        password = request.POST["password"] or ""
        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = request.POST["fname"] or ""
        myuser.save()

    return HttpResponse("This is handleSignUp")

def handleLogin(request):
    username = (request.POST["email"] or "").strip().lower()
    password = request.POST["password"] or ""
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)

def handleLogout(request):
    logout(request)
    return HttpResponse("This is handleLogout")