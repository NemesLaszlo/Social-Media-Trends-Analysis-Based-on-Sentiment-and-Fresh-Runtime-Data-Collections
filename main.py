import secret
import threading
from DatasetBuilder.twitterInformationBuilder import twitterInformationBuilder


def main():

    consumerAPI_Key = secret.consumerAPI_Key
    consumerAPI_Secret = secret.consumerAPI_Secret
    accessToken = secret.accessToken
    accessTokenSecret = secret.accessTokenSecret

    print("Dataset and Information base Building ...")
    keywords = str(input("Enter keywords to search for: (separated by a comma) "))
    limit = int(input("Enter the dataset builder limit: "))

    keywords_list = keywords.split(',')
    keywords_list_length = len(keywords_list)

    twitter_info_build = twitterInformationBuilder(consumerAPI_Key, consumerAPI_Secret, accessToken, accessTokenSecret)
    # twitter_info_build.InformationBuilder(keywords, limit, 'hu')

    for i in range(keywords_list_length):
        twitter_info_build.InformationBuilder(keywords_list[i], limit, 'hu')

    print("Dataset Build Finished!")


if __name__ == "__main__":
    main()
