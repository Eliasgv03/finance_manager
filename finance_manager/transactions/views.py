from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from .models import Transaction, Tag, Currency
from .forms import TransactionForm
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(user=request.user)

    # Filtros
    date_filters = {
        'last_week': timezone.now() - timezone.timedelta(weeks=1),
        'last_month': timezone.now() - timezone.timedelta(days=30),
        'last_3_months': timezone.now() - timezone.timedelta(days=90),
        'last_6_months': timezone.now() - timezone.timedelta(days=180),
        'last_year': timezone.now() - timezone.timedelta(days=365),
    }

    filter_date = request.GET.get('filter_date')
    if filter_date in date_filters:
        transactions = transactions.filter(date__gte=date_filters[filter_date])

    filter_type = request.GET.get('filter_type')
    if filter_type:
        transactions = transactions.filter(type=filter_type)

    filter_tag = request.GET.get('filter_tag')
    if filter_tag:
        transactions = transactions.filter(tag__id=filter_tag)

    tags = Tag.objects.filter(user=request.user)
    
    return render(request, 'transactions/transaction_list.html', {
        'transactions': transactions,
        'tags': tags,
    })

@login_required
def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST, user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.currency = form.cleaned_data['currency']
            transaction.save()
            messages.success(request, "Transaction created successfully!")
            return redirect('transactions:transaction_list')
        else:
            messages.error(request, "There was an error saving the transaction. Please check the form.")
    else:
        
        today = date.today().strftime('%Y-%m-%d')
        default_currency_id = getattr(request.user.profile.default_currency, 'id', None)
        initial_data = {
            'currency': default_currency_id,
            'date': today ,
        }
        form = TransactionForm(user=request.user, initial=initial_data)

    tags = Tag.objects.filter(user=request.user)
    expense_tags = tags.filter(tag_type='expense')
    income_tags = tags.filter(tag_type='income')
    currencies = Currency.objects.all()
    

    return render(request, 'transactions/transaction_new.html', {
        'form': form,
        'expense_tags': expense_tags,
        'income_tags': income_tags,
        'currencies': currencies,
        'default_currency': default_currency_id,
    })

@login_required
def transaction_edit(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    tags = Tag.objects.filter(user=request.user)
    expense_tags = tags.filter(tag_type='expense')
    income_tags = tags.filter(tag_type='income')
    currencies = Currency.objects.all()

    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction, user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.save()
            messages.success(request, "Transaction updated successfully!")
            return redirect('transactions:transaction_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        
        today = transaction.date
        default_currency_id = transaction.currency
        
        initial_data = {
            'currency': default_currency_id,
            'date': today ,
        }
        
        form = TransactionForm(instance=transaction, user=request.user , initial=initial_data)

    return render(request, 'transactions/transaction_new.html', {
        'form': form,
        'expense_tags': expense_tags,
        'income_tags': income_tags,
        'currencies': currencies,
        'transaction': transaction,
    })


@login_required
def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        transaction.delete()
        messages.success(request, "Transaction deleted successfully!")
        return redirect('transactions:transaction_list')

    return render(request, 'transactions/transaction_confirm.html', {'transaction': transaction})
