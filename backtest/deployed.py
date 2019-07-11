import json
import requests

api_url = 'https://emt.edelweiss.in/edelmw-content/content/charts/v2/main/M1/NSE/EQUITY/11536_NSE'
api_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHAiOjAsImV4cCI6MTU2NDE2NjU2MCwiZmYiOiJNIiwiaXNzIjoiZW10IiwibmJmIjoxNTYxNTc0MjYwLCJhcHBpZCI6IjhiMDk2N2FlMDVkMDgzMmEyNTdlMzEyNzcxYWRmMjc2Iiwic3JjIjoiZW10bXciLCJpYXQiOjE1NjE1NzQ1NjAsImF2IjoiNC4xLjEiLCJiZCI6ImFuZHJvaWQtcGhvbmUifQ.PuKISoLOvi1cf0tY_zbivH2mc4yQE_EuosVBYEPpyN4'
headers = {
    'accept': 'application/json',
    'appidkey': api_key,
    'content-type': 'application/json',
}

data = '{"frcConti":false,"crpAct":true,"conti":false, "chTyp":"Interval", "tiInLst": [{"tiTyp": "SMA", "tiIn": {"period" : 14}}, {"tiTyp": "SMA", "tiIn": {"period" : 100}}], "isPvl":true}'

response = requests.post(api_url, headers=headers, data=data)

data = json.loads(response.content.decode('utf-8'))


