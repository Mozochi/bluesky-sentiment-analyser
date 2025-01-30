import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.probability import FreqDist
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from bin import preprocessing

df = pd.read_csv('https://raw.githubusercontent.com/pycaret/pycaret/master/datasets/amazon.csv')
df = df.drop(columns=['Positive'])
df['Opinion'] = ''
analyzer = SentimentIntensityAnalyzer()

# Function to determine the sentiment of a string
def sentiment(tokens):
    scores = analyzer.polarity_scores(tokens)
    sentiment = "Positive" if scores['compound'] >= 0.05 else "Negative" if scores['compound'] <= -0.05 else "Neutral"

    return sentiment


# Calling the Preprocessing function and the sentiment function to determine the sentiment of each review
for row, text in enumerate(df['reviewText']):
    df.at[row, 'Opinion'] = sentiment(preprocessing.Process(text))

