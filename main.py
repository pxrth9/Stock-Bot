import os 
import discord 
import requests
import time


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

  return requests.get(url, headers=headers, params=querystring).json()
  

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
        +'\n `!time -> Stock Market Hours and Current Time '
        +'\n `!stock [TICKER] -> Stock Company Name')
    await message.channel.send(message.channel, help)

  if msg.startswith('!price'):
    ticker_symbol = msg.split('!price ', 1)[1]
    json_config = yahoo_call(ticker_symbol, YAHOO_FINANCE)
    stock_price = json_config['price']['regularMarketPrice']['raw']
    await message.channel.send("Stock Price: " + str(stock_price))

  if msg.startswith('!time'):
    current_time = time.strftime("%H:%M:%S")
    stock_market_time = "09:30:00  to 16:00:00"
    m = ('Current Time: ' + current_time 
       + '\nStock Market Time: ' + stock_market_time) 
    await message.channel.send(m)
    



client.run(DISCORD_API)