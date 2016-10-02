"""
"""
import tweepy
import time
from noaa_bot import Noaa_Bot


def main():

    twitter_bot = Noaa_Bot()
    auth = authenticate(twitter_bot.api_key, twitter_bot.api_secret,
        twitter_bot.user_token, twitter_bot.user_secret)
    api = tweepy.API(auth)

    #Check for New NOAA tweets to add to the document.
    print("Updating NOAA information...")
    new_noaa_tweets = get_noaa_tweets(twitter_bot, api)
    twitter_bot.write_noaa_tweets(new_noaa_tweets)

    print("Updating MOC information...")
    twitter_bot.read_moc_info()
    #Go through each member of congress.
    new_moc_data = process_new_moc_tweets(twitter_bot, api)

    print("Writing out updated last read MOC tweets.")
    twitter_bot.write_moc_info(new_moc_data)

    return

def authenticate(api_key, api_secret, user_token, user_secret):
    """
    Logs in.
    """
    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(user_token, user_secret)
    return auth

def get_noaa_tweets(bot, api):
    """
    Get relevant information from noaa tweet objects.
    """
    noaa_user = api.get_user('NOAA')
    status_objs = []
    for status in limit_handled(tweepy.Cursor(api.user_timeline,
        noaa_user.screen_name, since_id=bot.last_tweet_id).items()):
        status_obj = bot.process_noaa_tweets(status)
        status_objs.append(status_obj)
    return status_objs


def limit_handled(cursor):
    """
    Rate limiting actions, baby!
    """
    while True:
        try:
            yield cursor.next()
        except tweepy.error.TweepError:
            time.sleep(15 * 60)

def process_new_moc_tweets(bot, api):
    """
    Go through new tweets since we last read any by a member of congress, and
    determine if they're interesting.

    Returns moc_object reflecting most up-to-date read twitter statuses.
    """
    new_moc_data = {}
    for key in bot.moc_data:
        #keys are moc screen_names.
        last_id_seen = bot.moc_data[key]
        for status in limit_handled(tweepy.Cursor(api.user_timeline, \
            screen_name=key, since_id=last_id_seen).items()):
                #process moc tweet.
                tweet_text = status.text
        new_moc_data[key] = get_last_tweet_id(key, api)
    return new_moc_data

def get_last_tweet_id(screen_name, api):
    """
    Returns the id_str attribute of the last twitter post.
    """
    tweets = limit_handled(tweepy.Cursor(api.user_timeline, screen_name = screen_name, count=1).items())
    for tweet in tweets:
        #there should only be one element here
        return tweet.id_str


if __name__ == "__main__":
    main()
