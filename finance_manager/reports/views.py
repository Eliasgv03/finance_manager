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

def generate_report(request):
    start_date = pd.to_datetime(request.GET.get('start_date', '2020-01-01')) 
    income_transactions = Transaction.objects.filter(type='income', date__gte=start_date)
    expense_transactions = Transaction.objects.filter(type='expense', date__gte=start_date)

    total_income = income_transactions.aggregate(total=Sum('amount'))['total'] or 0
    total_expenses = expense_transactions.aggregate(total=Sum('amount'))['total'] or 0

    income_transactions_count = income_transactions.count()
    expense_transactions_count = expense_transactions.count()

    income_tags_data = income_transactions.values('tag__name', 'tag__color').annotate(total_income=Sum('amount'))
    expense_tags_data = expense_transactions.values('tag__name', 'tag__color').annotate(total_expenses=Sum('amount'))

    income_tags_df = pd.DataFrame(income_tags_data)
    expense_tags_df = pd.DataFrame(expense_tags_data)

    total_income_sum = income_tags_df['total_income'].sum()
    total_expenses_sum = expense_tags_df['total_expenses'].sum()

    income_tags_df['percentage'] = (income_tags_df['total_income'] / total_income_sum) * 100
    expense_tags_df['percentage'] = (expense_tags_df['total_expenses'] / total_expenses_sum) * 100

    income_colors = income_tags_df['tag__color'].tolist()
    expense_colors = expense_tags_df['tag__color'].tolist()

    fig, ax = plt.subplots(1, 2, figsize=(15, 8))  
    ax[0].pie(income_tags_df['total_income'], colors=income_colors, startangle=90, textprops={'color': 'black', 'fontsize': 18})
    ax[0].set_title('Income by Tag', fontsize=20)
    ax[0].legend(
        labels=[f"{name} - {color} - {percentage:.1f}%" 
                for name, color, percentage in zip(income_tags_df['tag__name'], income_colors, income_tags_df['percentage'])],
        loc="center", bbox_to_anchor=(0.5, -0.15), ncol=1, fontsize=14, title_fontsize=16
    )
    
    
    ax[1].pie(expense_tags_df['total_expenses'], colors=expense_colors, startangle=90, textprops={'color': 'black', 'fontsize': 18})
    ax[1].set_title('Expenses by Tag', fontsize=20)
    
    ax[1].legend(
        labels=[f"{name} - {color} - {percentage:.1f}%" 
                for name, color, percentage in zip(expense_tags_df['tag__name'], expense_colors, expense_tags_df['percentage'])],
        loc="center", bbox_to_anchor=(0.5, -0.15), ncol=1, fontsize=14
    )

    pie_image = BytesIO()
    plt.savefig(pie_image, format='png', bbox_inches='tight', dpi=100)
    pie_image.seek(0)
    income_expenses_chart = base64.b64encode(pie_image.getvalue()).decode()

    time_unit = request.GET.get('time_unit', 'M') 

    income_transactions = Transaction.objects.filter(type='income').values('date', 'amount')
    expense_transactions = Transaction.objects.filter(type='expense').values('date', 'amount')

    income_df = pd.DataFrame(income_transactions)
    expense_df = pd.DataFrame(expense_transactions)
 
    income_df['date'] = pd.to_datetime(income_df['date'])
    expense_df['date'] = pd.to_datetime(expense_df['date'])

    income_df.set_index('date', inplace=True)
    expense_df.set_index('date', inplace=True)

    if time_unit == 'week':
        income_df_resampled = income_df.resample('W').sum()  
        expense_df_resampled = expense_df.resample('W').sum()
    elif time_unit == '15days':
        income_df_resampled = income_df.resample('15D').sum() 
        expense_df_resampled = expense_df.resample('15D').sum()
    elif time_unit == 'month':
        income_df_resampled = income_df.resample('M').sum()  
        expense_df_resampled = expense_df.resample('M').sum()
    elif time_unit == '3months':
        income_df_resampled = income_df.resample('3MS').sum()  
        expense_df_resampled = expense_df.resample('3MS').sum()
    elif time_unit == '6months':
        income_df_resampled = income_df.resample('6MS').sum()  
        expense_df_resampled = expense_df.resample('6MS').sum()
    elif time_unit == 'year':
        income_df_resampled = income_df.resample('A').sum()  
        expense_df_resampled = expense_df.resample('A').sum()
    else:
        income_df_resampled = income_df
        expense_df_resampled = expense_df

    income_df_resampled, expense_df_resampled = income_df_resampled.align(expense_df_resampled, join='outer', axis=0, fill_value=0)

    dates = income_df_resampled.index
    income_values = income_df_resampled['amount']
    expense_values = expense_df_resampled['amount']

   
    fig, ax = plt.subplots(figsize=(15, 8))
    width = 3  
    ax.bar(dates - pd.Timedelta(days=width/2), income_values, width, label='Income', color='green')
    ax.bar(dates + pd.Timedelta(days=width/2), expense_values, width, label='Expense', color='red')

    ax.set_xlabel('Time', fontsize=18)
    ax.set_ylabel('Amount ($)', fontsize=18)
    ax.set_title('Income vs Expense Over Time', fontsize=18)

 
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45, ha="right", fontsize=10)

    ax.legend()

    
    fig.tight_layout(pad=3.0)

  
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png', bbox_inches='tight')
    image_stream.seek(0)
    graph_image = base64.b64encode(image_stream.getvalue()).decode()

    context = {
       'total_income': total_income,
       'total_expenses': total_expenses,
       'income_transactions': income_transactions_count,
       'expense_transactions': expense_transactions_count,
       'income_expenses_chart': income_expenses_chart,
       'graph_image': graph_image,
       'time_unit': time_unit
    }

    return render(request, 'reports/report.html', context)
