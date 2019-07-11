import json
import requests
from django.http import HttpResponseBadRequest
from indicators.sma import sma, rsi

def compare (first_parameter, condition, second_parameter):
    if condition == 'greater than':
        if first_parameter[-1] > second_parameter[-1]:
            return True
        else :
            return False
    elif condition == 'less than':
        if first_parameter[-1] < second_parameter[-1]:
            return True
        else :
            return False
    elif condition == 'crossed above':
        if first_parameter[-1] > second_parameter[-1] and first_parameter[-2] < second_parameter[-2]:
            return True
        else :
            return False
    elif condition == 'crossed below':
        if first_parameter[-1] < second_parameter[-1] and first_parameter[-2] > second_parameter[-2]:
            return True
        else :
            return False
    elif condition == 'equal to': 
        if first_parameter[-1] == second_parameter[-1]:
            return True
        else :
            return False


def check_conditions(entry_condition, exit_condition, datapoints, temp, live_results):
    
    
    if temp.buy_flag == 0:
        entry_flag = 1
        for i in range(0, len(entry_condition.first_parameter)):
            first_parameter = datapoints[entry_condition.first_parameter[i]]
            condition = entry_condition.condition[i]
            second_parameter = datapoints[entry_condition.second_parameter[i]]
            if compare(first_parameter, condition, second_parameter) == False:
                entry_flag = 0
                break
        if entry_flag == 1:
            temp.buy_flag = 1
            temp.save()
            live_results.buy_price.append(datapoints['close'][-1])
            live_results.buy_time.append(datapoints['ltt'][-1])
            live_results.save()
    else:
        exit_flag = 1
        for i in range(0,len(exit_condition.first_parameter)):
            first_parameter = datapoints[exit_condition.first_parameter[i]]
            condition = exit_condition.condition[i]
            second_parameter = datapoints[exit_condition.second_parameter[i]]
            if compare(first_parameter, condition , second_parameter) == False:
                exit_flag = 0
                break
        if exit_flag == 1:
            temp.buy_flag = 0
            temp.save()
            live_results.exit_price.append(datapoints['close'][-1])
            profit = float(live_results.buy_price[-1]) - live_results.exit_price[-1]
            live_results.exit_time.append(datapoints['ltt'][-1])
            live_results.profit.append(profit)
            live_results.save()
    


#same as backtest but calculates indicator data instead of input from the api
      
def deployed(entry_condition, exit_condition, temp, live_results):
    
    api_url = 'https://emt.edelweiss.in/edelmw-content/content/charts/main/M1/NSE/EQUITY/11536_NSE'
    api_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHAiOjAsImV4cCI6MTU2NDE2NjU2MCwiZmYiOiJNIiwiaXNzIjoiZW10IiwibmJmIjoxNTYxNTc0MjYwLCJhcHBpZCI6IjhiMDk2N2FlMDVkMDgzMmEyNTdlMzEyNzcxYWRmMjc2Iiwic3JjIjoiZW10bXciLCJpYXQiOjE1NjE1NzQ1NjAsImF2IjoiNC4xLjEiLCJiZCI6ImFuZHJvaWQtcGhvbmUifQ.PuKISoLOvi1cf0tY_zbivH2mc4yQE_EuosVBYEPpyN4'
    headers = {
        'accept': 'application/json',
        'appidkey': api_key,
        'content-type': 'application/json',
    }
    
    data = '{"frcConti":false,"crpAct":true,"conti":false, "chTyp":"Interval", "tiInLst": [{"tiTyp": "SMA", "tiIn": {"period" : 14}}, {"tiTyp": "SMA", "tiIn": {"period" : 100}}], "isPvl":true}'
    
    try:
        response = requests.post(api_url, headers=headers, data=data)
    except:
        return HttpResponseBadRequest("check your internet connection")
    
    if response.status_code == None:
        return HttpResponseBadRequest("check your internet connection")
    data = json.loads(response.content.decode('utf-8'))
    
    datapoints = {}
    pltpnts = data['data']['pltPnts']
    
    
    key_list = ['open','close', 'high', 'low' , 'vol' , 'ltt']
    
    for i in key_list:
        temp_list = [pltpnts[i][-2] ,pltpnts[i][-1]]
        datapoints[i] = temp_list
    
    for i in entry_condition.second_parameter:
        try:
            a = int(i)
            datapoints[i] = [a]*len(datapoints['close'])            
        except:
            continue
    for i in exit_condition.second_parameter:
        try:
            a = int(i)
            datapoints[i] = [a]*len(datapoints['close'])    
        except:
            continue
     
    #calculate the indicator data
        
    datapoints['SMA 14'] = sma(pltpnts['close'] , 14)
    datapoints['SMA 100'] = sma(pltpnts['close'] , 100)  
    datapoints['RSI 14'] = rsi(pltpnts['close'] , 14)
    
    
    check_conditions(entry_condition , exit_condition, datapoints, temp, live_results)