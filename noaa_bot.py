"""
"""

import tweepy
import json
import time


class Noaa_Bot:
    def __init__(self):
        self.config_fn = "data/twitter_app_keys.json"
        self.tweet_data_fn = "data/tweets.json"
        self.moc_data_fn = "data/moc_last_read_tweet.json"
        #self.moc_data_fn = 'test.json'
        self.api_key = None
        self.api_secret = None
        self.user_token = None
        self.user_secret = None
        self.get_keys()
        self.last_tweet_id = self.last_processed_tweet_id()
        self.moc_data = self.read_moc_info()
        return

    def get_keys(self):
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
        with open(self.config_fn, "r") as f:
            key = json.loads(f.read())
        self.api_key = key["consumer_key"]
        self.api_secret = key["consumer_secret"]
        self.user_token = key["access_token"]
        self.user_secret = key["access_token_secret"]

        return

    def write_noaa_tweets(self, data_arr):
        """
        Dump tweets into file
        """
        if data_arr == []:
            return
        print("Writing ", len(data_arr), " new NOAA tweets to JSON document.")
        #First, let's read the old file.
        with open(self.tweet_data_fn, "r") as f:
            old_data = f.read()
        #Now let's write out the new data first, and the the old data afterwards.
        with open(self.tweet_data_fn, "w") as f:
            for obj in data_arr:
                f.write(json.dumps(obj, ensure_ascii=False))
                f.write("\n")
            f.write(old_data)

        return

    def write_moc_info(self, data_obj):
        """
        Write out Members of Congress names, and the id of the last tweet we
        processed by them.
        """
        with open(self.moc_data_fn, "w") as f:
            f.write(json.dumps(data_obj))
        return

    def read_moc_info(self):
        """
        Read in the previously saved Member of Congress/last_tweet_id info.
        """
        with open(self.moc_data_fn, "r") as f:
            data_obj = json.loads(f.read())
        return data_obj

    def last_processed_tweet_id(self):
        """
        Read twitter json data, and determine what the most recent str_id recorded
        was.
        New data will always be written first, so we only need to read the first
        line of the file.
        """
        with open(self.tweet_data_fn, "r") as f:
            data_line = json.loads(f.readline())
        return [key for key in data_line][0]

    def process_noaa_tweets(self, status):
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
