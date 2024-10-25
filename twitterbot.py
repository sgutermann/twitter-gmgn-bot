import tweepy
import os
import random
import sys
import time
import requests
from dotenv import load_dotenv
from subprocess import Popen, PIPE
from datetime import datetime
import pytz  # Time zone support

# Load environment variables from '/var/opt/twitterbot/twitterbot.env'
load_dotenv('/var/opt/twitterbot/twitterbot.env')

# Set the path for the log file
log_file_path = "/var/opt/twitterbot/twitterbot.log"

# Function to log messages to both the console and the log file
def log_message(message):
    with open(log_file_path, "a") as log_file:
        log_file.write(f"{datetime.now()}: {message}\n")
    print(message)

# Load API keys and access tokens from environment variables
api_key = os.getenv("API_KEY")
api_secret_key = os.getenv("API_KEY_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")
weather_api_key = os.getenv("WEATHER_API_KEY")

# Script parameters
post_type = sys.argv[1].upper()  # First parameter: GM or GN
image_folder = sys.argv[2]  # Second parameter: Image folder or "none"
location = sys.argv[3] if sys.argv[3].lower() != "none" else None  # Third parameter: City for weather or "none"
extra_hashtags = sys.argv[4] if len(sys.argv) > 4 else ""  # Fourth parameter: Additional hashtags

# OAuth1 Authentication for media upload (API v1.1)
auth = tweepy.OAuth1UserHandler(api_key, api_secret_key, access_token, access_token_secret)
api = tweepy.API(auth)

# OAuth2 Authentication for posting tweets (API v2)
client = tweepy.Client(
    consumer_key=api_key,
    consumer_secret=api_secret_key,
    access_token=access_token,
    access_token_secret=access_token_secret
)

log_message("Twitter client authenticated successfully!")

# Function to choose a random image from a specified folder
def choose_random_image(folder_path):
    if folder_path.lower() == "none":
        log_message("Image option set to none.")
        return None
    log_message("Choosing a random image from folder: " + folder_path)
    images = [os.path.join(folder_path, img) for img in os.listdir(folder_path) if img.endswith(('.png', '.jpg', '.jpeg', '.webp'))]
    if images:
        chosen_image = random.choice(images)
        log_message("Chosen image: " + chosen_image)
        return chosen_image
    else:
        log_message("No images found in folder.")
        return None

# Function to retrieve weather information if a location is provided
def get_weather(location):
    if not location:
        log_message("No location provided for weather; skipping weather info.")
        return ""
    log_message(f"Fetching weather information for {location}...")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={weather_api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        description = data['weather'][0]['description']
        weather_info = f"The weather here is currently {temp}°C with {description}."
        log_message("Weather info fetched: " + weather_info)
        return weather_info
    else:
        log_message(f"Failed to fetch weather information: {response.status_code}")
        return ""

# Function to generate text using LLaMA model
def generate_text(prompt):
    log_message(f"Generating text with LLaMA for prompt: {prompt}")
    try:
        process = Popen(["ollama", "run", "llama3.2:1b"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate(input=prompt.encode(), timeout=60)
        if stderr:
            log_message(f"Error in LLaMA process: {stderr.decode().strip()}")
        generated_text = stdout.decode().strip()
        return generated_text if generated_text else "Good night, world!"
    except Exception as e:
        log_message(f"Error during text generation with LLaMA: {e}")
        return "Good night, world!"
    finally:
        process.terminate()

# Function for a random delay to vary post timing
def random_delay(max_delay=1800):
    delay = random.randint(0, max_delay)
    log_message(f"Waiting for a random delay of {delay} seconds...")
    time.sleep(delay)

# Consolidated function to handle both GM and GN posts with optional image, weather, and hashtags
def post_with_details(post_type, image_folder, weather_info, extra_hashtags):
    # Choose an image if folder is provided
    image_path = choose_random_image(image_folder)
    
    # Generate the prompt based on post type
    if post_type.lower() == "gm":
        prompt = f"Please generate a single casual good morning message with positivity, including the weather info: {weather_info}, no longer than 280 characters."
    else:
        prompt = f"Please generate a single good night message with a casual tone and mention memecoins. Keep it positive and casual, no longer than 280 characters."
    
    # Generate text with LLaMA
    post_text = generate_text(prompt).strip('"() ') + " " + extra_hashtags

    # Attempt to post with or without image
    try:
        if image_path:
            log_message(f"Uploading image and posting {post_type} tweet...")
            media = api.media_upload(image_path)
            response = client.create_tweet(text=post_text, media_ids=[media.media_id])
        else:
            log_message(f"Posting {post_type} tweet without image...")
            response = client.create_tweet(text=post_text)
        log_message(f"{post_type.capitalize()} Tweet successfully posted with ID: {response.data['id']}")
    except tweepy.errors.TweepyException as e:
        log_message(f"Error occurred while posting {post_type} tweet: {e}")

# Main program: determines whether to post GM or GN based on the parameters
def main():
    random_delay()
    weather_info = get_weather(location) if location else ""

    if post_type == "GM":
        post_with_details("Good morning", image_folder, weather_info, extra_hashtags)
    elif post_type == "GN":
        post_with_details("Good night", image_folder, weather_info, extra_hashtags)
    else:
        log_message("Invalid post type specified. Use 'GM' or 'GN'.")

# Start the main program
if __name__ == "__main__":
    main()
