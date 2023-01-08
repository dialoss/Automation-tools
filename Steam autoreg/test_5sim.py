import requests
import json

token = '***'
country = 'russia'
operator = 'any'
product = 'other'
id = 196962812

headers = {
    'Authorization': 'Bearer ' + token,
    'Accept': 'application/json',
}

buy_number = requests.get('https://5sim.net/v1/user/buy/activation/' + country + '/' + operator + '/' + product, headers=headers)
print(buy_number.text)
response = requests.get('https://5sim.net/v1/user/check/' + str(id), headers=headers)
print(response.text)
print(json.loads(response.text)["phone"])
