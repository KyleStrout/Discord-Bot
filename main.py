import discord
import os
import requests #allows bot to make http request to get data from api, returns json
import json #easier to work with data returned
import random
from flask import Flask, request, Response
from keep_alive import keep_alive
from replit import db



#curl --location --request
#GET 'https://api.twitch.tv/helix/search/channels?query=laevus' \
#--header 'client-id: p3atoxiilwa9je4t03twaedr5877mf' \
#--header 'Authorization: Bearer 2gbdx6oar67tqtcmt49t3wpcgycthx'

# secrets, twitch tokens, global vars
my_secret = os.environ['TOKEN']
CID = os.environ['CLIENT_ID']
OATH_TOKEN = os.environ['OATH_TOKEN']  
client_secret = os.environ['TWITCH_CLIENT_SECRET']
TWITCH_SECRET = os.environ['Webhook_Secret']
streamer_name = 'laevus'
oAuth_Token = ""


client = discord.Client()

def test(data):
  return data
  # 839092761584074832

async def send_message(data):
  channel = client.get_channel(839092761584074832)
  await channel.send('hello' + data)

# doesnt work for some reason
def is_user_live():
    endpoint = 'https://api.twitch.tv/helix/streams'
    my_headers = {
        'Client-ID': CID,
        'Authorization': f'Bearer {OATH_TOKEN}'
    }
    my_params = {'user_login': streamer_name}
    response = requests.get(endpoint, headers=my_headers, params=my_params)
    data = response.json()
    print(data)
    if len(data) == 0:
        return False

# channel:read:redemptions
#gets access token from cid and csecret
def get_token():
  url = "https://id.twitch.tv/oauth2/token"
  data = {
  'client_id': CID,
  'client_secret': client_secret,
  'grant_type': "client_credentials"
  }

  request = requests.post(url, data)

  json_data = json.loads(request.text)
  access_token = str(json_data["access_token"])
  #print('token: ' + access_token)
  return access_token

def allow():
  url = 'https://id.twitch.tv/oauth2/authorize'
  my_params = {
    "client_id": CID,
    "redirect_uri": "https://Laevus-Bot.kylestrout.repl.co",
    "response_type": "code",
    "scope": "channel:read:redemptions"
  }

  response = requests.get(url, params=my_params)
  print(response)

  my_params2 = {
    'broadcaster_id': '164713504'
  }
  response2 = requests.get('https://api.twitch.tv/helix/subscriptions', params=my_params2)
  print(response2)
  #data = response.json()
  #print(data)
  return response

def create_subscription(token):

  url = "https://api.twitch.tv/helix/eventsub/subscriptions"
  my_headers = {
    'Client-ID': CID,
    'Authorization': "Bearer " + token,
    'Content-Type': 'application/json'
  }


  data = {
    "type": "channel.channel_points_custom_reward_redemption.add",
    "version": "1",
    "condition": {
        "broadcaster_user_id": "164713504"
    },
    "transport": {
        "method": "webhook",
        "callback": "https://Laevus-Bot.kylestrout.repl.co/redeem/callback",
        "secret": TWITCH_SECRET
    }
  }
  #print(data)
  response = requests.post(url, json=data, headers=my_headers)
  print(response)
  #print(json.loads(response.text))
  #print(response.status_code)

  # 

  #def list_subscriptions():


# gets a random quote
def getQuote():
  response = requests.get('https://zenquotes.io/api/random')
  json_data = json.loads(response.text)
  print(json_data)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return quote

# gets random trivia data question
def getTrivia():
  url = "https://numbersapi.p.rapidapi.com/random/trivia"
  querystring = {"json":"true",
  "fragment":"true",
  "max":"20",
  "min":"10"}

  headers = {
    'x-rapidapi-key': "0acac537f2msh6f343358ba73dd4p125502jsn473a06834b54",
    'x-rapidapi-host': "numbersapi.p.rapidapi.com"
  }

  response = requests.request("GET", url, headers=headers, params=querystring)
  json_data = json.loads(response.text)
  updateTrivia(json_data)
  
# adds trivia data to db
def updateTrivia(trivia_data):
  # if it already exists, updates it
  if "trivia" in db.keys():
    deleteTrivia()
    db["trivia"] = trivia_data

    # else, creates new entry in db
  else:
    db["trivia"] = trivia_data

def deleteTrivia():
  del db["trivia"]

def getTriviaDate():
  url = "https://numbersapi.p.rapidapi.com/6/21/date"
  querystring = {"json":"true","fragment":"true"}

  headers = {
    'x-rapidapi-key': "0acac537f2msh6f343358ba73dd4p125502jsn473a06834b54",
    'x-rapidapi-host': "numbersapi.p.rapidapi.com"
  }

  response = requests.request("GET", url, headers=headers, params=querystring)
  json_data = json.loads(response.text)
  updateTriviaDate(json_data)

def updateTriviaDate(triviaDate):
  if "triviaDate" in db.keys():
    deleteTriviaDate()
    db["triviaDate"] = triviaDate

    # else, creates new entry in db
  else:
    db["triviaDate"] = triviaDate

def deleteTriviaDate():
  del db["triviaDate"]

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  channel = client.get_channel(839092761584074832)
  await channel.send('Hello')
  


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
    userNum = random.randrange(0, 100)
    botNum = random.randrange(0, 100)
    y = message.author.name

    await message.channel.send('\n' + y + ' rolled a ' + str(userNum) + '! ' + 'LaevusBot rolled a ' + str(botNum) + '!')

    if userNum > botNum:
      await message.add_reaction("LaevusPog:806694928092495913")
      await message.channel.send('Congratulations!')
    else:
      await message.channel.send('Sorry!')

  if message.content.startswith('$stream'):
    is_user_live()
      
  if message.content.startswith('$trivia random'):
    getTrivia()
    await message.channel.send(db["trivia"]['text'])

  if message.content.startswith('$answer'):
    msg = message.content
    userAnswer = int(msg.split("$answer", 1)[1])
    answer = db["trivia"]['number']

    if userAnswer == answer:
      await message.add_reaction("5Head:784646128209494016")

    else:
      await message.add_reaction("Pepega:784646222577139732")
        
  if message.content.startswith('$trivia dates'):
    getTriviaDate()
    await message.channel.send(db["triviaDate"]['text'])

  if message.content.startswith('$date'):
    msg = message.content
    userAnswer = int(msg.split("$date", 1)[1])
    answer = db["triviaDate"]['year']

    if userAnswer == answer:
      await message.add_reaction("5Head:784646128209494016")

    else:
      await message.add_reaction("Pepega:784646222577139732")

  if message.content.startswith('$help') or message.content.startswith('$commands'):
    await message.channel.send("Commands: \n roll dice: $roll \n random trivia: $trivia random \n answer with: $answer [answer] \n date trivia: $trivia dates \n answer with: $date [answer] \n quote: $quote")
  
  if message.content.startswith('$test'):
    await test()
    #allow()
    #token = get_token()
    #create_subscription(token)

    

    

keep_alive()
client.run(my_secret)  
