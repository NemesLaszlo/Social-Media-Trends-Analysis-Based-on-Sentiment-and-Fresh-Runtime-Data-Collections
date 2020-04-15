import csv
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

    def dataset_building(self, tag, limit, begin_date, end_date, lang):
        with open('result.csv', mode='wt', encoding='UTF-8', newline='') as file:
            w = csv.writer(file)
            w.writerow(['Time', 'UserName', 'Tweet_text', 'All_Hashtags', 'Followers_count'])

            for tweet in tweepy.Cursor(self.api.search, q=tag + ' -filter:retweets', lang=lang, tweet_mode='extended',
                                       since=begin_date, until=end_date).items(limit):
                w.writerow([tweet.created_at,
                            tweet.user.screen_name,
                            self.clean_tweet(tweet.full_text),
                            [e['text'] for e in tweet._json['entities']['hashtags']],
                            tweet.user.followers_count])

    def clean_tweet(self, text):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", text).split())
