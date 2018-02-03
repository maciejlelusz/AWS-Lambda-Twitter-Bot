import twitter
import json
import random

with open('credentials.json') as file:
    credentials = json.loads(file.read())

api = twitter.Api(**credentials)

def get_tweets():
  track = 'q='
  track += '%20AWS%20OR'
  track += '%20Azure%20OR'
  track += '%20GCE%20OR'
  track += '%20containers%20OR'
  track += '%20docker%20OR'
  track += '%20datacenter%20OR'
  track += '%20sdn'
  track += '%20exclude%3Aretweets'
  track += '%20exclude%3Areplies'
  track += '%20include%3Alinks'
  track += '%20min_retweets%3A5'
  track += '%20min_faves%3A5'
  track += '%20+filter%3Aretweets'
  track += '%lang%3en'
  
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
