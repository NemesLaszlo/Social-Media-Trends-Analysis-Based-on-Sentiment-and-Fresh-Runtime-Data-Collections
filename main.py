import threading
import secret
from analysis import sentimentAnalysis
from DatasetBuilder.twitterInformationBuilder import twitterInformationBuilder
from DatasetBuilder.twitterDatasetBuilder import twitterDatasetBuilder


def main():

    consumerAPI_Key = secret.consumerAPI_Key
    consumerAPI_Secret = secret.consumerAPI_Secret
    accessToken = secret.accessToken
    accessTokenSecret = secret.accessTokenSecret

    print("DataSet and Information Base Building ...")
    keyword = str(input("Enter keywords to search for: "))
    limit = int(input("Enter the DataSet builder limit: "))

    # Information Builder Init
    twitter_info_build = twitterInformationBuilder(ConsumerAPI_Key=consumerAPI_Key,
                                                   ConsumerAPI_Secret=consumerAPI_Secret,
                                                   Access_Token=accessToken, Access_Token_Secret=accessTokenSecret)
    # DataSet Builder Init
    twitter_dataset_build = twitterDatasetBuilder(ConsumerAPI_Key=consumerAPI_Key,
                                                  ConsumerAPI_Secret=consumerAPI_Secret,
                                                  Access_Token=accessToken, Access_Token_Secret=accessTokenSecret)
    # Analysis class for Sentiment Analysis by Trend~Keyword
    analysis = sentimentAnalysis(keyword=keyword, limit=limit)

    # Build information sheets about this theme (Tweets,HashTags and Links)
    twitter_info_build.information_builder(tag=keyword, limit=limit, lang="en")
    # Build a DataSet about this theme for analysis
    twitter_dataset_build.dataset_building(tag=keyword, limit=limit, lang="en")
    # Sentiment Analysis with TextBlob and Visualization
    analysis.sentiment_analysis_textblob()


if __name__ == "__main__":
    main()
