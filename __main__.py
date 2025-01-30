import pandas as pd
from nltk.corpus import twitter_samples
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.probability import FreqDist
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.classify import NaiveBayesClassifier
from bin import preprocessing


tweets = twitter_samples.strings('positive_tweets.json') + twitter_samples.strings('negative_tweets.json')

df = pd.DataFrame(tweets, columns=['Text'])
df['Sentiment'] = ''
#df = df.drop(columns=['Positive'])
#df['Opinion'] = ''
analyzer = SentimentIntensityAnalyzer()

# Function to determine the sentiment of a string
def sentiment(tokens):
    scores = analyzer.polarity_scores(tokens)
    sentiment = "Positive" if scores['compound'] >= 0.05 else "Negative" if scores['compound'] <= -0.05 else "Neutral"

    return sentiment


# Calling the Preprocessing function and the sentiment function to determine the sentiment of each review
for row, text in enumerate(df['Text']):
    df.at[row, 'Sentiment'] = sentiment(preprocessing.Process(text))

df.to_csv(r'tweets.csv', index=False)