import tweepy
import json
import time
import csv


def find_between(s,first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""

def get_twitter_api():
    consumer_key = '1KUtpMdGPAJl8oBJQJZgIJ0tr'
    consumer_secret = 'w3qaL8WISHnYoEoj62BDCmixBrroDJc5a5944759asaB4rV5lf'
    access_token = '937332677908279296-j0Ftw0wgcalvtqIiU2jliyfXBdvQbW2'
    access_token_secret = 'T7XVi7RsHjPXK7RlVdD1PgY0W0CuhOJ3i9bcs9AyO3qSo'
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    return tweepy.API(auth)

def mentioned_users_to_string(users):
    str = " "
    if len(users) >= 0:
        for user in users:
            str += user["id_str"] + " "
            str += user["screen_name"]+ " "
            str += user["name"]
            str += "-"
    return str.encode("utf-8")

def get_location(location):
    if location == None:
        return "None"
    else:
        return location.encode("utf-8")

def get_description(description):
    if description == None:
        return "None"
    else:
        return description.encode("utf-8")

def get_in_reply_to_screen_name(name):
    if name == None:
        return "None"
    else:
        return name.encode("utf-8")

def get_crated_at(date):
    if date == None:
        return "None"
    else:
        return date.strftime("%Y-%m-%d %H:%M")

def write_tweet_to_csv(tweet):
    dic_entities = tweet.entities
    mentioned_users = mentioned_users_to_string(dic_entities["user_mentions"])

    row = [get_crated_at(tweet.created_at) , str(tweet.id) , \
           tweet.text.replace(',',' ',1).replace('\n', ' ', 1).replace('\r', ' ', 1).encode("utf-8"), \
           tweet.user.name.encode("utf-8").replace(',',' ',1).replace('\n', ' ', 1).replace('\r', ' ', 1), \
           tweet.user.screen_name.encode("utf-8").replace(',',' ',1).replace('\n', ' ', 1).replace('\r', ' ', 1), \
           str(tweet.user.friends_count) , \
           str(tweet.user.followers_count) , \
           str(tweet.user.favourites_count) , \
           get_location(tweet.user.location).replace(',',' ',1).replace('\n', ' ', 1).replace('\r', ' ', 1) , \
           str(tweet.retweet_count) , \
           get_description(tweet.user.description).replace(',',' ',1).replace('\n', ' ', 1).replace('\r', ' ', 1), \
           str(tweet.user.statuses_count) , \
           str(tweet.in_reply_to_status_id) , \
           get_in_reply_to_screen_name(tweet.in_reply_to_screen_name).replace(',', ' ', 1).replace('\n', ' ', 1).replace('\r', ' ', 1) , \
           mentioned_users.replace(',',' ',1).replace('\n', ' ', 1).replace('\r', ' ', 1), \
           str(tweet.retweeted)]
    writer.writerow(row)

def write_filteredTweet_to_csv(tweet, isRetweet):

    dic_entities = tweet.entities
    mentioned_users = mentioned_users_to_string(dic_entities["user_mentions"])
    if isRetweet:
        retweet_origin_user = find_between(tweet.text.encode("utf-8"), 'RT ', ':')
        row1 = [tweet.user.name.encode("utf-8").replace(',',' ',1).replace('\n', ' ', 1).replace('\r', ' ', 1), \
               retweet_origin_user.replace(',', ' ', 1).replace('\n', ' ', 1).replace('\r', ' ', 1), \
               str(tweet.in_reply_to_status_id), \
               str(tweet.id), \
               tweet.text.replace(',', ' ', 1).replace('\n', ' ', 1).replace('\r', ' ', 1).encode("utf-8"), \
               str('True'), \
               str(tweet.retweet_count), \
               str(tweet.user.followers_count), \
               str(tweet.user.friends_count), \
               mentioned_users.replace(',', ' ', 1).replace('\n', ' ', 1).replace('\r', ' ', 1)]
        writer_filtered.writerow(row1)
    else:

        row2 = [tweet.user.name.encode("utf-8").replace(',', ' ', 1).replace('\n', ' ', 1).replace('\r', ' ', 1), \
               get_in_reply_to_screen_name(tweet.in_reply_to_screen_name).replace(',', ' ', 1).replace('\n', ' ', 1).replace('\r', ' ', 1), \
               str(tweet.in_reply_to_status_id), \
               str(tweet.id), \
               tweet.text.replace(',', ' ', 1).replace('\n', ' ', 1).replace('\r', ' ', 1).encode("utf-8"), \
               str(tweet.retweeted), \
               str(tweet.retweet_count), \
               str(tweet.user.followers_count), \
               str(tweet.user.friends_count), \
               mentioned_users.replace(',', ' ', 1).replace('\n', ' ', 1).replace('\r', ' ', 1)]
        writer_filtered.writerow(row2)
# main

api = get_twitter_api()

writer = csv.writer(open("twitter2_101217.csv", "wb"))
header = ['created', 'id', 'text', 'name', 'screen_name', 'friends', 'followers', \
'favorites', 'location', 'retweets', 'user_description', 'status_count','in_reply_to', 'in_reply_to_name', 'retweeted']
writer.writerow(header)
writer_filtered = csv.writer(open("twitter_101217_gephi_filtered.csv", "wb"))
header_filtered = ['Source','Target','in_reply_to_statusID','tweet_ID','text','isRetweet', 'retweet_count','followers_count','friends_count','mentioned_users']

writer_filtered.writerow(header_filtered)



resultList = []
counter = 0

c =  tweepy.Cursor(api.search,
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
        write_tweet_to_csv(tweet)
        if str(tweet.text.encode('UTF-8')).find('RT ') != -1:
            write_filteredTweet_to_csv(tweet, True)
        elif get_in_reply_to_screen_name(tweet.in_reply_to_screen_name).find("None") == -1:
            write_filteredTweet_to_csv(tweet, False)


        # Insert into db
    except tweepy.TweepError:
        # falls API Limit erreicht, schreibe noch alles in das File.
        with open('nobillag_json_101217.txt', 'w') as outfile:
            json.dump(resultList, outfile)
            time.sleep(15*60)
        continue
    except StopIteration:
        break

with open('nobillag_json_101217.txt', 'w') as outfile:
    json.dump(resultList, outfile)


print(counter)
