import tweepy
import json

from tweepy import OAuthHandler


def get_twitter_api():
    consumer_key = '1KUtpMdGPAJl8oBJQJZgIJ0tr'
    consumer_secret = 'w3qaL8WISHnYoEoj62BDCmixBrroDJc5a5944759asaB4rV5lf'
    access_token = '937332677908279296-j0Ftw0wgcalvtqIiU2jliyfXBdvQbW2'
    access_token_secret = 'T7XVi7RsHjPXK7RlVdD1PgY0W0CuhOJ3i9bcs9AyO3qSo'
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    return tweepy.API(auth)
    # return tweepy.API(auth, parser=tweepy.parsers.JSONParser())


api = get_twitter_api()

resultList = []
counter = 0

c = tweepy.Cursor(api.search,
                  q="nobillag",
                  count=100,
                  result_type="recent",
                  include_entities=True,
                  lang="de").items()

while True:
    try:
        tweet = c.next()
        counter += 1
        resultList.append(tweet._json)
        # Insert into db
    except tweepy.TweepError:
        # falls API Limit erreicht, schreibe noch alles in das File.
        with open('nobillag_031217_new.txt', 'w') as outfile:
            json.dump(resultList, outfile)
        continue
    except StopIteration:
        break

with open('nobillag_031217_new.txt', 'w') as outfile:
    json.dump(resultList, outfile)

print(counter)


'''for tweet in tweepy.Cursor(api.search,
                       q="nobillag",
                       count=100,
                       result_type="recent",
                       include_entities=True,
                       lang="de").items():
print tweet.created_at, tweet.text
resultList.append(tweet._json)'''
