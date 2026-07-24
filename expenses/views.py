import json
from datetime import date

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from .forms import SignUpForm, ExpenseForm, MonthlyBudgetForm
from .models import Expense, MonthlyBudget, Category


class CustomLoginView(LoginView):
    template_name = "expenses/login.html"


def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = SignUpForm()
    return render(request, "expenses/signup.html", {"form": form})


@login_required
def dashboard(request):
    today = date.today()
    year, month = today.year, today.month

    expenses_this_month = Expense.objects.filter(user=request.user, date__year=year, date__month=month)
    total_this_month = expenses_this_month.aggregate(total=Sum("amount"))["total"] or 0

    by_category = (
        expenses_this_month.values("category")
        .annotate(total=Sum("amount"))
        .order_by("-total")
    )
    category_labels = [Category(c["category"]).label for c in by_category]
    category_totals = [float(c["total"]) for c in by_category]

    # Last 6 months trend
    monthly_totals = []
    monthly_labels = []
    for i in range(5, -1, -1):
        m = month - i
        y = year
        while m <= 0:
            m += 12
            y -= 1
        total = (
            Expense.objects.filter(user=request.user, date__year=y, date__month=m).aggregate(
                total=Sum("amount")
            )["total"]
            or 0
        )
        monthly_totals.append(float(total))
        monthly_labels.append(f"{y}-{m:02d}")

    budget = MonthlyBudget.objects.filter(user=request.user, year=year, month=month).first()
    budget_amount = float(budget.amount) if budget else None
    remaining = (budget_amount - float(total_this_month)) if budget_amount is not None else None

    recent_expenses = Expense.objects.filter(user=request.user)[:10]

    context = {
        "total_this_month": total_this_month,
        "category_labels": json.dumps(category_labels),
        "category_totals": json.dumps(category_totals),
        "monthly_labels": json.dumps(monthly_labels),
        "monthly_totals": json.dumps(monthly_totals),
        "budget_amount": budget_amount,
        "remaining": remaining,
        "recent_expenses": recent_expenses,
        "current_month": today.strftime("%B %Y"),
    }
    return render(request, "expenses/dashboard.html", context)


@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user)
    category_filter = request.GET.get("category")
    if category_filter:
        expenses = expenses.filter(category=category_filter)
    return render(
        request,
        "expenses/expense_list.html",
        {"expenses": expenses, "categories": Category.choices, "selected_category": category_filter},
    )


@login_required
def expense_create(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect("expense_list")
    else:
        form = ExpenseForm(initial={"date": date.today()})
    return render(request, "expenses/expense_form.html", {"form": form, "title": "Add expense"})


@login_required
def expense_edit(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect("expense_list")
    else:
        form = ExpenseForm(instance=expense)
    return render(request, "expenses/expense_form.html", {"form": form, "title": "Edit expense"})


@login_required
def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == "POST":
        expense.delete()
        return redirect("expense_list")
    return render(request, "expenses/expense_confirm_delete.html", {"expense": expense})


@login_required
def budget_view(request):
    today = date.today()
    existing = MonthlyBudget.objects.filter(user=request.user, year=today.year, month=today.month).first()
    if request.method == "POST":
        form = MonthlyBudgetForm(request.POST, instance=existing)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            return redirect("dashboard")
    else:
        form = MonthlyBudgetForm(instance=existing, initial={"year": today.year, "month": today.month})
    return render(request, "expenses/budget_form.html", {"form": form})
