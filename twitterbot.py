import twitter
import json
import urllib

with open('credentials.json') as file:
	credentials = json.loads(file.read())

api = twitter.Api(**credentials)

def get_tweets(filter):
 
	query = "q=" + filter

	result = api.GetSearch(raw_query=query)
  
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
	max_num_to_follow = 5
	for follower in followable_followers[0:max_num_to_follow]:
		api.CreateFriendship(follower.id)

def follow_someone(tweets):
	users = list(map(lambda t: t.user, tweets))
	followable_users = list(filter(user_is_followable, users))
	if not followable_users:
		return False
	user_to_follow = random.choice(followable_users)
	api.CreateFriendship(user_to_follow.id)

def filter_prep(void):
	
	t_keywords = void
        t_exclude = [ "exclude:retweets", "exclude:replies" ]
        t_include = [ "include:links" ]
        t_options = [ "min_retweets:5", "min_faves:5", "lang:en" ]

        filter_keywords = " OR " .join(t_keywords)
        filter_exclude = " " .join(t_exclude)
        filter_include = " " .join(t_include)
        filter_options = " " .join(t_options)

        filter = urllib.quote(filter_keywords + " " + filter_exclude + " " + filter_include + " " + filter_options)

        return filter

def lambda_handler(_event_json, _context):

	keywords = [ "AWS", "Microsoft Azure", "MS Azure",  "VMware", "GCE", "Containers", "Docker", "Kubernetes", "Datacenter", "SDN" ]
	
	filter = filter_prep(keywords)

	tweets = get_tweets(filter)
	retweet(tweets)
	follow_someone(tweets)
	follow_followers()
