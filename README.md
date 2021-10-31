<a href="https://www.twilio.com">
  <img src="https://static0.twilio.com/marketing/bundles/marketing/img/logos/wordmark-red.svg" alt="Twilio" width="250" />
</a>
 
# aidungeon-twilio
<a href="./LICENSE">
  <img src="https://img.shields.io/badge/license-MIT-green.svg?style=for-the-badge" title="License" />
</a>

## About

This project shows how to integrate a custom machine learning model with an API to build an AI-powered conversational bot that builds a story based on your input.


## Set up

### Requirements

- Python 3.4 or newer
- A Twilio account — [sign up](https://www.twilio.com/referral/CwlrIy)
- A Twilio phone number with Voice capabilities
- A AIDungeon account — [sign up](https://play.aidungeon.io)

### Local development

After the above requirements have been met:

1. Clone this repository and `cd` into it

```bash
git clone git@github.com:KNawm/aidungeon-twilio.git
cd aidungeon-twilio
```

2. Create a new virtual environment

```bash
python3 -m venv venv
venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Set your environment variables

```bash
cp .env.example .env
```

Open `.env` in your favorite text editor and configure the following values.

| Config Value  | Description |
| :-------------  |:------------- |
`TWILIO_ACCOUNT_SID` | Your primary Twilio account identifier - [find this in the console here](https://www.twilio.com/console).
`TWILIO_AUTH_TOKEN` | Used to authenticate - [you can get it at twilio.com/console](https://www.twilio.com/console).
`AIDUNGEON_EMAIL` | Your AIDungeon account email - [get a free account at play.aidungeon.io](https://play.aidungeon.io).
`AIDUNGEON_PASS` | Your AIDungeon account password - [just like the above, you'll get one here](https://play.aidungeon.io).

5. Run the application

```bash
flask run
```

Alternatively, you can use this command to start the server in development mode. It will reload whenever you change any files.

```bash
export FLASK_ENV=development
flask run
```

6. (optional) Run ngrok

If you are going to develop or test locally, Twilio won't be able to access localhost directly. You'll need to create a publicly accessible URL using a tool like ngrok to send HTTP/HTTPS traffic to a server running on your localhost.

```bash
./ngrok http 5000
```

7. Configure Twilio

Enter [here](https://www.twilio.com/console/phone-numbers/incoming) and configure your webhook.

That's it!

## Contributing

This project is open source and welcomes contributions.
