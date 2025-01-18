from django.shortcuts import render
from django.db.models import Sum
from transactions.models import Transaction
from tags.models import Tag
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from io import BytesIO
import base64

matplotlib.use('Agg')

def generate_report(request):
    # Obtener los datos de ingresos y gastos
    total_income = Transaction.objects.filter(type='income').aggregate(total=Sum('amount'))['total'] or 0
    total_expenses = Transaction.objects.filter(type='expense').aggregate(total=Sum('amount'))['total'] or 0

    income_transactions = Transaction.objects.filter(type='income').count()
    expense_transactions = Transaction.objects.filter(type='expense').count()

    # Obtener los totales por tag para ingresos
    income_tags_data = Transaction.objects.filter(type='income') \
        .values('tag__name', 'tag__color') \
        .annotate(total_income=Sum('amount'))

    # Obtener los totales por tag para gastos
    expense_tags_data = Transaction.objects.filter(type='expense') \
        .values('tag__name', 'tag__color') \
        .annotate(total_expenses=Sum('amount'))

    # Convertir los datos a DataFrame para manipularlos fácilmente
    income_tags_df = pd.DataFrame(income_tags_data)
    expense_tags_df = pd.DataFrame(expense_tags_data)

    # Calcular los porcentajes para cada tag
    total_income_sum = income_tags_df['total_income'].sum()
    total_expenses_sum = expense_tags_df['total_expenses'].sum()

    income_tags_df['percentage'] = (income_tags_df['total_income'] / total_income_sum) * 100
    expense_tags_df['percentage'] = (expense_tags_df['total_expenses'] / total_expenses_sum) * 100

    # Colores de los tags
    income_colors = income_tags_df['tag__color'].tolist()
    expense_colors = expense_tags_df['tag__color'].tolist()

    # Gráficos de pastel
    fig, ax = plt.subplots(1, 2, figsize=(15, 8))  # Aumentamos el tamaño de la figura

    # Gráfico de ingresos por tag
    ax[0].pie(
        income_tags_df['total_income'], 
        colors=income_colors, 
        startangle=90,
        textprops={'color': 'black', 'fontsize': 18}  # Aumentar tamaño de letra
    )
    ax[0].set_title('Income by Tag', fontsize=20)

    # Mover la leyenda debajo del gráfico de ingresos con más tamaño y 2 columnas
    ax[0].legend(
        labels=[
            f"{name} - {color} - {percentage:.1f}%" 
            for name, color, percentage in zip(income_tags_df['tag__name'], income_colors, income_tags_df['percentage'])
        ],
        title="Tags", 
        loc="center", 
        bbox_to_anchor=(0.5, -0.35),  # Mover más hacia abajo
        ncol=2,  # Dos columnas
        fontsize=12,  # Aumentar tamaño de la leyenda
        title_fontsize=14  # Aumentar tamaño del título de la leyenda
    )

    # Gráfico de gastos por tag
    ax[1].pie(
        expense_tags_df['total_expenses'], 
        colors=expense_colors, 
        startangle=90,
        textprops={'color': 'black', 'fontsize': 18}  # Aumentar tamaño de letra
    )
    ax[1].set_title('Expenses by Tag', fontsize=20)

    # Mover la leyenda debajo del gráfico de gastos con más tamaño y 2 columnas
    ax[1].legend(
        labels=[
            f"{name} - {color} - {percentage:.1f}%" 
            for name, color, percentage in zip(expense_tags_df['tag__name'], expense_colors, expense_tags_df['percentage'])
        ],
        title="Tags", 
        loc="center", 
        bbox_to_anchor=(0.5, -0.35),  # Mover más hacia abajo
        ncol=2,  # Dos columnas
        fontsize=12,  # Aumentar tamaño de la leyenda
        title_fontsize=14  # Aumentar tamaño del título de la leyenda
    )

    # Convertir gráfico a base64
    pie_image = BytesIO()
    plt.savefig(pie_image, format='png', bbox_inches='tight', dpi=100)
    pie_image.seek(0)
    income_expenses_chart = base64.b64encode(pie_image.getvalue()).decode()

    # Contexto para la vista
    context = {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'income_transactions': income_transactions,
        'expense_transactions': expense_transactions,
        'income_expenses_chart': income_expenses_chart,
    }
    return render(request, 'reports/report.html', context)
