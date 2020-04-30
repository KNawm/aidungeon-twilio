import json
import os
import random

import requests
from dotenv import load_dotenv, find_dotenv
from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather

app = Flask(__name__)

# Initialize environment variables
load_dotenv(find_dotenv())
ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
AIDUNGEON_EMAIL = os.getenv('AIDUNGEON_EMAIL')
AIDUNGEON_PASS = os.getenv('AIDUNGEON_PASS')

# Initialize the Twilio client
client = Client(ACCOUNT_SID, AUTH_TOKEN)

# Get authorization header from AIDungeon
r = requests.post('https://api.aidungeon.io/users', data={'email': AIDUNGEON_EMAIL, 'password': AIDUNGEON_PASS})
response = json.loads(r.text)
auth_header = {'x-access-token': response['accessToken']}
adventure = None


@app.route('/answer', methods=['GET', 'POST'])
def answer_call():
    """Respond to incoming phone calls with a brief message."""
    global adventure

    # Start our TwiML response
    resp = VoiceResponse()

    resp.say(
        "You're about to enter a world of endless possibilities, where you can do absolutely anything you can imagine...", voice='Polly.Emma-Neural')

    resp.say(
        "The story will begin now, when you hear a male voice saying 'you', say something to do or say, good luck.", voice='Polly.Emma-Neural')

    # Generate a random story for the user
    adventure = new_story()
    story = random_story()

    # Once upon a time...
    resp.say(story)
    resp.redirect('/gather')

    return str(resp)


@app.route('/gather', methods=['GET', 'POST'])
def gather_response():
    """Gather the response of the user"""
    # Start our TwiML response and <Gather> verb
    resp = VoiceResponse()
    gather = Gather(input='speech', action='/process', timeout=3)
    gather.say('You', voice='Polly.Joey')
    resp.append(gather)

    # Keep talking if the user doens't say anything
    resp.redirect('/process')

    return str(resp)


@app.route('/process', methods=['GET', 'POST'])
def process_response():
    """Process the response of the user"""
    # Start our TwiML response
    resp = VoiceResponse()
    speech_result = request.values.get('SpeechResult')

    payload = {'input': speech_result}
    requests.post(f'https://api.aidungeon.io/user/adventure/{adventure}/action/progress', data=payload, headers=auth_header)

    # Get AI response
    response = json.loads(requests.get(f'https://api.aidungeon.io/user/adventure/{adventure}', headers=auth_header).text)
    output = response['history'][-1]['output']

    resp.say(output, voice='Polly.Amy-Neural')
    resp.redirect('/gather')

    return str(resp)


def new_story():
    # Create a new session
    response = json.loads(requests.post('https://api.aidungeon.io/user/adventure', headers=auth_header).text)
    adventure = response['id']

    return adventure


def random_story():
    with open('names.json') as f:
        file = json.load(f)

        # Choose random name
        name = random.choice(file['names'])

    with open('prompts.json') as f:
        file = json.load(f)

        # Choose random setting
        setting = random.choice(list(file['settings'].keys()))
        description = file['settings'][setting]['description']

        # Choose random character
        character = random.choice(list(file['settings'][setting]['characters'].keys()))
        prompt = file['settings'][setting]['characters'][character]['prompts'][0]
        item1 = file['settings'][setting]['characters'][character]['item1']
        item2 = file['settings'][setting]['characters'][character]['item2']

    return "You are " + name + ", a " + character + " " + description + "You have a " + item1 + " and a " + item2 + ". " + prompt


if __name__ == '__main__':
    app.run()
