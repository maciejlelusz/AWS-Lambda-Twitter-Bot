import twitter
import json
import random

with open('credentials.json') as file:
    credentials = json.loads(file.read())

api = twitter.Api(**credentials)

def get_tweets():
  track ='q=%23'
  track += 'cloud'
  track += '-filter%3'
  track += 'Alinks'
  track += '&lang=pl'
  track += '&count=50'
  
  result = api.GetSearch(raw_query=track)
  
  return result

def retweet(tweets):
    if not tweets:
        return False

    to_retweet = max(tweets, key=lambda status: status.favorite_count + status.retweet_count)
    
    api.PostRetweet(to_retweet.id)

def lambda_handler(_event_json, _context):
  tweets = get_tweets()
  retweet(tweets)
