from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Expense, MonthlyBudget


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ["amount", "category", "note", "date"]
        widgets = {
            "amount": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "note": forms.TextInput(attrs={"class": "form-control", "placeholder": "Optional note"}),
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }


class MonthlyBudgetForm(forms.ModelForm):
    class Meta:
        model = MonthlyBudget
        fields = ["year", "month", "amount"]
        widgets = {
            "year": forms.NumberInput(attrs={"class": "form-control"}),
            "month": forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 12}),
            "amount": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
        }
