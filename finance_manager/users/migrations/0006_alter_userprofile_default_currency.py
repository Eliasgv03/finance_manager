# Generated by Django 5.1.4 on 2024-12-25 21:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currencies', '0002_insert_default_currencies'),
        ('users', '0005_alter_userprofile_default_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='default_currency',
            field=models.ForeignKey(default=146, null=True, on_delete=django.db.models.deletion.SET_NULL, to='currencies.currency'),
        ),
    ]