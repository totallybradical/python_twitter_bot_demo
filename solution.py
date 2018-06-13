# Import tweepy for working with twitter
import tweepy
# Import the keys dictionary from our keys.py file
from keys import keys
# Import random for our random location selector
import random
# Import json to handle streaming API
import json

# Pull in each value from our keys.py
CONSUMER_KEY = keys['consumer_key']
CONSUMER_SECRET = keys['consumer_secret']
ACCESS_TOKEN = keys['access_token']
ACCESS_TOKEN_SECRET = keys['access_token_secret']
OWNER_ID = keys['owner_id']

# Create global auth and api objects
AUTH = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
AUTH.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
API = tweepy.API(AUTH)

# List of specific strings we want to check for in Tweets
REPLY_TO_THESE = [
    'where we landin',
    'where we droppin',
    'where we goin'
]

# Fortnite locations
LOCATIONS = [
    'Junk Junction',
    'Haunted Hills',
    'Anarchy Acres',
    'Risky Reels',
    'Pleasant Park',
    'Loot Lake',
    'Tomato Town',
    'Wailing Woods',
    'Snobby Shores',
    'Tilted Towers',
    'Dusty Divot',
    'Retail Row',
    'Lonely Lodge',
    'Greasy Grove',
    'Shifty Shafts',
    'Salty Springs',
    'Fatal Fields',
    'Moisty Mire',
    'Flush Factory',
    'Lucky Landing'
]

# Class that inherits from StreamListener
class MyTwitterStream(tweepy.StreamListener):
    # Override on_status to do what we want
    def on_status(self, status):
        # Short circuit if None
        if not status:
            return
        # Make sure the string can be decoded
        try:
            print(status)
            tweet_info = status._json
            print(tweet_info)
        except ValueError:
            return
        # Get the user id mentioned in the tweet and compare with account’s id
        tweeter_id = tweet_info["user"]["id_str"]
        from_self = (tweeter_id == OWNER_ID)
        # We only care about other’s tweets
        if from_self:
            print("You tweeted yourself.")
            return
        tweet_id = tweet_info["id_str"]
        tweeter_screen_name = tweet_info["user"]["screen_name"]
        tweet_text = tweet_info["text"]
        # Choose any chatbot or function here to add your response.
        if any(option in tweet_text.lower() for option in REPLY_TO_THESE):
            location = random.choice(LOCATIONS)
            reply_text = "@" + tweeter_screen_name + " " + location
            # Check if repsonse is over 140 char
            if len(reply_text) > 140:
                reply_text = reply_text[0:139] + "."
            print("Tweet ID: " + tweet_id)
            print("From: " + tweeter_screen_name)
            print("Tweet Text: " + tweet_text)
            print("Reply Text: " + reply_text)
            API.update_status(status=reply_text, in_reply_to_status_id=tweet_id)
    def on_error(self, status):
        print(status)

# MAIN CODE
if __name__ == "__main__":
    # Create an instance of MyTwitterStream (listener object)
    myTwitterSteam = MyTwitterStream()
    twitterStream = tweepy.Stream(auth=AUTH, listener=myTwitterSteam)
    twitterStream.userstream(_with="user")
