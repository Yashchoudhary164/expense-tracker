from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    expenses = Expense.objects.filter(user=request.user)
    total = sum(exp.amount for exp in expenses)

    return render(request, 'home.html', {
        'expenses': expenses,
        'total': total
    })

@login_required
def add_expense(request):
    if request.method == 'POST':
        Expense.objects.create(
            user=request.user,
            title=request.POST['title'],
            amount=request.POST['amount'],
            category=request.POST['category']
        )
        return redirect('home')

    return render(request, 'add_expense.html')

@login_required
def delete_expense(request, id):
    expense = get_object_or_404(Expense, id=id, user=request.user)
    expense.delete()
    return redirect('home')

@login_required
def edit_expense(request, id):
    expense = get_object_or_404(Expense, id=id, user=request.user)

    if request.method == 'POST':
        expense.title = request.POST['title']
        expense.amount = request.POST['amount']
        expense.category = request.POST['category']
        expense.save()
        return redirect('home')

    return render(request, 'edit_expense.html', {'expense': expense})