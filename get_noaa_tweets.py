"""
This file will access NOAAs timeline, and download any new tweets that have
yet to be stored.
"""
import tweepy
import json
import time

config_fn = "twitter_app_keys.json"
outfile = "tweets.json"

def main():
    """
    bot driver
    """
    api_key, api_secret, user_token, user_secret = get_keys(config_fn)
    auth = authenticate(api_key, api_secret, user_token, user_secret)
    api = tweepy.API(auth)

    last_id_seen = determine_recent_id('tweets.json')

    user = api.get_user('NOAA')
    status_objs = []
    count = 0
    for status in limit_handled(tweepy.Cursor(api.user_timeline, id="NOAA",
                                                since_id=last_id_seen).items()):
        status_obj = process_noaa_tweets(status)
        status_objs.append(status_obj)
        count +=1

    print("Adding ", count, " new entries to tweet file.\n")
    writeout(outfile, status_objs)

    return

def process_noaa_tweets(status):
    """
    Get relevant information from status object.
    """
    return_obj = {}
    id_str = status.id_str
    tweet_text = status.text
    hashtags = []
    mentioned_usernames = []
    for obj in status.entities["hashtags"]:
        hashtags.append(obj["text"])
    for obj in status.entities["user_mentions"]:
        mentioned_usernames.append(obj["screen_name"])

    return_obj[id_str] = { "text": tweet_text,
                            "hashtags": hashtags,
                            "mentions": mentioned_usernames}

    return return_obj


def authenticate(api_key, api_secret, user_token, user_secret):
    """
    Logs in.
    """
    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(user_token, user_secret)
    return auth


def get_keys(fhandle):
    """
    input:
        filename
    output:
        API keys
        user keys (bot account)

        Note: Names are confusing because twitter/tweepy documentation is
    inconsistent. Conversion process happens here.
    We will use the Twitter convention.
    """
    with open(fhandle, "r") as f:
        key = json.loads(f.read())
    api_key = key["consumer_key"]
    api_secret = key["consumer_secret"]
    user_token = key["access_token"]
    user_secret = key["access_token_secret"]

    return api_key, api_secret, user_token, user_secret

def writeout(fhandle, data_arr):
    """
    Dump tweets into file
    """
    #First, let's read the old file.
    with open(fhandle, "r") as f:
        old_data = f.read()
    #Now let's write out the new data first, and the the old data afterwards.
    with open(fhandle, "w") as f:
        for obj in data_arr:
            f.write(json.dumps(obj, ensure_ascii=False))
            f.write("\n")
        f.write(old_data)

    return

def determine_recent_id(fhandle):
    """
    Read twitter json data, and determine what the most recent str_id recorded
    was.
    New data will always be written first, so we only need to read the first
    line of the file.
    """
    with open(fhandle, "r") as f:
        data_line = json.loads(f.readline())
    return [key for key in data_line][0] #there has to be a better way...

def limit_handled(cursor):
    """
    Rate limiting actions, baby!
    """
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            time.sleep(15 * 60)


if __name__ == "__main__":
    main()
