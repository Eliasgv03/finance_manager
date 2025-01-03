# Generated by Django 5.1.4 on 2024-12-30 01:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('currencies', '0002_insert_default_currencies'),
        ('tags', '0002_alter_tag_unique_together'),
        ('users', '0007_userprofile_balance'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('expense', 'Expense'), ('income', 'Income')], max_length=7)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('date', models.DateField()),
                ('description', models.TextField(blank=True, null=True)),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='currencies.currency')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='tags.tag')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='users.userprofile')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]