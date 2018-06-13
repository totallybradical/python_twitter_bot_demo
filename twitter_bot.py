# Twitter Bot
import tweepy
# Import the keys from our keys file
from keys import keys
# import random
import random
import json

# pull in each value from our keys file
CONSUMER_KEY = keys['consumer_key']
CONSUMER_SECRET = keys['consumer_secret']
ACCESS_TOKEN = keys['access_token']
ACCESS_TOKEN_SECRET = keys['access_token_secret']
OWNER_ID = keys['owner_id']

# Create global auth and api object
AUTH = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
AUTH.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
API = tweepy.API(AUTH)

LOCATIONS = [
    'Haunted Hills',
    'Tilted Towers',
    'Dusty Divot',
    'Moisty Mire',
    'Lucky Landing',
    'Anarchy Acres'
]

# Class that inherits from StreamListener
class MyTwitterStream(tweepy.StreamListener):
    # Override on_status to do what we want
    def on_status(self, status):
        # Short circuit if None
        if not status:
            return
        # Get the tweet info
        tweet_info = status._json
        # print(status)
        tweeter_id = tweet_info["user"]["id_str"]
        from_self = (tweeter_id == OWNER_ID)
        if from_self:
            print("You tweeted yoself")
            return
        tweet_id = tweet_info["id_str"]
        tweeter_screen_name = tweet_info["user"]["screen_name"]
        tweet_text = tweet_info["text"]
        # Check the text and do something
        if "where we landin" in tweet_text.lower():
            location = random.choice(LOCATIONS)
            reply_text = "@" + tweeter_screen_name + " " + location
            print(reply_text)
            API.update_status(status=reply_text, in_reply_to_status=tweet_id)

if __name__ == "__main__":
    # Create an instance of a twitter stream
    myTwitterStream = MyTwitterStream()
    twitterStream = tweepy.Stream(auth=AUTH, listener=myTwitterStream)
    twitterStream.userstream(_with="user")
