from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Expense(models.Model):
    Eid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=120)
    isExpense = models.BooleanField()
    amount = models.FloatField()
    dateAdded = models.DateField()
    category = models.CharField(max_length=80, default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Goal(models.Model):
    Gid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=120, null=False)
    amount = models.FloatField( null=False)   # target
    Saving = models.FloatField( null=False)
    dateAdded = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.title