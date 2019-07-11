from django.shortcuts import render
from deploy.models import results, live_model


def homepage(request):

#Initialising the models to be used for deploy in a separate app as it gies convinience to truncate 
#the model in deploy/backtest app
    
    live_results = results()
    live_results.save()
    request.session['live_results'] = live_results.id
    
    temp = live_model()
    temp.buy_flag = 0
    temp.deployed = 0
    temp.save()
    request.session['temp_id'] = temp.id
    
    var = trade()
    var.save()
    request.session['saved'] = var.id
   
    return render(request, "main/home.html", {})
