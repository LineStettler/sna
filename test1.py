import tweepy

def get_twitter_api():
    consumer_key = '1KUtpMdGPAJl8oBJQJZgIJ0tr'
    consumer_secret = 'w3qaL8WISHnYoEoj62BDCmixBrroDJc5a5944759asaB4rV5lf'
    access_token = '937332677908279296-j0Ftw0wgcalvtqIiU2jliyfXBdvQbW2'
    access_token_secret = 'T7XVi7RsHjPXK7RlVdD1PgY0W0CuhOJ3i9bcs9AyO3qSo'
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)

api = get_twitter_api()

csv = open(twitter_1.csv, "w")

for tweet in tweepy.Cursor(api.search,
                           q="nobillag",
                           count=100,
                           result_type="recent",
                           include_entities=True,
                           lang="de").items():
    row = tweet.created_at + "," + tweet.text + "," + tweet.
    print tweet.created_at, tweet.text


