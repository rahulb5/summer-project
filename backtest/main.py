from .models import trade
from django.http import HttpResponseBadRequest
import json
import requests       

#class to store the condition parameters

class query:
    def __init__ (self):
        self.first_parameter = ""
        self.condition = ""
        self.second_parameter = "" 
        
#self explainatory    
        
def compare (condition , first_parameter, prev_first_paramter , second_parameter , prev_second_parameter):
    if condition == 'greater than':
        if first_parameter > second_parameter:
            return True
        else :
            return False
    elif condition == 'less than':
        if first_parameter < second_parameter:
            return True
        else :
            return False
    elif condition == 'crossed above':
        if first_parameter > second_parameter and prev_first_paramter < prev_second_parameter:
            return True
        else :
            return False
    elif condition == 'crossed below':
        if first_parameter < second_parameter and prev_first_paramter > prev_second_parameter:
            return True
        else :
            return False
    elif condition == 'equal to': 
        if first_parameter == second_parameter:
            return True
        else :
            return False

def backtest(user_entry_condition , user_exit_condition , datapoints , qty):
    
 #devlaring a variable to store the values   
    buy_flag = 0
    back = trade()
    back.name = "back"

    
    for i in range(1,len(datapoints['open'])):
        
        #checking if some stock has already been bought
        
        if buy_flag == 0:
            flag_entry_condition = 0
            
            #checking if all the entered entry conditions are satisfied
            
            for j in user_entry_condition:
                variable = compare(j.condition , datapoints[j.first_parameter][i], datapoints[j.first_parameter][i-1],datapoints[j.second_parameter][i] , datapoints[j.second_parameter][i-1])
                if variable == False:
                    flag_entry_condition = 1
                    break
            
            #if conditions are satisfied, buy
            
            if flag_entry_condition == 0: 
                buy_flag = 1
                back.investment.append(qty*datapoints['close'][i])
                back.entry_date.append(datapoints['ltt'][i])
             
        
        #if some stock has already been bought
                
        else:
            flag_exit_condition = 0
            
             #checking if all the entered exit conditions are satisfied
            
            for j in user_exit_condition:
                if not compare(j.condition , datapoints[j.first_parameter][i],datapoints[j.first_parameter][i-1],datapoints[j.second_parameter][i] , datapoints[j.second_parameter][i-1]):
                    flag_exit_condition = 1
                    break
            
            #if conditions are satisfied, exit
            
            if flag_exit_condition == 0:
                buy_flag = 0
                back.sell.append(qty*datapoints['close'][i])
                back.exit_date.append(datapoints['ltt'][i])
                profit = back.sell[-1] - back.investment[-1]
                back.profit = back.profit + profit
                back.transaction.append(profit)
                if profit >= 0:
                    back.pos += 1
                else:
                    back.neg += 1
                
                
    return back

def main(entry_condition , exit_condition):    
    
    #sorting out relevant datapoints        
    
    api_url = 'https://emt.edelweiss.in/edelmw-content/content/charts/v2/main/D1/NSE/EQUITY/11536_NSE'
    api_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHAiOjAsImV4cCI6MTUzMTQ1MjU0MywiZmYiOiJNIiwiaXNzIjoiZW10IiwibmJmIjoxNTI4ODYwMjQzLCJhcHBpZCI6ImM2ZjZhMDMzYjBiZWY1OTExNzNmNjM1N2I4YTllMDYyIiwic3JjIjoiZW10bXciLCJpYXQiOjE1Mjg4NjA1NDMsImF2IjoiMTUuMSIsImJkIjoiYW5kcm9pZC1waG9uZSJ9.BruotpCV-NyiCmeSAPm_AvyeY6kYzF04TWSvtIOnpfc'
    headers = {
        'accept': 'application/json',
        'appidkey': api_key,
        'content-type': 'application/json',
    }
    
    
    data = '{"frcConti":false,"crpAct":true,"conti":false, "chTyp":"Interval", "tiInLst": [{"tiTyp": "SMA", "tiIn": {"period" : 14}}, {"tiTyp": "SMA", "tiIn": {"period" : 100}}, {"tiTyp": "RSI", "tiIn": {"period" : 14}}], "isPvl":true}'
      
    try:
        response = requests.post(api_url, headers=headers, data=data)
    except:
        return HttpResponseBadRequest("check your internet connection")
    
    if response.status_code == None:
        return HttpResponseBadRequest("check your internet connection")
    
    data = json.loads(response.content.decode('utf-8'))
    
    pltPnts = data['data']['pltPnts']
    tiOut = data['data']['tiOut']
    
    #storing all the datapoints in a variable
    
    datapoints = {}
    for key in pltPnts.keys():
        datapoints[key] = pltPnts[key]
    
    for index in range(0, len(tiOut)):
        temp_index = data['data']['tiOut'][index]['tiTyp'] + " " + data['data']['tiOut'][index]['tiIn']['period']
        datapoints[temp_index] = tiOut[index]['rsltSet'][0]['vals']
    
    datapoints[''] = "None"
    user_entry_condition = []
    user_exit_condition = []
    
    #converting numeric entries if there are any
    
    for i in entry_condition[2]:
        try:
            a = int(i)
            datapoints[i] = [a]*len(datapoints['close'])
            
        except:
            continue
    for i in exit_condition[2]:
        try:
            a = int(i)
            datapoints[i] = [a]*len(datapoints['close'])
            
        except:
            continue
    
    #making variable to pass the entry/exit conditions
    
    for i in range(0,len(entry_condition[0])):
        temp = query()
        user_entry_condition.append(temp)
        user_entry_condition[i].first_parameter = entry_condition[0][i]
        user_entry_condition[i].condition = entry_condition[1][i]
        user_entry_condition[i].second_parameter = entry_condition[2][i]
      
    for i in range(0,len(exit_condition[0])):
        temp = query()
        user_exit_condition.append(temp)
        user_exit_condition[i].first_parameter = exit_condition[0][i]
        user_exit_condition[i].condition = exit_condition[1][i]
        user_exit_condition[i].second_parameter = exit_condition[2][i]

    return backtest(user_entry_condition, user_exit_condition , datapoints , 1)