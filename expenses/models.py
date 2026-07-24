from django.db import models
from django.contrib.auth.models import User


class Category(models.TextChoices):
    RENT = "rent", "Rent"
    GROCERY = "grocery", "Grocery"
    TRANSPORT = "transport", "Transport"
    INSURANCE = "insurance", "Insurance"
    UTILITIES = "utilities", "Utilities"
    HEALTHCARE = "healthcare", "Healthcare"
    ENTERTAINMENT = "entertainment", "Entertainment"
    OTHER = "other", "Other"


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expenses")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.OTHER)
    note = models.CharField(max_length=255, blank=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return f"{self.get_category_display()} - €{self.amount} ({self.date})"


class MonthlyBudget(models.Model):
    """One budget cap per user per calendar month."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="budgets")
    year = models.PositiveIntegerField()
    month = models.PositiveSmallIntegerField()  # 1-12
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ("user", "year", "month")
        ordering = ["-year", "-month"]

    def __str__(self):
        return f"Budget {self.month}/{self.year}: €{self.amount}"
