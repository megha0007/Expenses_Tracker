# expenses/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense
from .forms import ExpenseForm
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from collections import defaultdict

def expense_list(request):
    expenses = Expense.objects.order_by('-date')
    total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    return render(request, 'expenses/list.html', {'expenses': expenses, 'total': total})

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
