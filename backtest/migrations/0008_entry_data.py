# Generated by Django 2.2.2 on 2019-07-02 04:54

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backtest', '0007_auto_20190625_2027'),
    ]

    operations = [
        migrations.CreateModel(
            name='entry_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_parameter', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(default='', max_length=100), default=list, size=None)),
                ('condition', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(default='', max_length=100), default=list, size=None)),
                ('second_parameter', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(default='', max_length=100), default=list, size=None)),
            ],
        ),
    ]
