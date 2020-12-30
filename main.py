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
def yahoo_call_get_profile(ticker, YAHOO_FINANCE):
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
    help =('```!prce [TICKER] -> Stock Price '
        +'\n!time -> Stock Market Hours and Current Time '
        +'\n!info [TICKER] -> Stock Company Name'
        +'\n!trnd [TICEKR] -> Stock Trend ```')
    await message.channel.send(help)

  if msg.startswith('!prce'):
    ticker_symbol = msg.split('!prce ', 1)[1]
    json_config = yahoo_call_get_profile(ticker_symbol, YAHOO_FINANCE)
    if json_config != -1:    
      stock_price = json_config['price']['regularMarketPrice']['raw']
      ath_day = json_config['price']['regularMarketDayHigh']['raw']
      atl_day = json_config['price']['regularMarketDayLow']['raw']
      msg = ('```Current Price: '  + str(stock_price)  
          +'\nDay\'s all time high: '  + str(ath_day) 
          +'\nDay\'s all time low: '  + str(atl_day) + '```')
      await message.channel.send(msg)
    else:
      await message.channel.send("Stock Invalid! Please check for errors!")

  if msg.startswith('!time'):
    current_time = time.strftime("%H:%M:%S")
    stock_market_time = "09:30:00  to 16:00:00"
    msg = ('Current Time: ' + current_time 
        +'\nStock Market Time: ' + stock_market_time) 
    await message.channel.send(msg)

  if msg.startswith('!info'):
    ticker_symbol = msg.split('!info ', 1)[1]
    json_config = yahoo_call_get_profile(ticker_symbol, YAHOO_FINANCE)
    if json_config != -1:
      company_name = json_config['quoteType']['longName']
      company_sector = json_config['assetProfile']['sector']
      company_summary = json_config['assetProfile']['longBusinessSummary']
      msg = ('**Company Name:**     ' + '*' + company_name + '*' 
          +'\n**Company Sector:**   ' + '*' + company_sector + '*'
          +'\n**Company Summary:**  ' + '*' + company_summary + '*')
      await message.channel.send(msg)
    else:
      await message.channel.send("Stock Invalid! Check for errors!")

  if msg.startswith('!trnd'):
    ticker_symbol = msg.split('!trnd ', 1)[1]
    json_config = yahoo_call_get_profile(ticker_symbol, YAHOO_FINANCE)
    if json_config != -1:
      sTT = json_config['pageViews']['shortTermTrend']
      mTT = json_config['pageViews']['midTermTrend']
      lTT =json_config['pageViews']['longTermTrend']
      msg = ('```Short Term Trend: '  + sTT  
          +'\nMid Term Trend: '  + mTT 
          +'\nLong Term Trend: '  + lTT + '```')
      await message.channel.send(msg)
    else:
      await message.channel.send("Stock Invalid! Check for errors!") 


client.run(DISCORD_API)