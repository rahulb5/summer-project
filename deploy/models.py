from django.db import models
from django.contrib import admin
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class live_model(models.Model):
    
    #to check if some stock has been bought
    
    buy_flag = models.IntegerField()
    
    #to check if some strategy has already been deployed
    
    deployed = models.IntegerField()
    
class results(models.Model):
    buy_price = ArrayField(models.DecimalField(decimal_places = 3, max_digits= 9,default= 0), default = list)
    exit_price= ArrayField(models.DecimalField(decimal_places = 3, max_digits= 9,default= 0), default = list)
    buy_time = ArrayField(models.CharField(max_length = 20, default=''), default = list )
    exit_time = ArrayField(models.CharField(max_length = 20, default=''), default = list )
    profit = ArrayField(models.DecimalField(decimal_places = 3, max_digits= 9,default= 0), default = list)

admin.site.register(live_model)
admin.site.register(results)