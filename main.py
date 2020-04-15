import secret
from analysis import sentimentAnalysis
from DatasetBuilder.twitterInformationBuilder import twitterInformationBuilder
from DatasetBuilder.twitterDatasetBuilder import twitterDatasetBuilder
import Tensorflow.naturalLanguageProcessing as tensorflow_npl


def main():

    consumerAPI_Key = secret.consumerAPI_Key
    consumerAPI_Secret = secret.consumerAPI_Secret
    accessToken = secret.accessToken
    accessTokenSecret = secret.accessTokenSecret

    print("DataSet and Information Base Building ...")
    keyword = str(input("Enter keywords to search for: "))
    limit = int(input("Enter the DataSet builder limit: "))
    print("Use - to separate the date format. (For Example: 2020-04-15) ")
    begin_date = str(input("Enter the START date to search for in this period: "))
    end_date = str(input("Enter the END date to search for in this period: "))

    # Information Builder Init
    twitter_info_build = twitterInformationBuilder(ConsumerAPI_Key=consumerAPI_Key,
                                                   ConsumerAPI_Secret=consumerAPI_Secret,
                                                   Access_Token=accessToken, Access_Token_Secret=accessTokenSecret)
    # DataSet Builder Init
    twitter_dataset_build = twitterDatasetBuilder(ConsumerAPI_Key=consumerAPI_Key,
                                                  ConsumerAPI_Secret=consumerAPI_Secret,
                                                  Access_Token=accessToken, Access_Token_Secret=accessTokenSecret)
    # Analysis class for Sentiment Analysis by Trend~Keyword
    analysis = sentimentAnalysis(keyword=keyword, limit=limit, begin_date=begin_date, end_date=end_date)

    # Build information sheets about this theme (Tweets,HashTags and Links)
    # twitter_info_build.information_builder(tag=keyword, limit=limit, lang="en")
    # Build a DataSet about this theme for analysis
    twitter_dataset_build.dataset_building(tag=keyword, limit=limit, begin_date=begin_date, end_date=end_date,
                                           lang="en")
    # Sentiment Analysis with TextBlob and Visualization
    analysis.sentiment_analysis_textblob()
    # Sentiment Analysis, Natural Language Processing with Tensorflow 2.0
    # tensorflow_npl.training_and_analyze(keyword_parameter=keyword, limit_parameter=limit)


if __name__ == "__main__":
    main()
