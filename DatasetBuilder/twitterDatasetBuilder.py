import tweepy
import re


class twitterDatasetBuilder:

    def __init__(self, ConsumerAPI_Key, ConsumerAPI_Secret, Access_Token, Access_Token_Secret):
        self.consumerAPI_Key = ConsumerAPI_Key
        self.consumerAPI_Secret = ConsumerAPI_Secret
        self.accessToken = Access_Token
        self.accessTokenSecret = Access_Token_Secret

        auth = tweepy.OAuthHandler(self.consumerAPI_Key, self.consumerAPI_Secret)
        auth.set_access_token(self.accessToken, self.accessTokenSecret)
        self.api = tweepy.API(auth)

        self.tweets = []

    def dataset_building(self, tag, limit, lang):
        self.tweets = tweepy.Cursor(self.api.search, q=tag, lang=lang).items(limit)
        f = open('result.csv', 'w')

        for tweet in self.tweets:
            f.write(str(self.clean_tweet(tweet.text).encode('utf-8')))
            f.write('\n')

        f.close()

    def clean_tweet(self, text):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", text).split())
