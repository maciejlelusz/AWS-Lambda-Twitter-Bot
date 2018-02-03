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
	track += '%20kubernetes%20OR'
	track += '%20datacenter%20OR'
	track += '%20sdn'
	track += '%20exclude%3Aretweets'
	track += '%20exclude%3Areplies'
	track += '%20include%3Alinks'
	track += '%20min_retweets%3A5'
	track += '%20min_faves%3A5'
	track += '%20lang%3Aen'
  
	result = api.GetSearch(raw_query=track)
  
	return result

def retweet(tweets):
	if not tweets:
		return False

	to_retweet = max(tweets, key=lambda status: status.favorite_count + status.retweet_count)

	api.PostRetweet(to_retweet.id)

def user_is_followable(user):
	return not user.following and not user.protected

def follow_followers():
	(_, _, recent_followers) = api.GetFollowersPaged()
	followable_followers = list(filter(user_is_followable, recent_followers))
	max_num_to_follow = 2
	for follower in followable_followers[0:max_num_to_follow]:
		api.CreateFriendship(follower.id)

def follow_someone(tweets):
	users = list(map(lambda t: t.user, tweets))
	followable_users = list(filter(user_is_followable, users))
	if not followable_users:
		return False
	user_to_follow = random.choice(followable_users)
	api.CreateFriendship(user_to_follow.id)

def lambda_handler(_event_json, _context):
	tweets = get_tweets()
	retweet(tweets)
	follow_someone(tweets)
	follow_followers()
