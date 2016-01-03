import http.client, urllib.parse
import json
import base64
from pprint import pprint

TWITTER_KEY = 'AwDyvqBDop7ewtGjwXucUeR1v:'
TWITTER_SECRET = 'ifMtW6zueJ4vhHEFJeAsbxyIyUGEvJoVz0W5jYpjDCq3ZBfEON'
TWITTER_HOST = 'api.twitter.com'

access_token = 'AAAAAAAAAAAAAAAAAAAAAOVDhgAAAAAAPbsN4bp9ukjbEdSj2emNbT7lPhw%3D17tNoTGJHuSJYN8Kj8d8buao7SK95vnmKCkPw3d7CJzXNLMimG'
encoding = 'utf-8'


def OAuth( ):
	global access_token
	encoded_auth = TWITTER_KEY.encode(encoding)+TWITTER_SECRET.encode(encoding)
	base_auth = base64.b64encode(encoded_auth)
	request_body = 'grant_type=client_credentials'.encode(encoding)

	header = {'Authorization': 'Basic '+base_auth.decode('ascii'), 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}
	connection.request('POST', '/oauth2/token', request_body, headers=header)
	response = connection.getresponse()
	if(response.status == 200):
		data = json.loads(response.read().decode(encoding))
		token = data['access_token']
		access_token = token
	else:
		raise Exception



def getQueryTweets( query_term ):
	connection = http.client.HTTPSConnection( TWITTER_HOST )
	header = {'Authorization': 'Bearer %s' %access_token}
	query = {'q': query_term, 'lang': 'en', 'count': 10, 'result_type': 'mixed'}
	connection.request('GET', '/1.1/search/tweets.json?'+urllib.parse.urlencode(query), headers=header)

	response = connection.getresponse()

	tweets_dict = json.loads(response.read().decode(encoding))
	some_dict = filterTweets(tweets_dict)
	# response_dict = {'twitter': some_dict}
	# json_response = json.dumps(response_dict)
	return some_dict

def filterTweets(tweets_dict):
	# filtered_dict = {'tweets': tweet_list}
	if 'statuses' in tweets_dict:
		tweet_list = []
		for status in tweets_dict['statuses']:
			temp = {}
			temp['tweet_text'] = status['text']
			temp['retweet_count'] = status['retweet_count'] 
			tweet_list.append(temp)
	else:
		pass
	return tweet_list




# print(access_token)
# pprint(getQueryTweets('trump'))