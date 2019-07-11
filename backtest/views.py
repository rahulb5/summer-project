from django.shortcuts import render
from backtest.main import main
from .models import conditions, trade
from django.http import HttpResponseBadRequest
from deploy.models import live_model, results
import time
from threading import Thread
from deploy.deploy import deployed

#to store the entered parameters

class query:
    def __init__ (self):
        self.first_parameter = ""
        self.condition = ""
        self.second_parameter = "" 

def get_data(request):        
    return render(request, 'get_data.html' , {})

#to kill the thread
    
variable = 0

def thread_kill():
    global variable 
    
    #kill the thread
    
    variable = 1

def submit(request):
    
    #calling the variables
    
    var_id = request.session['saved']
    back = trade.objects.get(id = var_id)
    
    temp_id = request.session['temp_id']
    temp = live_model.objects.get(id = temp_id)
    
    
    if request.method == 'POST': 
        
        #taking the input from front end to back end
        
        user_entry_condition = []
        user_exit_condition = []
        user_entry_condition.append(request.POST.getlist('entry parameter'))
        user_entry_condition.append(request.POST.getlist('entry condtion'))
        user_entry_condition.append(request.POST.getlist('second_entry_parameter'))
        
        user_exit_condition.append(request.POST.getlist('exit parameter'))
        user_exit_condition.append(request.POST.getlist('exit condition'))
        user_exit_condition.append(request.POST.getlist('second exit parameter'))

        #if some error in input raise an exception

        try:
            back = main(user_entry_condition, user_exit_condition)
            back.save()
        except:
            return HttpResponseBadRequest("please fill the fields correctly or check you connection")
        
        #same the condtions
        
        entry_conditions = conditions()
        entry_conditions.first_parameter = user_entry_condition[0]
        entry_conditions.condition = user_entry_condition[1] 
        entry_conditions.second_parameter = user_entry_condition[2]
        entry_conditions.save()
        
        exit_conditions = conditions()
        exit_conditions.first_parameter= user_exit_condition[0]
        exit_conditions.condition = user_exit_condition[1]
        exit_conditions.second_parameter = user_exit_condition[2]
        exit_conditions.save()
        
        
        
        request.session['saved'] = back.id
        request.session['entry_conditions'] = entry_conditions.id
        request.session['exit_conditions'] = exit_conditions.id


        
    return render(request , "submit.html" , {
        'back' : back,  
        'deploy' : temp.deployed,
        })

def details(request):
    
    var_id = request.session['saved']
    details = trade.objects.get(id = var_id)
    details.summary()
    rang = len(details.exit_date)
    
    #to show backtest data in tablulated format
    
    zippped_list = zip(details.investment, details.entry_date,details.sell,details.exit_date,details.transaction)
    
    return render(request, 'details.html' , {'detail': details,'zipped_list':zippped_list, 'range' : range(rang)})


#to deploy the strategy

def callsss(request):
    
    #get the variables
    
    entry_id = request.session['entry_conditions']
    exit_id = request.session['exit_conditions']
    temp_id = request.session['temp_id']
    live_results_id = request.session['live_results']
    
    entry_condition = conditions.objects.get(id = entry_id)
    exit_condition = conditions.objects.get(id = exit_id)
    temp = live_model.objects.get(id = temp_id)
    live_results = results.objects.get(id = live_results_id)
    temp.deployed = 1
    temp.save()
    
    global variable
    variable = 0
    
    #while the strategy is deployed
    
    while variable == 0:
        deployed(entry_condition, exit_condition, temp, live_results)        
        
        #can print results.profit to see the profit (available in deployed details though)
        
        time.sleep(5)
        
        

def deploy_strategy(request):
    
    #deploy the strategy    
    
    t = Thread(target = callsss , args = (request, ))
    t.daemon = True
    t.start()
    
    return render(request , "deployed.html" , {})