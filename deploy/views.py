from django.shortcuts import render
from .models import live_model, results
from django.shortcuts import redirect
from backtest.views import thread_kill

def truncate(request):
    
    #delete the deployed model
    
    try:
        live_results_id = request.session['live_results']
    except: 
        return redirect('http://127.0.0.1:8000/get_data/submit')
    
    live_results = results.objects.get(id = live_results_id)
    live_results.delete()    
    
    #reinitialise the model
    
    live_results = results()
    live_results.save()
    request.session['live_results'] = live_results.id

    
    
    temp_id = request.session['temp_id']
    temp = live_model.objects.get(id = temp_id)
    temp.buy_flag = 0
    temp.deployed = 0
    temp.save()
    
    #kill the deploy thread    
    
    thread_kill()

    return redirect('http://127.0.0.1:8000/get_data/submit')

def deploy(request):
    
    live_results_id = request.session['live_results']
    live_results = results.objects.get(id = live_results_id)

    #to show the data in a tabular format

    zipped_list1 = zip(live_results.buy_price, live_results.buy_time )
    zipped_list2 = zip(live_results.exit_price, live_results.exit_time, live_results.profit)
    
    content = {'zipped_list1': zipped_list1, 'zipped_list2' : zipped_list2}
    
    return render(request, 'deploy.html' , content)
