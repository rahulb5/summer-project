from django import forms

# Create your models here.
#class data (models.Model):
#    open_data = models.TextField(null = True)
#    close_data = models.TextField(null = True)
#    high_data = models.TextField(null = True)
#    low_data = models.TextField(null = True)
#    volume_data = models.TextField(null = True)
#    ltt_data = models.TextField(null = True)
    
class dataform(forms.Form):
    first_parameter = forms.CharField()
    second_parameter = forms.CharField()