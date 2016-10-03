import json
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import re
from collections import Counter



def main():
    tweetobjects = read_data('tweets.json')
    justtweets = just_tweets(tweetobjects)
    removeurls = remove_urls(justtweets)
    justhashtags = just_hashtags(tweetobjects)
    justusers = just_users(tweetobjects)
    wordsofinterest = word_list(removeurls)
    print(type(justhashtags))
    print(type(justusers))
    print(type(wordsofinterest))
    finalwordsofinterest = total_list(wordsofinterest, justhashtags, justusers)



    # interesting_words = tgif(removeurls)
    # #print(justtweets[0])
    # #print(justhashtags[0])
    # print(len(interesting_words))
    # print(interesting_words[:20])


def read_data(tweets):
    """
    identify key terms from NOAA tweets
    """
    data_arr = []
    with open(tweets) as f:
        for line in f:
            data = json.loads(f.readline())
            data_arr.append(data)

    return data_arr


def just_tweets(jsondata):
    '''
    grabs just the tweets
    '''

    tweets_arr = []
    for elt in jsondata:
        for key in elt:
            tweet = elt[key]['text']
            tweets_arr.append(tweet)
    return tweets_arr


def remove_urls(tweets):
    '''
    removes the urls from tweets because http keeps showing up in key words
    '''
    cleaned_tweets = []
    for tweet in tweets:
        cleaned_tweet = re.sub(r"http\S+", "", tweet)
        cleaned_tweet = re.sub(r"@\S+", "", cleaned_tweet)
        cleaned_tweet = re.sub(r"&amp", "", cleaned_tweet)
        cleaned_tweet = re.sub(r"edt", '', cleaned_tweet)
        cleaned_tweet = re.sub(r"00", '', cleaned_tweet)
        cleaned_tweet = re.sub(r"mmi", '', cleaned_tweet)
        cleaned_tweet = re.sub(r"^RT", '', cleaned_tweet)
        cleaned_tweets.append(cleaned_tweet)

    return cleaned_tweets



def just_hashtags(data):
    '''
    grabs just the hashtags
    '''
    hashtags_arr = []
    for elt in data:
        for key in elt:
            hashtags = elt[key]['hashtags']
            hashtags_arr.append(hashtags)
    return hashtags_arr

def just_users(data):
    '''
    makes an array of users mentioned_usernames
    '''
    mentions_arr = []
    for elt in data:
        for key in elt:
            mentions = elt[key]['mentions']
            mentions_arr.append(mentions)
    return mentions_arr


def word_list(data):
    '''
    passing
    '''
    word_count_dict = {}
    stop = set(stopwords.words('english'))
    stop.add('')

    for tweet in data:
        split_tweet = tweet.split(" ")
        for word in split_tweet:
            if word.lower() in stop:
                pass
            elif word.lower() in word_count_dict:
                word_count_dict[word.lower()] += 1
            else:
                word_count_dict[word.lower()] = 1
    word_count_list = list(reversed(sorted(word_count_dict, key = lambda i: int(word_count_dict[i]))))
    top_150 = word_count_list[:150]
    print(top_150)
    return top_150







# def tgif(data):
#     tf = TfidfVectorizer(analyzer='word', ngram_range=(1,2), min_df = 0, stop_words = 'english')
#     tfidf_matrix = tf.fit_transform(data)
#     feature_names = tf.get_feature_names()
#     return feature_names
#













if __name__ == '__main__':
    main()


    '''
    TfidfVectorizer(input=u'tweets.json', )
    '''
