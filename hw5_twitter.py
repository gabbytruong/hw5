from requests_oauthlib import OAuth1
import json
import sys
import requests
import secret_data # file that contains OAuth credentials
import nltk # uncomment line after you install nltk

## SI 206 - HW
## COMMENT WITH:
## Your section day/time: Tuesday, 5:30-7
## Any names of people you worked with on this assignment: Willem Lucas

#usage should be python3 hw5_twitter.py <username> <num_tweets>
username = sys.argv[1]
num_tweets = sys.argv[2]

consumer_key = secret_data.CONSUMER_KEY
consumer_secret = secret_data.CONSUMER_SECRET
access_token = secret_data.ACCESS_KEY
access_secret = secret_data.ACCESS_SECRET

#Code for OAuth starts
url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)
requests.get(url, auth=auth)
#Code for OAuth ends

#Write your code below:
baseurl = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
params = {'screen_name': username, 'count': num_tweets}
response = requests.get(baseurl, params, auth=auth)
tweet_data = json.loads(response.text)
tweet_file = open('tweet.json', 'w')
tweet_file.write(json.dumps(tweet_data, indent = 2))
tweet_file.close()

def make_cache_request(baseurl, params):
    unique_id = unique_combo(baseurl,params)
    if unique_id in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_id]
    else:
        print("Making a request for new data...")
        resp = requests.get(baseurl, params, auth = auth)
        CACHE_DICTION[unique_id] = json.loads(resp.text)
        dumped_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_cache)
        fw.close()
        return CACHE_DICTION[unique_id]

def unique_combo(baseurl, params):
    empty_lst = []
    for key in params.keys():
        empty_lst.append("{}-{}".format(key, params[key]))
    return baseurl + "&".join(empty_lst)

def twitter_params(username, num_tweets):
    baseurl = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
    param_diction = {}
    param_diction['screen_name'] = username
    param_diction['count'] = num_tweets
    return make_cache_request(baseurl, params_diction)

all_tweets = ''
for tweet in tweet_data:
    all_tweets = all_tweets + ' ' + tweet['text']

    tokens = nltk.word_tokenize(all_tweets)
    freqDist = nltk.FreqDist(token for token in tokens if token.isalpha()
    and "http" not in token and "https" not in token and "RT" not in token)
    for word, frequency in freqDist.most_common(5):
        print(word + ' ' + str(frequency))


if __name__ == "__main__":
    if not consumer_key or not consumer_secret:
        print("You need to fill in client_key and client_secret in the secret_data.py file.")
        exit()
    if not access_token or not access_secret:
        print("You need to fill in this API's specific OAuth URLs in this file.")
        exit()
