import os 
import discord 
import requests
import time
import json


#API-KEYS
DISCORD_API = os.getenv('DISCORD_KEY')
YAHOO_FINANCE = os.getenv('YAHOO_FINANCE_KEY')


'''
Return value required
returns the API call in a json config 
'''
def yahoo_call(ticker, YAHOO_FINANCE):
  url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-profile"

  querystring = {"symbol":ticker,"region":"US"}

  headers = {
      'x-rapidapi-key': YAHOO_FINANCE,
      'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
  }

  json_data = requests.get(url, headers=headers, params=querystring).json()

  return json_data if json.dumps(json_data) else -1
  

# Create Discord Object 
client = discord.Client()

@client.event
async def on_ready():
  print("Bot Ready!")

@client.event
async def on_message(message):

  msg = message.content
  if msg.startswith('!help'):
    help = ('`!price [TICKER] -> Current Stock Price` '
        +'\n`!time -> Stock Market Hours and Current Time `'
        +'\n`!stock [TICKER] -> Stock Company Name`')
    await message.channel.send(help)

  if msg.startswith('!price'):
    ticker_symbol = msg.split('!price ', 1)[1]
    json_config = yahoo_call(ticker_symbol, YAHOO_FINANCE)
    if json_config != -1:    
      stock_price = json_config['price']['regularMarketPrice']['raw']
      await message.channel.send("Stock Price: " + str(stock_price))
    else:
      await message.channel.send("Stock Invalid! Please check for errors!")

  if msg.startswith('!time'):
    current_time = time.strftime("%H:%M:%S")
    stock_market_time = "09:30:00  to 16:00:00"
    m = ('Current Time: ' + current_time 
       + '\nStock Market Time: ' + stock_market_time) 
    await message.channel.send(m)

  if msg.startswith('!stock'):
    ticker_symbol = msg.split('!stock ', 1)[1]

    



client.run(DISCORD_API)