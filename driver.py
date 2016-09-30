"""
Runs the twitter bot.
Hey, I'm doing stuff, too!
"""
import tweepy
import json

config_fn = "twitter_app_keys.json"

def main():
    """
    bot driver
    """
    api_key, api_secret, user_token, user_secret = get_keys(config_fn)
    auth = authenticate(api_key, api_secret, user_token, user_secret)

    api = tweepy.API(auth)
    api.update_status("...")

    return


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


if __name__ == "__main__":
    main()
