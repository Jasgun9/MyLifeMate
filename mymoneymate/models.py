from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Expense(models.Model):
    Eid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=120)
    isExpense = models.BooleanField()
    amount = models.FloatField()
    dateAdded = models.DateField()
    category = models.CharField(max_length=80)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title