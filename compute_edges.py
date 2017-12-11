import csv




writer = csv.writer(open("twitter_031217_gephi.csv", "wb"))
header = ['Tweeter_name','in_reply_to_name','in_reply_to_statusID','tweet_ID','text','isRetweet']

writer.writerow(header)

def find_between(s,first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


def UnicodeDictReader(utf8_data, **kwargs):
    csv_reader = csv.DictReader(utf8_data, **kwargs)
    for row in csv_reader:
        yield {unicode(key, 'utf-8'):unicode(value, 'utf-8') for key, value in row.iteritems()}

#udr = UnicodeDictReader('twitter2.csv', 'rb')

with open('twitter2.csv', 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if str(row['in_replay_to_name']).find("None") == -1:
            outputRow = row['name'] + "," + row['in_replay_to_name'] + "," + row['in_replay_to'] + "," +row['id'] + "," +row['text'] + "," + "false"
            writer.writerow(outputRow)
            print(outputRow)
        elif str(row['text']).find("RT ") != -1:
            retweet_origin_user = find_between(row['text'], ' RT ', ':')
            outputRow = row['name'] + "," + retweet_origin_user + "," + row['in_replay_to'] + "," +row['id'] + "," +row['text'] + "," + "true"
            writer.writerow(outputRow)
            print(outputRow)




