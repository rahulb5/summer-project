# Generated by Django 2.2.2 on 2019-06-25 14:57

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backtest', '0006_auto_20190625_2025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trade',
            name='entry_date',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(default='', max_length=20), default=list, size=None),
        ),
        migrations.AlterField(
            model_name='trade',
            name='exit_date',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(default='', max_length=20), default=list, size=None),
        ),
    ]
