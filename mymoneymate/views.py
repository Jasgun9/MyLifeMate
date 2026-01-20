from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .models import Expense, Goal
from django.db.models import Sum
from django.db.models.functions import Coalesce


# Create your views here.
def index(request):
    # transactions = Expense.objects.all()
    latest_expenses = Expense.objects.filter(user=request.user).order_by('-dateAdded')[:5]
    goals = Goal.objects.filter(user=request.user).order_by('-dateAdded')[:5]
    allexpenses = Expense.objects.filter(user=request.user).order_by('-dateAdded')
    income = Expense.objects.filter(user=request.user, isExpense=False).aggregate(total_income=Coalesce(Sum('amount'), 0.0))['total_income']
    expense = Expense.objects.filter(user=request.user, isExpense=True).aggregate(total_expense=Coalesce(Sum('amount'), 0.0))['total_expense']
    balance = income - expense
    params = {"balance": balance, "income": income, "expense": expense, "latest_expenses": latest_expenses, "allexpenses": allexpenses, "goals":goals}
    # return HttpResponse(transactions)
    return render(request, 'mymoneymate/index.html', params)



def expense_to_dict(e):
    return {
        "id": e.Eid,
        "title": e.title,
        "category": e.category,
        "amount": e.amount,
        "isExpense": e.isExpense,
        "date": e.dateAdded.isoformat(),
        "date_display": e.dateAdded.strftime("%d %b"),
    }



def goal_to_dict(g: Goal):
    return {
        "id": g.Gid,
        "title": g.title,
        "target": g.amount,
        "saved": g.Saving,
        "progress": 0 if g.amount == 0 else round((g.Saving / g.amount) * 100, 1),
        "date": g.dateAdded.isoformat(),
    }

@csrf_exempt

def transactions(request):
    transactions = Expense.objects.filter(user=request.user).order_by('-dateAdded')
    params = {"expenses": transactions}
    if request.method == "POST":
        data = [expense_to_dict(e) for e in transactions]
        return JsonResponse(data, safe=False)
    return render(request, 'mymoneymate/transactions.html', params)



def addTransaction(request):
    # /add_transaction?title="+title+"&category="+category+"&amount="+amount+"&isExpense="+isExpense+"&dateAdded="+date
    title = request.GET.get("title")
    category = request.GET.get("category")
    amount = float(request.GET.get("amount", 0))
    isExpense = request.GET.get("isExpense")
    dateAdded = request.GET.get("dateAdded")
    if dateAdded:
        try:
            date_obj = datetime.fromisoformat(dateAdded).date()
        except ValueError:
            date_obj = datetime.utcnow().date()
    else:
        date_obj = datetime.utcnow().date()
    exp = Expense(
        title=title,
        category=category,
        amount=float(amount),
        isExpense=bool(int(isExpense)),
        dateAdded=date_obj,
        user=request.user
    )
    exp.save()
    return JsonResponse({"status": "success", "message": "Transaction added successfully."})




def addGoal(request):
    title = request.GET.get("title")
    amount = request.GET.get("amount")
    saving = request.GET.get("saving")
    dateAdded = request.GET.get("dateAdded")
    if dateAdded:
        try:
            date_obj = datetime.fromisoformat(dateAdded).date()
        except ValueError:
            date_obj = datetime.utcnow().date()
    else:
        date_obj = datetime.utcnow().date()
    goal = Goal(
        title=title,
        amount=float(amount),
        Saving=float(saving),
        dateAdded=date_obj,
        user=request.user
    )
    goal.save()
    return JsonResponse({"status": "success", "message": "Goal added successfully."})





@csrf_exempt
def goals(request):
    goals = Goal.objects.filter(user=request.user).order_by('-dateAdded')
    if request.method == "POST":
        data = [goal_to_dict(g) for g in goals]
        return JsonResponse(data, safe=False)
    return render(request, 'mymoneymate/goals.html')


