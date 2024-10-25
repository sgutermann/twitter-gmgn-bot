import tweepy
import os
from dotenv import load_dotenv

# Lade die Umgebungsvariablen aus der .env-Datei
load_dotenv('/var/opt/twitterbot/twitterbot.env')

# API-Schlüssel aus den Umgebungsvariablen laden
api_key = os.getenv("API_KEY")
api_secret_key = os.getenv("API_KEY_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

# OAuth1-Authentifizierung
client = tweepy.Client(
    consumer_key=api_key,
    consumer_secret=api_secret_key,
    access_token=access_token,
    access_token_secret=access_token_secret
)

# Test-Tweet posten (API v2)
try:
    response = client.create_tweet(text="Hello world! Posting with API v2.")
    print(f"Tweet successfully posted with ID: {response.data['id']}")
except tweepy.errors.TweepyException as e:
    print(f"Error occurred: {e}")
