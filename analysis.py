from textblob import TextBlob
import matplotlib.pyplot as plt
import pandas as pd


class sentimentAnalysis:

    def __init__(self, keyword, limit, begin_date, end_date):
        self.tweetTexts = []
        self.keyword = keyword
        self.limit = limit
        self.begin_date = begin_date
        self.end_date = end_date

    def read_from_dataset(self):
        data_set = pd.read_csv("result.csv")
        # print(data_set['Tweet_text'])
        for line in data_set['Tweet_text']:
            self.tweetTexts.append(line)

    def percentage(self, part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')

    def visualization(self, positive, wpositive, spositive, negative, wnegative, snegative, neutral):
        labels = ['Positive [' + str(positive) + '%]', 'Weakly Positive [' + str(wpositive) + '%]',
                  'Strongly Positive [' + str(spositive) + '%]', 'Neutral [' + str(neutral) + '%]',
                  'Negative [' + str(negative) + '%]', 'Weakly Negative [' + str(wnegative) + '%]',
                  'Strongly Negative [' + str(snegative) + '%]']
        sizes = [positive, wpositive, spositive, neutral, negative, wnegative, snegative]
        colors = ['yellowgreen', 'lightgreen', 'darkgreen', 'gold', 'red', 'lightsalmon', 'darkred']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.title('How people are reacting on ' + self.keyword + ' by analyzing ' + str(self.limit) + ' Tweets.')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()

    def sentiment_analysis_textblob(self):
        polarity = 0
        positive = 0
        wpositive = 0
        spositive = 0
        negative = 0
        wnegative = 0
        snegative = 0
        neutral = 0

        self.read_from_dataset()
        for tweet in self.tweetTexts:
            analysis = TextBlob(tweet)
            polarity += analysis.sentiment.polarity

            if analysis.sentiment.polarity == 0:
                neutral += 1
            elif 0 < analysis.sentiment.polarity <= 0.3:
                wpositive += 1
            elif 0.3 < analysis.sentiment.polarity <= 0.6:
                positive += 1
            elif 0.6 < analysis.sentiment.polarity <= 1:
                spositive += 1
            elif -0.3 < analysis.sentiment.polarity <= 0:
                wnegative += 1
            elif -0.6 < analysis.sentiment.polarity <= -0.3:
                negative += 1
            elif -1 < analysis.sentiment.polarity <= -0.6:
                snegative += 1

        positive = self.percentage(part=positive, whole=self.limit)
        wpositive = self.percentage(part=wpositive, whole=self.limit)
        spositive = self.percentage(part=spositive, whole=self.limit)
        negative = self.percentage(part=negative, whole=self.limit)
        wnegative = self.percentage(part=wnegative, whole=self.limit)
        snegative = self.percentage(part=snegative, whole=self.limit)
        neutral = self.percentage(part=neutral, whole=self.limit)

        polarity = polarity / self.limit

        print("How people are reacting on " + self.keyword + " by analyzing " + str(self.limit) + " tweets.")
        print()
        print("General Report: ")

        if polarity == 0:
            print("Neutral")
        elif 0 < polarity <= 0.3:
            print("Weakly Positive")
        elif 0.3 < polarity <= 0.6:
            print("Positive")
        elif 0.6 < polarity <= 1:
            print("Strongly Positive")
        elif -0.3 < polarity <= 0:
            print("Weakly Negative")
        elif -0.6 < polarity <= -0.3:
            print("Negative")
        elif -1 < polarity <= -0.6:
            print("Strongly Negative")

        print()
        print("Detailed Report: ")
        print(str(positive) + "% people thought it was positive")
        print(str(wpositive) + "% people thought it was weakly positive")
        print(str(spositive) + "% people thought it was strongly positive")
        print(str(negative) + "% people thought it was negative")
        print(str(wnegative) + "% people thought it was weakly negative")
        print(str(snegative) + "% people thought it was strongly negative")
        print(str(neutral) + "% people thought it was neutral")

        self.visualization(positive=positive, wpositive=wpositive, spositive=spositive, negative=negative,
                           wnegative=wnegative, snegative=snegative, neutral=neutral)
