"""
Runs the twitter bot.
Hey, I'm doing stuff, too!
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

    user = api.get_user('NOAA')
    status_objs = []
    count = 0
    for status in limit_handled(tweepy.Cursor(api.user_timeline, id="NOAA").items()):
        status_obj = process_noaa_tweets(status)
        status_objs.append(status_obj)
        count +=1

    print(count)
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
    with open(fhandle, "w") as f:
        for obj in data_arr:
            f.write(json.dumps(obj, ensure_ascii=False))
            f.write("\n")

    return

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
