# Generated by Django 2.2.2 on 2019-06-25 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backtest', '0002_auto_20190625_1551'),
    ]

    operations = [
        migrations.AddField(
            model_name='trade',
            name='name',
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='trade',
            name='neg',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='trade',
            name='pos',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='trade',
            name='profit',
            field=models.IntegerField(default=0),
        ),
    ]
