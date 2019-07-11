from django.contrib import admin
from django.db import models
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class trade(models.Model):

    pos = models.IntegerField(default = 0)
    neg = models.IntegerField(default = 0) 
    profit = models.IntegerField(default = 0) 
    transaction = ArrayField(models.DecimalField(decimal_places = 3, max_digits= 9,default= 0), default = list)
    investment = ArrayField(models.DecimalField(decimal_places = 3, max_digits= 9,default = 0), default = list)
    sell = ArrayField(models.DecimalField(decimal_places = 3, max_digits= 9, default = 0), default = list)
    entry_date = ArrayField(models.CharField(max_length = 20, default=''), default = list )
    exit_date = ArrayField(models.CharField(max_length = 20, default = ''),default = list)
    name = models.CharField(max_length = 100, default = "hello")

    
    def summary(self):
        print("Total Profit: " + str(self.profit))
        print("Successful trades " + str(self.pos))
        print("Unsuccessful trade " + str(self.neg))

class conditions(models.Model):
    first_parameter = ArrayField(models.CharField(max_length = 100, default = ''), default = list)
    condition = ArrayField(models.CharField(max_length = 100, default = ''), default = list)
    second_parameter = ArrayField(models.CharField(max_length = 100, default = ''), default = list)
    
    def summary(self):
        print(self.first_parameter)
        print(self.condition)
        print(self.second_parameter)
    
admin.site.register(trade) 
admin.site.register(conditions)