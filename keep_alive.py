from flask import Flask
from threading import Thread
from flask import request
import os
import hmac
import hashlib
import requests
import binascii
import requests
#from main import send_message

app = Flask('')

@app.route('/')
def home():
    return "Hello. I am alive!"

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

@app.route('/webhooks/callback', methods=['POST'])
def process_twitch():
  is_valid = verify_signature(request)

  if (not is_valid):
    response = app.response_class(
          response="",
          status=403,
          mimetype='application/json'
      )
    return response
  if (is_valid):
    #print('valid')
    #print(request.get_json())
    data = request.get_json()['event']['user_name']
    #print(data)
    #get challenge and send response back to twitch
    return data
    #validate, if invalid return error, if valid, pass to discord bot and return ok
    #import from main.py import test
    #call test function and pass whatever it needs
    # my id 164713504
  

@app.route('/follower/callback', methods=['POST'])
def process_new_follower():
  print('new follower ===')
  is_valid = verify_signature(request)

  if (not is_valid):
    response = app.response_class(
          response="",
          status=403,
          mimetype='application/json'
      )
    return response
  if (is_valid):
    print('valid')
    data = request.get_json()['event']['user_name']
    print(request.get_json()['subscription']['condition'])
    print(data)
    #send_message(data)
    return data

@app.route('/online/callback', methods=['POST'])
def process_going_live():
  print('went live ===')
  is_valid = verify_signature(request)

  if (not is_valid):
    response = app.response_class(
          response="",
          status=403,
          mimetype='application/json'
      )
    return response
  if (is_valid):
    print('valid')
    data = request.get_json()['event']['broadcaster_user_name']
    print(data)
    return data

@app.route('/redeem/callback', methods=['POST'])
def process_new_subscriber():
  print('redeemed ===')
  is_valid = verify_signature(request)

  if (not is_valid):
    response = app.response_class(
          response="",
          status=403,
          mimetype='application/json'
      )
    return response
  if (is_valid):
    print('valid')
    data = request.get_json()['challenge']
    print(data)
    return data


# verify sha signature
# return challenge
def verify_signature(request):
  #print(body)
  message_id = request.headers['Twitch-Eventsub-Message-Id']
  message_timestamp = request.headers['Twitch-Eventsub-Message-Timestamp']
  body = request.get_data(True, True, False)
  message_signature = request.headers['Twitch-Eventsub-Message-Signature']

  hmac_message = message_id + message_timestamp + body
  secret = os.environ['Webhook_Secret']
  key = bytes(secret, 'utf-8')
  
  #key = secret.encode()
  data = bytes(hmac_message, 'utf-8')
  #data = hmac_message.encode()
  signature = hmac.new(key, data, hashlib.sha256)
  expected_signature_header = 'sha256=' + signature.hexdigest()

  if  message_signature != expected_signature_header:
    return False
  return True


  
  #hmac = header

    # only accept post requests
    # set up so it only responds to twitch
