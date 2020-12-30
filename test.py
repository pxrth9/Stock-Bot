import requests

url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-profile"

querystring = {"symbol":'TSLA',"region":"US"}

headers = {
    'x-rapidapi-key': '671f685758msh1b9f31f4ca697d8p153f69jsn296e1b470257',
    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
}

json  = requests.get(url, headers=headers, params=querystring).json()

print(json['price']['regularMarketPrice']['raw'])