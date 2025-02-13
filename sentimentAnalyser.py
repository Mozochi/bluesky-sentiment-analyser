import nltk
from nltk.corpus import twitter_samples
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.probability import FreqDist
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.classify import NaiveBayesClassifier

class sentimentAnalyser:

    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def Process(self, text) -> str:
        tokens = word_tokenize(text.lower())
        filtered_tokens = [token for token in tokens if token not in stopwords.words('english')]

        lemmatizer = WordNetLemmatizer()
        lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]

        processed_tokens = ' '.join(lemmatized_tokens)

        return processed_tokens

    # Function to determine the sentiment of a string
    def sentiment(self, tokens):
        scores = self.analyzer.polarity_scores(tokens)
        sentiment = "Positive" if scores['compound'] >= 0.05 else "Negative" if scores['compound'] <= -0.05 else "Neutral"

        return sentiment
