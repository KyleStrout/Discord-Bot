import discord
import os
import requests #allows bot to make http request to get data from api, returns json
import json #easier to work with data returned
import random
from flask import request
from replit import db
from keep_alive import keep_alive



#curl --location --request
#GET 'https://api.twitch.tv/helix/search/channels?query=laevus' \
#--header 'client-id: p3atoxiilwa9je4t03twaedr5877mf' \
#--header 'Authorization: Bearer 2gbdx6oar67tqtcmt49t3wpcgycthx'


my_secret = os.environ['TOKEN']
CID = os.environ['CLIENT_ID']
TOKEN = os.environ['OATH_TOKEN']  
TWITCH_SECRET = 'good'
streamer_name = 'laevus'

API_HEADERS = {
  'client_ID': CID,
  'client_secret': TOKEN,
  "grant_type": 'client credentials'
}

client = discord.Client()

def checkIfLive(): #this shit dont work
  r = requests.post('https://discord.com/api/oauth2/authorize?client_id=839072169128493056&permissions=2148002880&scope=bot', API_HEADERS)
  
  keys = r.json()

  print(keys)

  headers = {
    'Client-ID': CID,
    'Authorization': 'Bearer ' + keys['access_token']
  }

  print(headers)
  
  stream = requests.get('https://api.twitch.tv/helix/streams?user_login=' + streamer_name, headers=headers)

  stream_data = stream.json();

  print(stream_data);
  if len(stream_data['data']) == 1:
    print(streamer_name + ' is live: ' + stream_data['data'][0]['title'] + ' playing ' + stream_data['data'][0]['game_name']);
  else:
      print(streamer_name + ' is not live');

def getQuote():
  response = requests.get('https://zenquotes.io/api/random')
  json_data = json.loads(response.text)
  print(json_data)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return quote



@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('$hello'):
    await message.channel.send('Hello!')

  if message.content.startswith('$quote'):
    quote = getQuote()
    await message.channel.send(quote)

  if message.content.startswith('$roll'):
    x = random.randrange(0, 100)
    y = message.author.name
    await message.channel.send(y + ' rolled a ' + str(x) + '!')

  if message.content.startswith('$stream'):
    
    await message.channel.send('cool')

keep_alive()
client.run(my_secret)  
