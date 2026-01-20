from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="moneyHome"),
    path('transactions/', views.transactions, name="moneyTrans"),
    path('goals/', views.goals, name="moneyGoals"),
    path('addTransaction/', views.addTransaction, name="addTransaction"),
    path('addGoal/', views.addGoal, name="addGoal"),
    path('deleteGoal/', views.deleteGoal, name="deleteGoal"),
    path('updategoalsaving/', views.updateGoalSaving, name="updateGoalSaving"),
    
    
    
    

]
