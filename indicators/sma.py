import statistics as stat
from django.http import HttpResponseBadRequest

def sma(data, period):
    temp_data = data[-period +2 : -2]
    temp = []
    temp.append(stat.mean(temp_data))
    temp_data = data[-period+1 : -1]
    temp.append(stat.mean(temp_data))
    return temp

def rsi(data, period):
    if len(data) < period:
        return HttpResponseBadRequest("Data not sufficient")
    temp = data[0:period]
    total_gain = 0
    temp_change = 0
    total_loss = 0 
    for i in range(1,len(temp)):
        temp_change = temp[i] - temp[i-1]
        if temp_change > 0:
            total_gain += temp_change
        else :
            total_loss += temp_change
    prev_avg_gain = total_gain/period
    prev_avg_loss = abs(total_loss)/period
    rs = prev_avg_gain/prev_avg_loss
    int_rsi = 100 - 100/(1+rs)
    rsi = [int_rsi]
    
    try:
        for i in range(period ,len(data)) :
            change = data[i] - data[i-1]
            temp_gain = 0
            temp_loss = 0
            if change > 0:
                temp_gain = change
            else:
                temp_loss = abs(change)
            avg_gain = (prev_avg_gain*(period-1) + temp_gain)/period
            avg_loss = (prev_avg_loss*(period-1) + temp_loss)/period
            prev_avg_gain = avg_gain
            prev_avg_loss = avg_loss
            rs = avg_gain/abs(avg_loss)
            int_rsi = 100 - 100/(1+rs)
            rsi.append(int_rsi)
        return rsi
    except:
        return rsi