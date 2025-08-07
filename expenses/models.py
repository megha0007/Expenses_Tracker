# expenses/models.py
from django.db import models


class CustomUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)  # Store hashed passwords if manually managing
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
# expenses/models.py

class Expense(models.Model):
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    date = models.DateField()

    def __str__(self):
        return f"{self.title} - ₹{self.amount}"


class Budget(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.DateField()  # Ideally store first day of month

    class Meta:
        unique_together = ('user', 'category', 'month')

    def __str__(self):
        return f"{self.user} - {self.category} - {self.month.strftime('%B %Y')}"


