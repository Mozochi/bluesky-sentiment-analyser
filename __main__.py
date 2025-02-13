from nltk.corpus import twitter_samples
from bin import sentimentAnalyser
from bin import preprocessing
import pandas as pd

def main():
    Analyse = sentimentAnalyser.sentimentAnalyser()

    tweets = twitter_samples.strings('positive_tweets.json') + twitter_samples.strings('negative_tweets.json')

    df = pd.DataFrame(tweets, columns=['Text'])
    df['Sentiment'] = ''

    # Calling the Preprocessing function and the sentiment function to determine the sentiment of each review
    for row, text in enumerate(df['Text']):
        df.at[row, 'Sentiment'] = Analyse.sentiment(preprocessing.Process(text))

    df.to_csv(r'tweets.csv', index=False)


if __name__ == '__main__':
    main()