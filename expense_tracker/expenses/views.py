# expenses/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense, Category,Budget, CustomUser
from .forms import ExpenseForm, BudgetForm
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from collections import defaultdict
import csv
from django.http import HttpResponse

def export_expenses_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="expenses.csv"'

    writer = csv.writer(response)
    writer.writerow(['Title', 'Amount', 'Date', 'Category'])

    expenses = Expense.objects.all()
    for expense in expenses:
        writer.writerow([expense.title, expense.amount, expense.date, expense.category.name])

    return response

# def expense_list(request):
#     expenses = Expense.objects.order_by('-date')
#     total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
#     return render(request, 'expenses/list.html', {'expenses': expenses, 'total': total})

def expense_list(request):
    expenses = Expense.objects.all()
    categories = Category.objects.all()

    # Filtering logic
    category = request.GET.get('category')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    if category and category != "all":
        expenses = expenses.filter(category__id=category)

    if date_from and date_to:
        expenses = expenses.filter(date__range=[date_from, date_to])

    context = {
        'expenses': expenses,
        'categories': categories,
        'selected_category': category,
        'date_from': date_from,
        'date_to': date_to,
    }
    return render(request, 'expenses/list.html', context)


def add_expense(request):
    form = ExpenseForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('expense_list')
    return render(request, 'expenses/form.html', {'form': form})

def edit_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    form = ExpenseForm(request.POST or None, instance=expense)
    if form.is_valid():
        form.save()
        return redirect('expense_list')
    return render(request, 'expenses/form.html', {'form': form})

def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    expense.delete()
    return redirect('expense_list')

def category_summary_chart(request):
    data = Expense.objects.values('category').annotate(total=Sum('amount')).order_by('category')
    categories = [d['category'] for d in data]
    totals = [float(d['total']) for d in data]
    return render(request, 'expenses/chart.html', {
        'categories': categories,
        'totals': totals
    })



def budget_list(request):
    user = CustomUser.objects.first()  # Or use session/authenticated user
    budgets = Budget.objects.filter(user=user)
    return render(request, 'expenses/budget_list.html', {'budgets': budgets})

def add_budget(request):
    user = CustomUser.objects.first()  # Replace with actual logged-in user
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = user
            budget.save()
            return redirect('budget_list')
    else:
        form = BudgetForm()
    return render(request, 'expenses/add_budget.html', {'form': form})
