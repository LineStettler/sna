import tweepy
import sys  # import sys package, if not already imported
import json
#reload(sys)
#sys.setdefaultencoding('utf-8')

def get_twitter_api():
    consumer_key = '1KUtpMdGPAJl8oBJQJZgIJ0tr'
    consumer_secret = 'w3qaL8WISHnYoEoj62BDCmixBrroDJc5a5944759asaB4rV5lf'
    access_token = '937332677908279296-j0Ftw0wgcalvtqIiU2jliyfXBdvQbW2'
    access_token_secret = 'T7XVi7RsHjPXK7RlVdD1PgY0W0CuhOJ3i9bcs9AyO3qSo'
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)

def mentiened_users_to_string(users):
    str = ""
    print len(users)
    print users
    if len(users) >= 0:
        for user in users:
            str += user["id_str"] + " "
            str += user["screen_name"]+ " "
            str += user["name"]+ " "
            str += "-"
    print type(str)
    return str.encode('utf-8')

api = get_twitter_api()

csv = open("twitter_1.csv", "wb")
c =0
for tweet in tweepy.Cursor(api.search,
                           q="nobillag",
                           count=100,
                           result_type="recent",
                           include_entities=True,
                           lang="de").items():
    dic_entities = tweet.entities
    mentiened_users = mentiened_users_to_string(dic_entities["user_mentions"])
    print mentiened_users
    #m = json.dumps(dic_entities["user_mentions"])
    row = (tweet.created_at).strftime("%Y-%m-%d %H:%M") + "," +  \
    str(tweet.id) + "," + \
    tweet.text + "," + \
    tweet.user.name + "," + \
    tweet.user.screen_name + "," + \
    str(tweet.user.friends_count) + "," + \
    str(tweet.user.followers_count) + "," + \
    str(tweet.user.favourites_count) + "," + \
    tweet.user.location + "," + \
    str(tweet.retweet_count) + "," + \
    tweet.user.description + "," + \
    str(tweet.user.statuses_count) + "," + \
    str(tweet.in_reply_to_status_id) + "," + \
    tweet.in_reply_to_screen_name + "," + \
    mentiened_users + "\n"
    #str(m) + "\n"
    
    c += 1
    print c
    row_utf = row.encode('utf-8')
    csv.write(row_utf)








