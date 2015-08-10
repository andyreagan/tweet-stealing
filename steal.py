# steal tweets
#
# usage: python steal.py andyreagan

from sys import argv
import datetime
from twython import Twython, TwythonError
import json

if __name__ == '__main__':

    # store the keys somewhere (so I can share this script)
    f = open('keys','r')
    APP_KEY = f.readline().rstrip()
    APP_SECRET = f.readline().rstrip()
    OAUTH_TOKEN = f.readline().rstrip()
    OAUTH_TOKEN_SECRET = f.readline().rstrip()
    f.close()

    # log in to twitter as that user (me)
    # twitter = Twython(APP_KEY,APP_SECRET,OAUTH_TOKEN,OAUTH_TOKEN_SECRET)

    # send a tweet
    # tweet='test at {0}'.format(datetime.datetime.now().strftime('%H-%M on %Y-%m-%d'))
    # twitter.update_status(status=tweet)

    # # log in to twitter and get an oauth 2 token
    # twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
    # ACCESS_TOKEN = twitter.obtain_access_token()
    # print(ACCESS_TOKEN)

    # log in as oauth 2
    # some endpoints have a higher rate limit
    # store the keys somewhere (so I can share this script)
    f = open('keys_oauth2','r')
    APP_KEY = f.readline().rstrip()
    ACCESS_TOKEN = f.readline().rstrip()
    f.close()
    twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)

    # # testing out some iteration
    # danforth = 301579658
    # reagan = 55931868
    # tweets = twitter.get_user_timeline(id=danforth,count=200)
    # # print(result)
    # # for tweet in tweets:
    # #     print(tweet['text'])
    # print('obtained {0} tweets'.format(len(tweets)))
    # min_id = tweets[-1]["id"]
    # print(min_id)
    # tweets = twitter.get_user_timeline(id=danforth,count=200,max_id=min_id)
    # print('obtained {0} tweets'.format(len(tweets)))
    # min_id = tweets[-1]["id"]
    # print(min_id)

    # grab the name from the command
    name = argv[1]
    
    # can also lookup with the id= flag
    user_info = twitter.lookup_user(screen_name=name)[0]
    # print(user_info)
    num_statuses = user_info["statuses_count"]
    user_id = user_info["id"]
    # print(num_statuses)
    
    alltweets = twitter.get_user_timeline(id=user_id,count=200)
    stolen = len(alltweets)
    min_id = alltweets[-1]["id"]
    while stolen < 3200 and stolen < num_statuses:
        tweets = twitter.get_user_timeline(id=user_id,count=200,max_id=min_id)
        alltweets.extend(tweets)
        min_id = alltweets[-1]["id"]
        stolen = len(alltweets)

    print('took {0} tweets from {1}'.format(len(alltweets),name))

    f = open('{0}-alltweets.json'.format(name),'w')
    # the indent=4 makes the json look nice
    json.dump(alltweets,f,indent=4)
    f.close()




