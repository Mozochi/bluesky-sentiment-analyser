from nltk.corpus import twitter_samples
from sentimentAnalyser import sentimentAnalyser
import pandas as pd

theSentimentAnalyser = sentimentAnalyser()
tweets = twitter_samples.strings('positive_tweets.json') + twitter_samples.strings('negative_tweets.json')

df = pd.DataFrame(tweets, columns=['Text'])
df['Sentiment'] = ''

# Calling the Preprocessing function and the sentiment function to determine the sentiment of each review
for row, text in enumerate(df['Text']):
    df.at[row, 'Sentiment'] = theSentimentAnalyser.sentiment(theSentimentAnalyser.Process(text))

df.to_csv(r'tweets.csv', index=False)
