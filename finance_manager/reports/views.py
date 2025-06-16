import matplotlib.pyplot as plt
import matplotlib
from io import BytesIO
import base64
import pandas as pd
from django.shortcuts import render
from django.db.models import Sum
from transactions.models import Transaction
import matplotlib.dates as mdates

matplotlib.use('Agg')

from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.utils import timezone

def _get_image_from_plot(fig):
    """Converts a Matplotlib figure to a base64 encoded image."""
    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', dpi=100)
    plt.close(fig) 
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def _generate_tags_pie_chart(income_data, expense_data):
    """Generates a pie chart for income and expense tags. Expects Django QuerySets."""
    fig, ax = plt.subplots(1, 2, figsize=(16, 7))

   
    income_tags_df = pd.DataFrame(income_data)
    if not income_tags_df.empty and income_tags_df['total'].sum() > 0:
        income_total_sum = income_tags_df['total'].sum()
        income_tags_df['percentage'] = (income_tags_df['total'] / income_total_sum) * 100
        ax[0].pie(income_tags_df['total'], colors=income_tags_df['tag__color'].tolist(), startangle=90)
        ax[0].legend(
            [f"{name} ({percentage:.1f}%) " for name, percentage in zip(income_tags_df['tag__name'], income_tags_df['percentage'])],
            title="Income Tags", loc="best", bbox_to_anchor=(0.9, 1))
    ax[0].set_title('Income by Tag')

   
    expense_tags_df = pd.DataFrame(expense_data)
    if not expense_tags_df.empty and expense_tags_df['total'].sum() > 0:
        expense_total_sum = expense_tags_df['total'].sum()
        expense_tags_df['percentage'] = (expense_tags_df['total'] / expense_total_sum) * 100
        ax[1].pie(expense_tags_df['total'], colors=expense_tags_df['tag__color'].tolist(), startangle=90)
        ax[1].legend(
            [f"{name} ({percentage:.1f}%) " for name, percentage in zip(expense_tags_df['tag__name'], expense_tags_df['percentage'])],
            title="Expense Tags", loc="best", bbox_to_anchor=(0.9, 1))
    ax[1].set_title('Expenses by Tag')

    fig.tight_layout(pad=2.0)
    return _get_image_from_plot(fig)



def _generate_time_series_chart(transactions_df, time_unit):
    """Generates an income vs expense bar chart over time. Handles empty data gracefully."""
    # Debug prints
    print('--- Initial DataFrame for Time Series ---')
    print(transactions_df.head())

    if transactions_df.empty:
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.text(0.5, 0.5, 'No data for time series chart', fontsize=15, ha='center')
        ax.axis('off')
        return _get_image_from_plot(fig)

    df = transactions_df.copy()
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)

    resample_map = {
        'week': 'W', '15days': '15D', 'month': 'ME',
        '3months': '3MS', '6months': '6MS', 'year': 'A'
    }
    resample_freq = resample_map.get(time_unit, 'ME') # Default to month

    # Resample and align data
    income_df = df[df['type'] == 'income'].resample(resample_freq)['amount'].sum()
    expense_df = df[df['type'] == 'expense'].resample(resample_freq)['amount'].sum()
    
    aligned_income, aligned_expense = income_df.align(expense_df, join='outer', axis=0, fill_value=0)

    # Debug prints
    print('--- Aligned Income Data ---')
    print(aligned_income.head())
    print('--- Aligned Expense Data ---')
    print(aligned_expense.head())

    if aligned_income.empty and aligned_expense.empty:
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.text(0.5, 0.5, 'No data to display in chart', fontsize=15, ha='center')
        ax.axis('off')
        return _get_image_from_plot(fig)

    # Plotting
    fig, ax = plt.subplots(figsize=(15, 8))
    bar_width = pd.Timedelta(days=3) # Adjust width as needed
    index = aligned_income.index

    ax.bar(index - bar_width/2, aligned_income, width=bar_width, label='Income', color='green', align='center')
    ax.bar(index + bar_width/2, aligned_expense, width=bar_width, label='Expense', color='red', align='center')

    ax.set_xlabel('Date')
    ax.set_ylabel('Amount')
    ax.set_title('Income vs Expense Over Time')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xticks(rotation=45, ha="right")
    ax.legend()
    fig.tight_layout()

    return _get_image_from_plot(fig)

@login_required
def generate_report(request):
    one_year_ago = timezone.now().date() - timedelta(days=365)
    try:
        start_date_str = request.GET.get('start_date', one_year_ago.strftime('%Y-%m-%d'))
        start_date = pd.to_datetime(start_date_str).date()
    except (ValueError, TypeError):
        start_date = one_year_ago

    time_unit = request.GET.get('time_unit', 'month')

    base_transactions = Transaction.objects.filter(user=request.user, date__gte=start_date)

    income_transactions = base_transactions.filter(type='income')
    expense_transactions = base_transactions.filter(type='expense')

    total_income = income_transactions.aggregate(total=Sum('amount'))['total'] or 0
    total_expenses = expense_transactions.aggregate(total=Sum('amount'))['total'] or 0
    income_transactions_count = income_transactions.count()
    expense_transactions_count = expense_transactions.count()

    income_tags_data = income_transactions.values('tag__name', 'tag__color').annotate(total=Sum('amount')).order_by('-total')
    expense_tags_data = expense_transactions.values('tag__name', 'tag__color').annotate(total=Sum('amount')).order_by('-total')

    time_series_data = base_transactions.values('date', 'type', 'amount')

    income_expenses_chart = _generate_tags_pie_chart(income_tags_data, expense_tags_data)
    graph_image = _generate_time_series_chart(pd.DataFrame(time_series_data), time_unit)

    context = {
       'total_income': total_income,
       'total_expenses': total_expenses,
       'income_transactions': income_transactions_count,
       'expense_transactions': expense_transactions_count,
       'income_expenses_chart': income_expenses_chart,
       'graph_image': graph_image,
       'time_unit': time_unit,
       'start_date': start_date.strftime('%Y-%m-%d'),
    }

    return render(request, 'reports/report.html', context)
